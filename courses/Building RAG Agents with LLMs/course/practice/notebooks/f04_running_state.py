from langchain.schema.runnable.passthrough import RunnableAssign
from langchain.schema.runnable import RunnableBranch, RunnablePassthrough
from rich.style import Style
from rich.console import Console
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from functools import partial
from typing import Dict, Union, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
import os

# Cargar las variables de entorno del archivo .env
from dotenv import load_dotenv
load_dotenv()
# from langchain_nvidia_ai_endpoints import ChatNVIDIA


console = Console()
base_style = Style(color="#76B900", bold=True)
pprint = partial(console.print, style=base_style)


def RPrint(preface="State 1: "):
    def print_and_return(x, preface=""):
        print(f"{preface}{x}")
        return x
    return RunnableLambda(partial(print_and_return, preface=preface))


def PPrint(preface="State 2: "):
    def print_and_return(x, preface=""):
        pprint(preface, x)
        return x
    return RunnableLambda(partial(print_and_return, preface=preface))


"""
## **Part 1:** Keeping Variables Flowing

Recall the zero-shot classification example from the last notebook
"""

# Zero-shot classification prompt and chain w/ explicit few-shot prompting
sys_msg = (
    "Choose the most likely topic classification given the sentence as context."
    " Only one word, no explanation.\n[Options : {options}]"
)

zsc_prompt = ChatPromptTemplate.from_template(
    f"{sys_msg}\n\n"
    "[[The sea is awesome]][/INST]boat</s><s>[INST]"
    "[[{input}]]"
)

# Define your simple instruct_model Crear una instancia de 'ChatNVIDIA' con el
# modelo especificado
instruct_chat = ChatOpenAI(model="gpt-4o-mini", max_tokens=60)

# Unir la instancia de chat con un 'StrOutputParser' y asignar a 'instruct_llm'
instruct_llm = instruct_chat | StrOutputParser()

# Vincular la instancia de chat con una lista de palabras de parada y unir con
# un 'StrOutputParser', asignar a 'one_word_llm'
one_word_llm = instruct_chat.bind(stop=[" ", "\n"]) | StrOutputParser()

# Crear 'zsc_chain' uniendo 'zsc_prompt' con 'one_word_llm'
zsc_chain = zsc_prompt | one_word_llm


# Function that just prints out the first word of the output. With early
# stopping bind
def zsc_call(input, options=["car", "boat", "airplane", "bike"]):
    return zsc_chain.invoke({"input": input, "options": options}).split()[0]


def classify():

    print("-" * 80)
    print(zsc_call("Should I take the next exit, or keep going to the next one?"))

    print("-" * 80)
    print(zsc_call("I get seasick, so I think I'll pass on the trip"))

    print("-" * 80)
    print(zsc_call("I'm scared of heights, so flying probably isn't for me"))


"""
We want it to act like a function, so all we want it to do is generate the
output and return it
"""

gen_prompt = ChatPromptTemplate.from_template(
    "Haz una nueva oracion sobre el siguiente tema: {topic}. Se creativo!"
)

gen_chain = gen_prompt | instruct_llm


def like_a_function():

    input_msg = "Estoy en la playa"
    options = ["car", "boat", "airplane", "bike"]

    chain = (
        # -> {"input", "options"}
        {'topic': zsc_chain}
        | PPrint()
        # -> {**, "topic"}
        | gen_chain
        # -> string
    )

    r = chain.invoke({"input": input_msg, "options": options})
    print(f"{r=}")


def propagating_state():
    """
    However, it's a bit problematic when you want to keep the information
    flowing since we lose the topic and input variables in generating our
    response. If we wanted do something with both the output and the input, we'd
    need a to make sure that both variables pass through.

    Lucky for us, we can use the mapping runnable (i.e. interpretted from a
    dictionary or using manual `RunnableMap`) to pass both of the variables
    through by assigning the output of our chain to just a single key and
    letting the other keys propagate as desired. Alternatively, we could also
    use `RunnableAssign` to merge the state-consuming chain's output with the
    input dictionary by default.

    With this technique, we can propagate whatever we want through our chain
    system:
    """

    big_chain = (
        PPrint()
        # El flujo primero aplica un mapeo manual para extraer la entrada
        # relevante y procesarla con zsc_chain. Manual mapping. Can be useful
        # sometimes and inside branch chains
        | {'input': lambda d: d.get('input'), 'topic': zsc_chain}
        | PPrint()
        # Luego, se usa RunnableAssign para pasar el resultado de gen_chain al
        # estado bajo la clave 'generation'. RunnableAssign passing. Better for
        # running state chains by default
        | RunnableAssign({'generation': gen_chain})
        | PPrint()
        # Finalmente, se combina la entrada original y la generación con una
        # plantilla (ChatPromptTemplate) que se pasa a otro modelo de lenguaje
        # (instruct_llm). Using the input and generation together
        | RunnableAssign({'combination': (
            ChatPromptTemplate.from_template(
                "Considera los siguientes pasajes:"
                "\nP1: {input}"
                "\nP2: {generation}"
                "\n\nCombina las ideas de ambos pasajes en una simple expresion en espanol."
            )
            | instruct_llm
        )})
    )

    # La cadena comienza con una entrada(big_chain.invoke) que contiene un
    # texto(input) y una lista de opciones.
    output = big_chain.invoke({
        "input": "Me siento enfermo, asi que voy a quedarme en casa",
        "options": ["car", "boat", "airplane", "bike", "unknown"]
    })
    # Final Output: { 'input': 'Me siento enfermo, asi que voy a quedarme en
    # casa', 'topic': ' unknown', 'generation': '...', 'combination': '...' } Se
    #     han ido pasando todas las variables por todo el flujo <---
    pprint("Final Output: ", output)


"""
## **Part 2:** Running State Chain

Una **Running State Chain** permite mantener un estado acumulativo en cadenas
complejas. Este enfoque asegura que un diccionario con variables importantes (el
"estado en ejecución") fluya a través de la cadena, conservando la información.
Las "ramas" dentro de la cadena pueden extraer este estado y generar respuestas,
y deben ejecutarse dentro de un contexto `RunnableAssign`, tomando su entrada
del estado.

Este patrón es comparable a una clase en Python: la cadena es como la clase
abstracta, el estado como los atributos, y las ramas como los métodos que usan
esos atributos. Forzar este paradigma permite acumular y reutilizar estados a lo
largo de la cadena, e incluso reutilizar las salidas como entradas, creando un
ciclo similar a un bucle.
"""

"""
## **Part 3:** Implementing a Knowledge Base with Running State Chain

Una **Running State Chain** puede ampliarse para manejar tareas más complejas,
como la creación de **sistemas dinámicos** que evolucionan a través de
interacciones. Aquí se implementa un sistema con una **base de conocimiento** y
**relleno de espacios habilitado por JSON**:

- **Base de Conocimiento**: Un almacén de información relevante que el modelo de
  lenguaje mantiene actualizado.
- **Relleno de Espacios con JSON**: Técnica que utiliza un modelo ajustado por
  instrucciones para generar una salida en formato JSON, donde se rellenan
  espacios específicos con información útil y relevante proporcionada por el
  modelo.

Este enfoque permite al sistema acumular y estructurar datos de manera eficiente
durante múltiples interacciones.

---

Para construir un sistema inteligente y dinámico que retenga y actualice
información a lo largo de la conversación, necesitamos un método que estructure
y valide los datos de manera eficiente. Aquí es donde la combinación de
**LangChain** y **Pydantic** resulta crucial.

**Pydantic** es una biblioteca de Python que facilita la validación y
estructuración de modelos de datos. Utiliza clases modelo que validan objetos
(como datos o clases) con una sintaxis simplificada y muchas opciones de
personalización. Esto se usa ampliamente en LangChain, especialmente en casos
donde se requiere conversión o validación de datos.

Un **modelo** de Pydantic es útil para definir clases con argumentos esperados y
validaciones personalizadas. Aunque no nos enfocaremos en los scripts de
validación en este curso, podemos utilizar un `BaseModel` de Pydantic para
definir una **base de conocimiento** estructurada, usando variables `Field` para
especificar los datos que queremos retener y validar a lo largo de la
conversación.
"""


class KnowledgeBase1(BaseModel):
    # Fields of the BaseModel, which will be validated/assigned when the
    # knowledge base is constructed
    topic: str = Field('general', description="Current conversation topic")
    user_preferences: Dict[str, Union[str, int]] = Field(
        {}, description="User preferences and choices")
    session_notes: str = Field(
        "", description="Notes on the ongoing session")
    unresolved_queries: list = Field(
        [], description="Unresolved user queries")
    action_items: list = Field(
        [], description="Actionable items identified during the conversation")


def knowledge_base():

    # print(repr(KnowledgeBase1(topic="Travel")) + "\n\n")

    # This functionality generates instructions for creating valid inputs to the
    # Knowledge Base, which in turn helps the LLM by providing a concrete
    # one-shot example of the desired output format.

    # Crear un objeto PydanticOutputParser con KnowledgeBase1 como el objeto pydantic
    parser = PydanticOutputParser(pydantic_object=KnowledgeBase1)

    # Obtener las instrucciones de formato del parser
    instruct_string = parser.get_format_instructions()

    # Imprimir las instrucciones de formato
    pprint(instruct_string)

############################################################################
# Definition of RExtract


def RExtract(pydantic_class, llm, prompt):
    '''
    Módulo de extracción ejecutable que devuelve un diccionario de conocimiento
    poblado mediante extracción de llenado de espacios.
    '''
    # Crear un parser de salida de Pydantic con la clase pydantic proporcionada
    parser = PydanticOutputParser(pydantic_object=pydantic_class)

    # Asignar instrucciones de formato utilizando una función lambda para obtener
    # las instrucciones de formato del parser
    # La lambda se ejecutará cuando RunnableAssign sea invocado o utilizado dentro de ese flujo de trabajo. E
    instruct_merge = RunnableAssign(
        {'format_instructions': lambda x: parser.get_format_instructions()})

    # Definir una función para preprocesar la cadena de entrada
    def preparse(string):
        # Si la cadena no contiene '{', agregar '{' al inicio
        if '{' not in string:
            string = '{' + string
        # Si la cadena no contiene '}', agregar '}' al final
        if '}' not in string:
            string = string + '}'
        # Reemplazar caracteres específicos en la cadena
        string = (string
                  .replace("\\_", "_")  # Reemplazar "\_" con "_"
                  # Reemplazar saltos de línea con espacios
                  .replace("\n", " ")
                  .replace("\]", "]")   # Reemplazar "\]" con "]"
                  .replace("\[", "[")   # Reemplazar "\[" con "["
                  )
        print(string)  # Bueno para diagnósticos
        return string

    # Devolver una cadena de operaciones que incluye las instrucciones de formato,
    # el prompt, el modelo de lenguaje y la función de preprocesamiento
    # return instruct_merge | prompt | llm | PPrint | preparse | parser
    return instruct_merge | prompt | llm | preparse | parser


def knowledge_base_chain():

    # Crear una plantilla de mensaje de chat a partir de una plantilla
    parser_prompt = ChatPromptTemplate.from_template(
        "Actualiza la base de conocimiento: {format_instructions}. Solo usa información de la entrada."
        "\n\nNUEVO MENSAJE: {input}"
    )

    # Crear un extractor usando RExtract con KnowledgeBase1, instruct_llm y parser_prompt
    extractor = RExtract(KnowledgeBase1, instruct_llm, parser_prompt)

    # Invocar el extractor con una entrada específica
    knowledge = extractor.invoke(
        {'input': "¡Me encantan las flores! ¡Las orquídeas son increíbles! ¿Puedes comprarme algunas?"})
    # Imprimir el conocimiento extraído
    pprint(knowledge)
    """ Ten en cuenta que este proceso puede fallar debido a la naturaleza difusa
    de la predicción de los LLM, especialmente con modelos que no están optimizados
    para seguir instrucciones. Para este proceso, es importante tener un LLM que
    siga instrucciones con verificaciones adicionales y rutinas de fallo elegantes.
    """


class KnowledgeBase2(BaseModel):
    firstname: str = Field(
        'unknown', description="Nombre del usuario del chat, desconocido si es desconocido")
    lastname: str = Field(
        'unknown', description="Apellido del usuario del chat, desconocido si es desconocido")
    location: str = Field(
        'unknown', description="Dónde se encuentra el usuario")
    summary: str = Field(
        'unknown', description="Resumen en curso de la conversación. Actualiza esto con la nueva entrada")
    response: str = Field(
        'unknown', description="Una respuesta ideal para el usuario basada en su nuevo mensaje")


"""
Actualizaciones Dinámicas de la Base de Conocimiento Podemos crear un sistema
que actualice continuamente la Base de Conocimiento durante una conversación.
Esto se logra al alimentar el estado actual de la base, junto con nuevas
entradas del usuario, de vuelta al sistema, permitiendo actualizaciones
continuas.

A continuación, se presenta un ejemplo que demuestra el poder de     esta
formulación para rellenar detalles de manera dinámica, aunque también muestra
algunas limitaciones, como que el rendimiento del relleno de espacios puede no
ser tan eficiente como el rendimiento general de las respuestas:
"""


def dynamic_knowledge_base_updates():
    parser_prompt = ChatPromptTemplate.from_template(
        "Estás chateando con un usuario. El usuario acaba de responder ('input'). Por favor, actualiza la base de conocimiento."
        " Registra tu respuesta en la etiqueta 'response' para continuar la conversación."
        " No alucines ningún detalle y asegúrate de que la base de conocimiento no sea redundante."
        " Actualiza las entradas con frecuencia para adaptarte al flujo de la conversación."
        "\n{format_instructions}"
        "\n\nBASE DE CONOCIMIENTO ANTIGUA: {know_base}"
        "\n\nNUEVO MENSAJE: {input}"
        "\n\nNUEVA BASE DE CONOCIMIENTO:"
    )

    instruct_llm = ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

    # Una cadena de operaciones que incluye las instrucciones de formato, el
    # prompt, el modelo de lenguaje y la función de preprocesamiento
    extractor = RExtract(KnowledgeBase2, instruct_llm, parser_prompt)

    info_update = RunnableAssign({'know_base': extractor})

    # Inicializa la base de conocimiento y observa lo que obtienes
    state = {'know_base': KnowledgeBase2()}
    state['input'] = "¡Me llamo Carmen Sandiego! ¡Adivina dónde estoy! Pista: Está en algún lugar de los Estados Unidos."
    state = info_update.invoke(state)
    pprint(state)

    state['input'] = "Estoy en un lugar considerado la cuna del Jazz."
    state = info_update.invoke(state)
    pprint(state)

    state['input'] = "Sí, estoy en Nueva Orleans... ¿Cómo lo supiste?"
    state = info_update.invoke(state)
    pprint(state)


"""
## **Part 4: [Exercise]** Airline Customer Service Bot

Ejercicio: Bot de Servicio al Cliente de Aerolíneas En este ejercicio,
utilizaremos las herramientas aprendidas para implementar un gestor de diálogo
simple pero efectivo. El objetivo es crear un bot de soporte para aerolíneas que
ayude a los clientes a obtener información sobre sus vuelos.

Paso 1: Crear una interfaz para simular una base de datos Vamos a crear una
interfaz sencilla que simule una base de datos, almacenando información del
cliente en un diccionario:
"""

############################################################################
# Function that can be queried for information. Implementation details not
# important


def get_flight_info(d: dict) -> str:
    """
    Ejemplo de una función de recuperación que toma un diccionario como clave.
    Se asemeja a una consulta de base de datos SQL.
    """
    req_keys = ['first_name', 'last_name', 'confirmation']
    assert all((key in d)
               for key in req_keys), f"Se esperaba un diccionario con las claves {req_keys}, se obtuvo {d}"

    # Conjunto de datos estático. get_key y get_val se pueden usar para trabajar con él, y
    # db es tu variable
    keys = req_keys + ["departure", "destination",
                       "departure_time", "arrival_time", "flight_day"]
    values = [
        ["Jane", "Doe", 12345, "San Jose", "Nueva Orleans",
         "12:30 PM", "9:30 PM", "mañana"
         ],
        ["John", "Smith", 54321, "Nueva York", "Los Ángeles",
         "8:00 AM", "11:00 AM", "domingo"
         ],
        ["Alice", "Johnson", 98765, "Chicago", "Miami",
         "7:00 PM", "11:00 PM", "la próxima semana"
         ],
        ["Bob", "Brown", 56789, "Dallas", "Seattle",
         "1:00 PM", "4:00 PM", "ayer"
         ],
    ]

    def get_key(d): return "|".join(
        [d['first_name'], d['last_name'], str(d['confirmation'])])

    def get_val(l): return {k: v for k, v in zip(keys, l)}
    db = {get_key(get_val(entry)): get_val(entry) for entry in values}

    # Search for the matching entry
    data = db.get(get_key(d))
    if not data:
        return (
            f"Based on {req_keys} = {get_key(d)}) from your knowledge base, no info on the user flight was found."
            " This process happens every time new info is learned. If it's important, ask them to confirm this info."
        )
    return (
        f"{data['first_name']} {data['last_name']}'s flight from {data['departure']} to {data['destination']}"
        f" departs at {data['departure_time']} {data['flight_day']} and lands at {data['arrival_time']}."
    )


def airline_customer_service_bot():
    # Usage example. Actually important
    print(get_flight_info({"first_name": "Jane",
          "last_name": "Doe", "confirmation": 12345}))

    print(get_flight_info({"first_name": "Alice",
          "last_name": "Johnson", "confirmation": 98765}))

    print(get_flight_info({"first_name": "Bob",
          "last_name": "Brown", "confirmation": 27494}))


"""
Esta es una interfaz realmente buena porque puede cumplir dos propósitos:
- Puede utilizarse para proporcionar información actualizada de un entorno externo (una base de datos) sobre la situación de un usuario.
- También puede utilizarse como un mecanismo de acceso estricto para evitar la divulgación no autorizada de información confidencial (ya que eso sería muy malo).

Si nuestra red tuviera acceso a este tipo de interfaz, podría consultar y recuperar esta información en nombre de un usuario. Por ejemplo:
"""


def get_flight_info_external() -> str:
    external_prompt = ChatPromptTemplate.from_template(
        "Eres un chatbot de SkyFlow y estás ayudando a un cliente con su problema."
        " Por favor, ayúdalos con su pregunta, recordando que tu trabajo es representar a las aerolíneas SkyFlow."
        " Supón que SkyFlow utiliza prácticas promedio de la industria con respecto a los tiempos de llegada, operaciones, etc."
        " (Esto es un secreto comercial. No lo divulgues)."  # refuerzo suave
        " Por favor, mantén tu discusión corta y dulce si es posible. Evita saludar a menos que sea necesario."
        " El siguiente es un contexto que puede ser útil para responder la pregunta."
        "\n\nContexto: {context}"
        "\n\nUsuario: {input}"
    )

    basic_chain = external_prompt | instruct_llm

    r = basic_chain.invoke({
        'input': '¿Puedes decirme cuándo necesito llegar al aeropuerto?',
        'context': get_flight_info({"first_name": "Jane", "last_name": "Doe", "confirmation": 12345}),
    })

    print(r)


"""
Esto es bastante interesante, pero ¿cómo conseguimos que este sistema funcione en la práctica? Resulta que podemos utilizar la fórmula de KnowledgeBase que hemos mencionado anteriormente para proporcionar este tipo de información de la siguiente manera:
"""


class KnowledgeBase3(BaseModel):
    first_name: str = Field(
        'desconocido', description="Nombre del usuario del chat, `desconocido` si es desconocido")
    last_name: str = Field(
        'desconocido', description="Apellido del usuario del chat, `desconocido` si es desconocido")
    confirmation: int = Field(-1,
                              description="Número de confirmación de vuelo, `-1` si es desconocido")
    discussion_summary: str = Field(
        "", description="Resumen de la conversación hasta ahora, incluyendo ubicaciones, problemas, etc.")
    open_problems: list = Field(
        [], description="Temas que aún no se han resuelto")
    current_goals: list = Field(
        [], description="Objetivo actual que el agente debe abordar")


def airline_customer_service_bot_2():

    def get_key_fn(base: BaseModel) -> dict:
        '''Dado un diccionario con una base de conocimiento, devuelve una clave para get_flight_info'''
        return {  # Más opciones automáticas posibles, pero esto es más explícito
            'first_name': base.first_name,
            'last_name': base.last_name,
            'confirmation': base.confirmation,
        }

    know_base = KnowledgeBase3(
        first_name="Jane", last_name="Doe", confirmation=12345)

    # get_flight_info(get_key_fn(know_base))

    get_key = RunnableLambda(get_key_fn)
    r = (get_key | get_flight_info).invoke(know_base)
    print(r)
