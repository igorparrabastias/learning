from dotenv import load_dotenv
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
import gradio as gr
from langchain.schema.runnable.passthrough import RunnableAssign
from langchain.output_parsers import PydanticOutputParser
from operator import itemgetter
import os


# Cargar las variables de entorno del archivo .env
load_dotenv()

console = Console()
base_style = Style(color="#76B900", bold=True)
pprint = partial(console.print, style=base_style)

external_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Eres un chatbot de SkyFlow Airlines y estás ayudando a un cliente con su problema."
        " ¡Por favor, chatea con ellos! ¡Mantente conciso y claro!"
        " Tu base de conocimiento en ejecución es: {know_base}."
        " Esto es solo para ti; ¡No lo menciones!"
        " \nUsando eso, recuperamos lo siguiente: {context}\n"
        " Si proporcionan información y la recuperación falla, pide que confirmen su nombre y apellido y la confirmación."
        " No les pidas ninguna otra información personal."
        " Si no es importante saber sobre su vuelo, no preguntes."
        " La verificación ocurre automáticamente; no puedes verificar manualmente."
    )),
    ("assistant", "{output}"),
    ("user", "{input}"),
])


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


##########################################################################
# Knowledge Base Things


class KnowledgeBase(BaseModel):
    first_name: str = Field(
        'unknown', description="Nombre del usuario del chat, `desconocido` si es desconocido")
    last_name: str = Field(
        'unknown', description="Apellido del usuario del chat, `desconocido` si es desconocido")
    confirmation: Optional[int] = Field(
        None, description="Número de confirmación de vuelo, `-1` si es desconocido")
    discussion_summary: str = Field(
        "", description="Resumen de la conversación hasta ahora, incluyendo ubicaciones, problemas, etc.")
    open_problems: str = Field(
        "", description="Temas que aún no se han resuelto")
    current_goals: str = Field(
        "", description="Objetivo actual que el agente debe abordar")


parser_prompt = ChatPromptTemplate.from_template(
    "Eres un asistente de chat que representa a la aerolínea SkyFlow y estás tratando de rastrear información sobre la conversación."
    " Acabas de recibir un mensaje del usuario. Por favor, completa el esquema basado en el chat."
    "\n\n{format_instructions}"
    "\n\nOLD KNOWLEDGE BASE: {know_base}"
    "\n\nASSISTANT RESPONSE: {output}"
    "\n\nUSER MESSAGE: {input}"
    "\n\nNEW KNOWLEDGE BASE: "
)

# Your goal is to invoke the following through natural conversation
# get_flight_info({"first_name" : "Jane", "last_name" : "Doe", "confirmation" : 12345}) ->
#     "Jane Doe's flight from San Jose to New Orleans departs at 12:30 PM tomorrow and lands at 9:30 PM."

chat_llm = ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()
instruct_llm = ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

external_chain = external_prompt | chat_llm

#############################################################################
# START : Define the extractor and internal chain to satisfy the objective

# Una cadena de operaciones que incluye las instrucciones de formato, el
# prompt, el modelo de lenguaje y la función de preprocesamiento
extractor = RExtract(KnowledgeBase, instruct_llm, parser_prompt)

# Make a chain that will populate your knowledge base based on provided context


def knowbase_getter(x):
    # crear un nuevo KnowledgeBase y mantener actualizado
    y = extractor.invoke(x)
    print(f"{y=}")
    return y

# Make a chain to pull d["know_base"] and outputs a retrieval from db


def database_getter(x):
    # print(f"{x=}, type(x)={type(x)}")
    # llamar a get_flight_info con los datos del usuario

    def get_key_fn(base: BaseModel) -> dict:
        '''Dado un diccionario con una base de conocimiento, devuelve una clave para get_flight_info'''
        return {  # Más opciones automáticas posibles, pero esto es más explícito
            'first_name': base.first_name,
            'last_name': base.last_name,
            'confirmation': base.confirmation,
        }

    know_base = x['know_base']

    print(repr(know_base))

    x = get_key_fn(know_base)
    print(f"{x=}")

    y = get_flight_info(x)
    return y


def get_flight_info(d: dict) -> str:
    pprint(f"{d=}")
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
            "12:31 PM", "9:31 PM", "mañana"],
        ["John", "Smith", 54321, "Nueva York", "Los Ángeles",
            "8:00 AM", "11:00 AM", "domingo"],
        ["Alice", "Johnson", 98765, "Chicago", "Miami",
            "7:00 PM", "11:00 PM", "la próxima semana"],
        ["Bob", "Brown", 56789, "Dallas", "Seattle",
            "1:00 PM", "4:00 PM", "ayer"],
    ]

    def get_key(d): return "|".join(
        [d['first_name'], d['last_name'], str(d['confirmation'])])

    def get_val(l): return {k: v for k, v in zip(keys, l)}
    db = {get_key(get_val(entry)): get_val(entry) for entry in values}

    # Search for the matching entry
    data = db.get(get_key(d))
    if not data:
        return (
            f"Basado en {req_keys} = {get_key(d)}) de tu base de conocimiento, no se encontró información sobre el vuelo del usuario."
            " Este proceso ocurre cada vez que se aprende nueva información. Si es importante, pídeles que confirmen esta información."
        )
    return (
        f"El vuelo de {data['first_name']} {data['last_name']} desde {data['departure']} a {data['destination']}"
        f" sale a las {data['departure_time']} {data['flight_day']} y llega a las {data['arrival_time']}."
    )


# These components integrate to make your internal chain
internal_chain = (
    RunnableAssign({'know_base': knowbase_getter})
    | RunnableAssign({'context': database_getter})
)

# END TODO
#############################################################################

state = {'know_base': KnowledgeBase()}


def chat_gen(message, history=[], return_buffer=True):

    # Pulling in, updating, and printing the state
    global state
    state['input'] = message
    state['history'] = history
    state['output'] = "" if not history else history[-1][1]

    # Generating the new state from the internal chain
    state = internal_chain.invoke(state)
    print("State after chain run:")
    pprint({k: v for k, v in state.items() if k != "history"})

    # Streaming the results
    buffer = ""
    for token in external_chain.stream(state):
        buffer += token
        yield buffer if return_buffer else token


def queue_fake_streaming_gradio(chat_stream, history=[], max_questions=8):

    # Mimic of the gradio initialization routine, where a set of starter messages can be printed off
    for human_msg, agent_msg in history:
        if human_msg:
            print("\n[ Human ]:", human_msg)
        if agent_msg:
            print("\n[ Agent ]:", agent_msg)

    # Mimic of the gradio loop with an initial message from the agent.
    for _ in range(max_questions):
        print(f"{_=}")
        message = input("\n[ Human ]: ")
        print("\n[ Agent ]: ")
        history_entry = [message, ""]
        for token in chat_stream(message, history, return_buffer=False):
            print(token, end='')
            history_entry[1] += token
        history += [history_entry]
        print("\n")


# history is of format [[User response 0, Bot response 0], ...]
chat_history = [
    [None, "Hola! Soy tu agente de SkyFlow. ¿Cómo puedo ayudarte?"]]

# Simulating the queueing of a streaming gradio interface, using python input
queue_fake_streaming_gradio(
    chat_stream=chat_gen,
    history=chat_history
)
