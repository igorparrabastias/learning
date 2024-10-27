from langchain_core.runnables import RunnableLambda, RunnableAssign
from langchain_community.document_transformers import LongContextReorder
from langchain.chains import ConversationalRetrievalChain
import os
from functools import partial
from operator import itemgetter

from rich.console import Console
from rich.style import Style

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import OpenAIEmbeddings, ChatOpenAI

import pandas as pd

from faiss import IndexFlatL2

# Console setup
console = Console()
base_style = Style(color="#76B900", bold=True)
pprint = partial(console.print, style=base_style)

# Constants
DB_PATH = 'db'
EMBEDDING_MODEL = "text-embedding-3-small"
INSTRUCT_MODEL = "gpt-4o-mini"

INDEX_FILE = os.path.join(DB_PATH, "faiss_index")
VECTORSTORE_FILE = os.path.join(DB_PATH, "faiss_store.pkl")

# Embedder and LLM setup
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=512)
instruct_llm = ChatOpenAI(model=INSTRUCT_MODEL).bind(
    max_tokens=1024) | StrOutputParser()

embed_dims = len(embedder.embed_query("test111"))


def RPrint(preface=""):
    """
    Crea una cadena de ejecución que imprime un prefijo opcional seguido del contenido, y luego devuelve el contenido.
    Esta función es útil para imprimir información adicional antes de devolver el resultado de una operación.
    """
    def print_and_return(x, preface):
        """
        Imprime el prefijo especificado, si hay alguno, seguido del contenido x, y luego devuelve x.
        """
        if preface:
            print(preface, end="")
        # Utiliza pprint para imprimir el contenido x de manera formateada
        pprint(x)
        return x
    # Retorna una instancia de RunnableLambda que ejecuta la función print_and_return con el prefijo especificado
    return RunnableLambda(partial(print_and_return, preface=preface))


def default_FAISS():
    '''Useful utility for making an empty FAISS vectorstore'''
    return FAISS(
        # Define la función de embedding que se utilizará para convertir textos en vectores.
        embedding_function=embedder,

        # Crea un índice FAISS utilizando el algoritmo IndexFlatL2, que es un índice plano que utiliza la distancia L2 (euclidiana).
        index=IndexFlatL2(embed_dims),

        # Define un almacén de documentos en memoria para almacenar los documentos asociados a los vectores.
        docstore=InMemoryDocstore(),

        # Un diccionario que mapea los IDs del índice a los IDs del almacén de documentos.
        index_to_docstore_id={},

        # Indica si se debe normalizar los vectores a longitud 1 (L2 normalización). Aquí está desactivado.
        normalize_L2=False
    )


def view_docstore(docstore):

    all_docs = []
    i = 0
    for key, item in docstore.docstore._dict.items():
        all_docs.append(item.page_content)
        pprint(f"{i=}: {item.page_content[:100]}")
        i += 1
        # docs = new_db.similarity_search("Testing the index")
        # print(docs[0].page_content[:1000])


# - Una forma de construir un vector store desde cero para la memoria conversacional (y una forma de inicializar uno vacío con `default_FAISS()`)
convstore = default_FAISS()

INDEX_FILE = os.path.join(DB_PATH, "docstore_index")

if os.path.exists(INDEX_FILE):
    pprint(f"FAISS index loading from {INDEX_FILE}")

    docstore = FAISS.load_local(
        INDEX_FILE, embedder, allow_dangerous_deserialization=True
    )

    pprint(
        f"Number of vectors in the vector store: {len(docstore.docstore._dict)}")

    view_docstore(docstore)
else:
    pprint("No index file found, use load_arxiv_docs()")


def save_memory_and_get_output(d, vstore):
    """Acepta un diccionario 'input'/'output' y guarda en convstore"""
    vstore.add_texts([
        f"El usuario respondió previamente con {d.get('input')}",
        f"El agente respondió previamente con {d.get('output')}"
    ])
    return d.get('output')


doc_string = ''

initial_msg = (
    "¡Hola! Soy un agente de chat de documentos aquí para ayudar al usuario!"
    f" Tengo acceso a los siguientes documentos: {doc_string}\n\n¿Cómo puedo ayudarte?"
)

chat_prompt = ChatPromptTemplate.from_messages([(
    "system",
    "Eres un chatbot de documentos. Ayuda al usuario a medida que hacen preguntas sobre documentos."
    " El usuario acaba de preguntar: {input}\n\n"
    " A partir de esto, hemos recuperado la siguiente información potencialmente útil: "
    " Recuperación del Historial de Conversación:\n{history}\n\n"
    " Recuperación del Documento:\n{context}\n\n"
    " (Responde solo desde la recuperación. Cita solo las fuentes que se utilizan. Haz que tu respuesta sea conversacional.)"
), ('user', '{input}')])

stream_chain = chat_prompt | RPrint() | instruct_llm | StrOutputParser()


def docs2str(docs, title="Document"):
    """Useful utility for making chunks into context string. Optional, but useful"""
    out_str = ""
    for doc in docs:
        doc_name = getattr(doc, 'metadata', {}).get('Title', title)
        if doc_name:
            out_str += f"[Quote from {doc_name}] "
        out_str += getattr(doc, 'page_content', str(doc)) + "\n"
    return out_str


# El componente `LongContextReorder` de LangChain es un transformador de documentos diseñado para abordar un problema específico llamado "lost-in-the-middle" (perdido en el medio). Este problema se refiere a la tendencia de los modelos de lenguaje a tener dificultades para priorizar información que se encuentra en la parte media de una secuencia larga de texto. Investigaciones han demostrado que los modelos suelen obtener un mejor rendimiento cuando la información clave se coloca al inicio o al final de un contexto, ya que tienden a perder detalles importantes si están en el centro de un texto largo.
# Para solucionar esto, `LongContextReorder` reorganiza los documentos recuperados colocando los más relevantes al principio y al final, dejando los menos relevantes en el medio. Esta técnica es útil cuando se manejan grandes cantidades de documentos en un pipeline de generación aumentada por recuperación(RAG), como cuando hay más de 10 documentos relevantes. El objetivo es mejorar la precisión y el rendimiento del modelo de lenguaje.
# En el código, cuando usas `RunnableLambda(LongContextReorder().transform_documents)`, encapsulas la lógica de reordenamiento de documentos en un componente modular ejecutable, lo que permite integrarlo en un flujo de trabajo mayor. La función `transform_documents` maneja esta lógica reorganizando los documentos de manera estratégica, alternando los documentos para optimizar su ubicación dentro del contexto del modelo de lenguaje【8†source】【9†source】【11†source】.
long_reorder = RunnableLambda(LongContextReorder().transform_documents)

################################################################################
# BEGIN TODO: Implement the retrieval chain to make your system work!
retrieval_chain = (
    {'input': (lambda x: x)}
    # | RunnableAssign({
    #     'history': lambda d: convstore.similarity_search(d['input'], k=3),
    #     'context': lambda d: docstore.similarity_search(d['input'], k=3)
    # })
    # | RunnableAssign({
    #     'history': lambda d: LongContextReorder().transform_documents(d['history']),
    #     'context': lambda d: LongContextReorder().transform_documents(d['context'])
    # })
    # | RunnableAssign({
    #     'history': lambda d: '\n'.join([doc.page_content for doc in d['history']]),
    #     'context': lambda d: '\n'.join([doc.page_content for doc in d['context']])
    # })
    | RunnableAssign({'history': itemgetter('input') | convstore.as_retriever() | long_reorder | docs2str})
    | RunnableAssign({'context': itemgetter('input') | docstore.as_retriever() | long_reorder | docs2str})
    | RPrint()
)

# END TODO
################################################################################


def chat_gen(message, history=[], return_buffer=True):
    buffer = ""
    # First perform the retrieval based on the input message
    retrieval = retrieval_chain.invoke(message)
    line_buffer = ""

    # Then, stream the results of the stream_chain
    for token in stream_chain.stream(retrieval):
        buffer += token
        # If you're using standard print, keep line from getting too long
        yield buffer if return_buffer else token

    # Lastly, save the chat exchange to the conversation memory buffer
    save_memory_and_get_output(
        {'input':  message, 'output': buffer}, convstore)


def main():
    # Start of Agent Event Loop
    test_question = "Tell me about RAG!"  # <- modify as desired
    print(f"{test_question=}")

    # Before you launch your gradio interface, make sure your thing works
    for response in chat_gen(test_question, return_buffer=False):
        print(response, end='')


# main()
