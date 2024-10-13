from copy import deepcopy
from operator import itemgetter
import gradio as gr
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from functools import partial
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_nvidia_ai_endpoints import ChatNVIDIA


def print_and_return(x, preface=""):
    print(f"{preface}{x}")
    return x


log = RunnableLambda(partial(print_and_return, preface="log: "))


def runnable():
    identity = RunnableLambda(lambda x: x)  # Or RunnablePassthrough works

    # Given an arbitrary function, you can make a runnable with it

    rprint0 = RunnableLambda(print_and_return)

    ################################################################################
    # You can also pre-fill some of values using functools.partial
    rprint1 = RunnableLambda(partial(print_and_return, preface="1: "))

    ################################################################################
    # And you can use the same idea to make your own custom Runnable generator

    def RPrint(preface=""):
        return RunnableLambda(partial(print_and_return, preface=preface))

    ################################################################################
    # Chaining two runnables
    chain1 = identity | rprint0
    chain1.invoke("Hello World!")
    print()

    ################################################################################
    # Chaining that one in as well
    output = (
        chain1  # Prints "Welcome Home!" & passes "Welcome Home!" onward
        | rprint1  # Prints "1: Welcome Home!" & passes "Welcome Home!" onward
        # Prints "2: Welcome Home!" & passes "Welcome Home!" onward
        | RPrint("2: ")
    ).invoke("Welcome Home!")

    # Final Output Is Preserved As "Welcome Home!"
    print("\nOutput:", output)


def rhymes():
    # Simple Chat Pipeline
    chat_llm = ChatNVIDIA(model="meta/llama3-8b-instruct")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Only respond in rhymes"),
        ("user", "{input}")
    ])

    rhyme_chain = prompt | chat_llm | StrOutputParser()

    print(rhyme_chain.invoke({"input": "Tell me about birds!"}))


def gradio():
    # Simple Chat Pipeline
    chat_llm = ChatNVIDIA(model="meta/llama3-8b-instruct")

    prompt = ChatPromptTemplate.from_messages([
        # ("system", "solo responde en rimas"),
        ("system", "solo responde como cientifico social"),
        # ("system", "Solo responde en lenguaje técnico informatico. Sé simpre
        # conciso a menos que te pida explayarte"),
        ("user", "{input}")
    ])

    rhyme_chain = prompt | chat_llm | StrOutputParser()

    # Non-streaming
    # Interface like that shown above

    # def rhyme_chat(message, history): return rhyme_chain.invoke({"input" :
    #     message})

    # gr.ChatInterface(rhyme_chat).launch()

    # Streaming Interface

    def rhyme_chat_stream(message, history):
        # This is a generator function, where each call will yield the next
        # entry
        buffer = ""
        for token in rhyme_chain.stream({"input": message}):
            buffer += token
            yield buffer

    # Uncomment when you're ready to try this.
    iface = gr.ChatInterface(rhyme_chat_stream).queue()
    window_kwargs = {}  # or {"server_name": "0.0.0.0", "root_path": "/7860/"}
    iface.launch(share=False, debug=True, **window_kwargs)


def inner_answer():
    # TODO: Try out some more models and see if there are better options
    instruct_llm = ChatNVIDIA(model="mistralai/mistral-7b-instruct-v0.2")

    sys_msg = (
        "Choose the most likely topic classification given the sentence as context."
        " Only one word, no explanation.\n[Options : {options}]"
    )

    # One-shot classification prompt with heavy format assumptions.
    zsc_prompt = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        ("user", "[[The sea is awesome]]"),
        ("assistant", "boat"),
        ("user", "[[{input}]]"),
    ])

    # Roughly equivalent as above for <s>[INST]instruction[/INST]response</s>
    # format zsc_prompt = ChatPromptTemplate.from_template( f"{sys_msg}\n\n"
    #     "[[The sea is awesome]][/INST]boat</s><s>[INST]" "[[{input}]]" )

    zsc_chain = zsc_prompt | instruct_llm | StrOutputParser()

    def zsc_call(input, options=["car", "boat", "airplane", "bike"]):
        return zsc_chain.invoke({"input": input, "options": options}).split()[0]

    print("-" * 80)
    print(zsc_call("Should I take the next exit, or keep going to the next one?"))

    print("-" * 80)
    print(zsc_call("I get seasick, so I think I'll pass on the trip"))

    print("-" * 80)
    print(zsc_call("I'm scared of heights, so flying probably isn't for me"))


def chain_multi_components():

    ################################################################################
    # Example of dictionary enforcement methods
    def make_dictionary(v, key):
        if isinstance(v, dict):
            return v
        return {key: v}

    def RInput(key='input'):
        '''Coercing method to mold a value (i.e. string) to in-like dict'''
        return RunnableLambda(partial(make_dictionary, key=key))

    def ROutput(key='output'):
        '''Coercing method to mold a value (i.e. string) to out-like dict'''
        return RunnableLambda(partial(make_dictionary, key=key))

    def RPrint(preface=""):
        return RunnableLambda(partial(print_and_return, preface=preface))

    ################################################################################
    # Common LCEL utility for pulling values from dictionaries

    up_and_down = (
        RPrint("A: ")
        # Custom ensure-dictionary process
        | RInput()
        | RPrint("B: ")
        # Pull-values-from-dictionary utility
        | itemgetter("input")
        | RPrint("C: ")
        # Anything-in Dictionary-out implicit map
        | {
            'word1': (lambda x: x.split()[0]),
            'word2': (lambda x: x.split()[1]),
            'words': (lambda x: x),  # <- == to RunnablePassthrough()
        }
        | RPrint("D: ")
        | itemgetter("word1")
        | RPrint("E: ")
        # Anything-in anything-out lambda application
        | RunnableLambda(lambda x: x.upper())
        | RPrint("F: ")
        # Custom ensure-dictionary process
        | ROutput()
    )

    up_and_down.invoke({"input": "Hello World"})

    """
    Este fragmento de código utiliza varias funcionalidades de LangChain (como
    `RunnableLambda` y `RunnablePassthrough`) para manejar flujos de
    procesamiento de datos, específicamente para transformar y manipular
    diccionarios y cadenas. Aquí te explico algunos puntos clave del código y
    cómo se relacionan con Python y LangChain:

    ### 1. **`RunnableLambda` y `partial`** - `RunnableLambda` es una clase de
    LangChain que encapsula una función para que sea parte de una cadena de
    procesamiento ("pipeline"). Se utiliza para aplicar transformaciones
    específicas a los datos que pasan por la cadena. - `partial` es una función
    de Python (del módulo `functools`) que te permite crear una nueva función
    pre-rellenando algunos de los argumentos de la función original. En este
    caso, `partial` se usa para especificar el valor del argumento `key` en
    `make_dictionary`. - Por ejemplo, en `RInput()`, `partial` crea una versión
    de `make_dictionary` que siempre pasará `key='input'`, mientras que en
    `ROutput()` el valor será `key='output'`.

    ### 2. **Uso de `itemgetter` y funciones Lambda** - `itemgetter` (del módulo
    `operator`) es una utilidad que extrae valores de diccionarios. En este
    caso, se usa para acceder al valor de la clave `"input"` y más tarde para
    obtener `"word1"`. Al combinarlo con las funciones Lambda, es posible
    dividir la cadena en palabras y realizar transformaciones específicas (como
    convertir a mayúsculas). - Las funciones Lambda en el código (e.g. `lambda
    x: x.split()[0]`) permiten realizar operaciones in-line sobre las cadenas,
    extrayendo palabras individuales o modificando el texto.

    ### 3. **Flujo de procesamiento y coerción de diccionarios** - Este código
    ilustra un flujo de procesamiento encadenado, donde el valor inicial
    (`{"input": "Hello World"}`) es transformado paso a paso. Primero, se
    imprime, luego se convierte en un diccionario si no lo es (`RInput()`), se
    extraen palabras con `itemgetter`, y finalmente se convierten a mayúsculas.
    - `RunnablePassthrough` se menciona de manera implícita en la parte donde no
    hay una transformación explícita, lo que significa que los datos simplemente
    pasan a la siguiente etapa.

    Este flujo encadenado permite manejar datos de forma flexible y modular,
    aprovechando tanto las características de LangChain como funciones nativas
    de Python.
    """
    None


def rhyme_re_themer():
    """
    A continuación se muestra un ejemplo de generación de poesía que muestra
    cómo se pueden organizar dos tareas diferentes bajo la apariencia de un solo
    agente. El sistema vuelve al ejemplo simple de Gradio, pero lo amplía con
    algunas respuestas estándar y lógica detrás de escena.
    """

    # Feel free to change the models
    instruct_llm = ChatNVIDIA(
        model="mistralai/mixtral-8x22b-instruct-v0.1", max_tokens=200)

    prompt1 = ChatPromptTemplate.from_messages([("user", (
        "INSTRUCTION: Solo responde en rimas en español"
        "\n\nPROMPT: {input}"
    ))])

    prompt2 = ChatPromptTemplate.from_messages([("user", (
        "INSTRUCTION: Solo responde en rimas en español. Change the topic of the input poem to be about {topic}!"
        " Make it happy! Try to keep the same sentence structure, but make sure it's easy to recite!"
        " Try not to rhyme a word with itself."
        "\n\nOriginal Poem: {input}"
        "\n\nNew Topic: {topic}"
    ))])

    # These are the main chains, constructed here as modules of functionality.
    chain1 = prompt1 | instruct_llm | StrOutputParser()  # only expects input
    # expects both input and topic
    chain2 = prompt2 | instruct_llm | StrOutputParser()

    ################################################################################

    def rhyme_chat2_stream(message, history, return_buffer=True):
        '''This is a generator function, where each call will yield the next
        entry'''

        print(f"{history=}")

        first_poem = None

        for entry in history:
            if entry[0] and entry[1]:
                # If a generation occurred as a direct result of a user input,
                # keep that response (the first poem generated) and break out
                first_poem = "\n\n".join(entry[1].split("\n\n")[1:-1])
                break

        if first_poem is None:
            # First Case: There is no initial poem generated. Better make one
            # up!

            buffer = "Oh! I can make a wonderful poem about that! Let me think!\n\n"
            yield buffer

            # iterate over stream generator for first generation
            inst_out = ""
            chat_gen = chain1.stream({"input": message})
            for token in chat_gen:
                inst_out += token
                buffer += token
                yield buffer if return_buffer else token

            passage = "\n\nNow let me rewrite it with a different focus! What should the new focus be?"
            buffer += passage
            yield buffer if return_buffer else passage

        else:
            # Subsequent Cases: There is a poem to start with. Generate a
            # similar one with a new topic!

            # yield f"Not Implemented!!!" return  # <- TODO: Comment this out

            ########################################################################
            # TODO: Invoke the second chain to generate the new rhymes.

            buffer = f"Sure! Here you go!\n\n"  # <- TODO: Uncomment these lines
            yield buffer

            # iterate over stream generator for second generation
            chat_gen = chain2.stream({"input": first_poem, "topic": message})
            for token in chat_gen:
                buffer += token
                yield buffer if return_buffer else token

            # END TODO
            ########################################################################

            passage = "\n\nThis is fun! Give me another topic!"
            buffer += passage
            yield buffer if return_buffer else passage

    ################################################################################
    # Below: This is a small-scale simulation of the gradio routine.

    def queue_fake_streaming_gradio(chat_stream, history=[], max_questions=3):

        # Mimic of the gradio initialization routine, where a set of starter
        # messages can be printed off
        for human_msg, agent_msg in history:
            if human_msg:
                print("\n[ Human 1 ]:", human_msg)
            if agent_msg:
                print("\n[ Agent 1 ]:", agent_msg)

        # Mimic of the gradio loop with an initial message from the agent.
        for _ in range(max_questions):
            message = input("\n[ Human 2 ]: ")
            print("\n[ Agent 2 ]: ")
            history_entry = [message, ""]
            for token in chat_stream(message, history, return_buffer=False):
                print(token, end='')
                history_entry[1] += token
            history += [history_entry]
            print("\n")

    # history is of format [[User response 0, Bot response 0], ...]
    history = [
        [None, "Let me help you make a poem! What would you like for me to write?"]]

    # Simulating the queueing of a streaming gradio interface, using python
    # input queue_fake_streaming_gradio( chat_stream=rhyme_chat2_stream,
    #     history=history )

    # Simple way to initialize history for the ChatInterface El componente
    # gr.Chatbot guarda el historial de la conversación en una lista de pares,
    # donde cada par representa un intercambio entre el usuario y el bot, por
    # ejemplo: [[mensaje_usuario1, respuesta_bot1], [mensaje_usuario2,
    # respuesta_bot2]]. El valor predeterminado de value es una lista de pares,
    # donde cada par contiene dos elementos: el mensaje del usuario y el mensaje
    # del bot.
    chatbot = gr.Chatbot(
        value=[[None, "Escritor de poemas"]])

    # Gradio pasa automáticamente el historial al rhyme_chat2_stream. En Gradio,
    # cuando el usuario interactúa con el chatbot, cada nuevo mensaje se agrega
    # al historial de la conversación. Este historial de mensajes se pasa como
    # un argumento a la función que maneja la lógica de generación de
    # respuestas, en este caso, rhyme_chat2_stream. El parámetro history en
    # rhyme_chat2_stream corresponde al historial del chatbot, que incluye tanto
    # los mensajes iniciales definidos por value como los intercambios
    # posteriores generados por el usuario y el bot.

    # Gradio pasa automáticamente el historial del chatbot a la función que
    # maneja las respuestas(en este caso, rhyme_chat2_stream) para que puedas
    # acceder a los mensajes previos. Esto permite que tu función utilice el
    # contexto de la conversación y mantenga la coherencia en las interacciones
    # posteriores. El value de gr.Chatbot se usa para inicializar este
    # historial, y luego se va actualizando con cada nuevo intercambio de
    # mensajes.
    gr.ChatInterface(rhyme_chat2_stream, chatbot=chatbot, title="Poem Maker").queue().launch(
        debug=True, share=False, height=700)


def deep_integration():

    from langserve import RemoteRunnable
    from langchain_core.output_parsers import StrOutputParser
    from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings

    llm = RemoteRunnable("http://0.0.0.0:9012/basic_chat/") | StrOutputParser()
    for token in llm.stream("Soy un terminator modelo T800"):
        print(token, end='')

    # # Equivalent to the following, assuming you're using the same model
    # llm = ChatNVIDIA(model="meta/llama-3.1-8b-instruct") | StrOutputParser()
    # for token in llm.stream("Hello World! How is it going?"):
    #     print(token, end='')
