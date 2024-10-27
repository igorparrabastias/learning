from langchain.chains import ConversationalRetrievalChain
import shutil
import os
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from operator import itemgetter
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
import gradio as gr

from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from langchain_community.document_transformers import LongContextReorder
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

from langchain.schema.runnable import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableAssign
from langchain_core.runnables.passthrough import RunnableAssign

from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ArxivLoader

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

conversation = [  # Esta conversación fue generada parcialmente por un sistema de IA, y modificada para exhibir propiedades deseables
    "[User]  ¡Hola! Mi nombre es Beras, y soy un gran oso azul! ¿Podrías decirme sobre las montañas rocosas?",
    "[Agent] Las Montañas Rocosas son una hermosa y majestuosa cadena de montañas que se extienden a través de Norteamérica",
    "[Beras] ¡Guau, eso suena increíble! Nunca he estado en las Montañas Rocosas antes, pero he escuchado muchas cosas buenas sobre ellas.",
    "[Agent] Espero que puedas visitarlas algún día, Beras! Sería una gran aventura para ti!"
    "[Beras] ¡Gracias por la sugerencia! Definitivamente la tendré en cuenta para el futuro.",
    "[Agent] Mientras tanto, puedes aprender más sobre las Montañas Rocosas haciendo algunas investigaciones en línea o viendo documentales sobre ellas."
    "[Beras] Vivo en el ártico, así que no estoy acostumbrado al clima cálido allí. Solo estaba curioso, ¡ya sabes!",
    "[Agent] ¡Absolutamente! ¡Vamos a continuar la conversación y explorar más sobre las Montañas Rocosas y su significado!"
]


# Ensure the database directory exists
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)


def save_faiss(convstore):
    """
    Function to save FAISS index and metadata
    """
    convstore.save_local(INDEX_FILE)


def load_faiss(INDEX_FILE):
    return FAISS.load_local(INDEX_FILE, embedder, allow_dangerous_deserialization=True)


def manage_faiss_index(INDEX_FILE, conversation):
    """
    Manage the loading or creation of a FAISS index based on the existence of INDEX_FILE.

    Parameters:
    - INDEX_FILE: Path to the FAISS index file.
    - conversation: List of texts to index if the FAISS index doesn't exist.
    - embedder: Embedding function or model for FAISS indexing.
    - load_faiss: Function to load the existing FAISS index.
    - save_faiss: Function to save the newly created FAISS index.
    """
    if os.path.exists(INDEX_FILE):
        convstore = load_faiss(INDEX_FILE)
        pprint("FAISS index loaded")
    else:
        print("Creating FAISS index from conversation texts")
        convstore = FAISS.from_texts(conversation, embedding=embedder)
        save_faiss(convstore)

    return convstore


def reset_faiss_store(INDEX_FILE):
    if os.path.exists(INDEX_FILE):
        if os.path.isfile(INDEX_FILE):
            os.remove(INDEX_FILE)
        elif os.path.isdir(INDEX_FILE):
            shutil.rmtree(INDEX_FILE)


########################################################################
# Utility Runnables/Methods


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


def docs2str(docs, title="Document"):
    """Useful utility for making chunks into context string. Optional, but useful"""
    out_str = ""
    for doc in docs:
        doc_name = getattr(doc, 'metadata', {}).get('Title', title)
        if doc_name:
            out_str += f"[Quote from {doc_name}] "
        out_str += getattr(doc, 'page_content', str(doc)) + "\n"
    return out_str


########################################################################
# Incorporating Conversation Retrieval Into Our Chain

# Optional; Reorders longer documents to center of output text
long_reorder = RunnableLambda(LongContextReorder().transform_documents)

context_prompt = ChatPromptTemplate.from_template(
    "Responde a la pregunta solo usando el contexto"
    "\n\nContexto Recuperado: {context}"
    "\n\nPregunta del Usuario: {question}"
    "\nResponde al usuario de manera conversacional. El usuario no está al tanto del contexto."
)


def chain_with_retriever():
    """
    Cadena de procesamiento de preguntas:
    Función chain_with_retriever: La cadena principal tiene varios componentes conectados mediante operaciones de RunnableLambda.
    Primero, se imprime la pregunta.
    Luego, se obtiene el contexto utilizando un retriever(que se apoya en el índice FAISS) y se aplica una reorganización opcional para documentos largos(LongContextReorder).
    El contexto y la pregunta se alimentan a un modelo ChatPromptTemplate, que formatea la pregunta y el contexto.
    Finalmente, se imprime el resultado y se pasa al LLM para generar una respuesta.
    """

    # Get the retriever from the loaded FAISS store
    retriever = convstore.as_retriever()
    chain = (
        RPrint('\npregunta: ') |
        {
            'context': convstore.as_retriever() | long_reorder | docs2str,
            'question': (lambda x: x)
        }
        | context_prompt
        | RPrint()
        | instruct_llm
        | StrOutputParser()
    )

    pprint(chain.invoke("¿Dónde vive Beras?"))
    pprint(retriever.invoke("¿Dónde están las Montañas Rocosas?"))
    pprint(chain.invoke(
        "¿Dónde están las Montañas Rocosas? ¿Están cerca de California?"))
    pprint(chain.invoke("¿Cuánto está Beras de las Montañas Rocosas?"))


def save_memory_and_get_output(d, vstore):
    """Accepts 'input'/'output' dictionary and saves to convstore"""
    vstore.add_texts(
        [f"El usuario dijo {d.get('input')}", f"El agente dijo {d.get('output')}"])
    return d.get('output')


def automatic_conversation_storage():
    """
    Cadena para almacenamiento automático de la conversación:
    Función automatic_conversation_storage: Define una cadena similar a chain_with_retriever, pero incluye una operación adicional de almacenamiento que guarda las entradas y salidas de la conversación en el vector store FAISS. De esta manera, la conversación se enriquece automáticamente con cada nueva interacción.
    """

    reset_faiss_store()

    chat_prompt = ChatPromptTemplate.from_template(
        "Responde a la pregunta solo usando el contexto"
        "\n\nContexto Recuperado: {context}"
        "\n\nPregunta del Usuario: {input}"
        "\nResponde al usuario de manera conversacional. Asegúrate de que la conversación fluya naturalmente.\n"
        "[Agent]"
    )

    # Esta cadena de procesamiento se encarga de manejar la conversación, incluyendo el almacenamiento automático de las interacciones.
    conv_chain = (
        # Primero, se definen dos variables: 'context' y 'input'. 'context' se llena con el contexto recuperado del vector store FAISS,
        # aplicando una reordenación opcional para documentos largos y convertir los documentos en una cadena de texto. 'input' simplemente
        # toma el input del usuario sin modificación.
        {
            'context': convstore.as_retriever() | long_reorder | docs2szstr,
            'input': (lambda x: x)
        }
        # | RPrint()
        # Luego, se asigna el valor de 'output' basado en el contexto y el input del usuario. Esto se logra mediante una plantilla de
        # conversación que combina el contexto y el input, y luego se pasa a un modelo de lenguaje para generar una respuesta. La respuesta
        # se parsea a una cadena de texto para su uso posterior.
        | RunnableAssign({'output': chat_prompt | instruct_llm | StrOutputParser()})
        # Finalmente, se llama a una función que guarda el input del usuario y el output del agente en el vector store FAISS, lo que
        # permite el almacenamiento automático de la conversación. La función devuelve el output del agente.
        | partial(save_memory_and_get_output, vstore=convstore)
    )

    pprint(conv_chain.invoke(
        "¡Me alegra que estés de acuerdo! ¡No puedo esperar para probar helado allí! ¡Es un alimento tan bueno!"))
    print()
    pprint(conv_chain.invoke("¿Puedes adivinar cuál es mi comida favorita?"))
    print()
    pprint(conv_chain.invoke(
        "En realidad, mi favorita es la miel! ¡No estoy seguro de dónde sacaste esa idea?"))
    print()
    pprint(conv_chain.invoke(
        "¡Veo! ¡Bueno, es justo! ¿Sabes cuál es mi comida favorita ahora?"))


embed_dims = len(embedder.embed_query("test111"))


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


def aggregate_vstores(vectorstores):
    # Inicializa un índice FAISS vacío utilizando la función default_FAISS.
    # Esta función está configurada para usar el embedder que has definido previamente.
    agg_vstore = default_FAISS()

    # Itera sobre cada vector store en la lista vectorstores.
    for vstore in vectorstores:
        # Fusiona el vector store actual en el índice FAISS agregado (agg_vstore).
        # Esto combina los datos de múltiples vector stores en uno solo.
        agg_vstore.merge_from(vstore)

    # Devuelve el índice FAISS combinado que ahora contiene datos de todos los vector stores.
    return agg_vstore


def load_arxiv_docs():
    INDEX_FILE = os.path.join(DB_PATH, "arxiv_index")

    if os.path.exists(INDEX_FILE):
        pprint(f"FAISS index loading from {INDEX_FILE}")

        docstore = FAISS.load_local(
            INDEX_FILE, embedder, allow_dangerous_deserialization=True
        )

        pprint(
            f"Number of vectors in the vector store: {len(docstore.docstore._dict)}")

        # docs = docstore.similarity_search("holon")
        # pprint(docs[0])

        # # Genera un vector de características para la consulta
        # vector = embedder.embed_query("holon")
        # # Busca documentos similares al vector generado
        # results = docstore.similarity_search_by_vector(vector)
        # pprint("similarity_search_by_vector",       results[0])

        # # Busca documentos similares al vector generado con un enfoque en la relevancia marginal máxima
        # results = docstore.max_marginal_relevance_search(
        #     "holon", k=5, lambda_mult=0.5)
        # pprint("max_marginal_relevance_search", results)

        # Convierte el vector store en un retriever
        retriever = docstore.as_retriever()
        # results = retriever.invoke("holon")
        # pprint(results)

        # Crear una cadena de preguntas y respuestas conversacional
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=instruct_llm, retriever=retriever)

        # Consulta dentro del flujo de la cadena
        response = qa_chain.invoke({
            "question": "Explain the concept of holon",
            "chat_history": []
        })

        print("Explain the concept of holon", response["answer"])

    else:

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100,
            separators=["\n\n", "\n", ".", ";", ",", " "],
        )

        print("Loading Documents")
        docs = [
            # Attention Is All You Need Paper
            ArxivLoader(query="1706.03762").load(),
            ArxivLoader(query="1810.04805").load(),  # BERT Paper
            ArxivLoader(query="2005.11401").load(),  # RAG Paper
            ArxivLoader(query="2205.00445").load(),  # MRKL Paper
            ArxivLoader(query="2310.06825").load(),  # Mistral Paper
            ArxivLoader(query="2306.05685").load(),  # LLM-as-a-Judge

            # Some longer papers
            # Tratar usar< 1 month old
            # Holon Programming Model -- A Software-Defined Approach for System of Systems
            ArxivLoader(query="2410.17784").load(),
        ]

        # Cut the paper short if references is included.
        # This is a standard string in papers.
        for doc in docs:
            content = json.dumps(doc[0].page_content)
            if "References" in content:
                doc[0].page_content = content[:content.index("References")]

        # Split the documents and also filter out stubs (overly short chunks)
        print("Chunking Documents")
        docs_chunks = [text_splitter.split_documents(doc) for doc in docs]
        docs_chunks = [[c for c in dchunks if len(
            c.page_content) > 200] for dchunks in docs_chunks]

        # Make some custom Chunks to give big-picture details
        doc_string = "Available Documents:"
        doc_metadata = []
        for chunks in docs_chunks:
            metadata = getattr(chunks[0], 'metadata', {})
            doc_string += "\n - " + metadata.get('Title')
            doc_metadata += [str(metadata)]

        extra_chunks = [doc_string] + doc_metadata

        # Printing out some summary information for reference
        pprint(doc_string, '\n')
        for i, chunks in enumerate(docs_chunks):
            print(f"Document {i}")
            print(f" - # Chunks: {len(chunks)}")
            print(f" - Metadata: ")
            pprint(chunks[0].metadata)
            print()

        print("Constructing Vector Stores")
        vecstores = [FAISS.from_texts(extra_chunks, embedder)]
        vecstores += [FAISS.from_documents(doc_chunks, embedder)
                      for doc_chunks in docs_chunks]

        # Unintuitive optimization; merge_from seems to optimize constituent vector stores away
        docstore = aggregate_vstores(vecstores)

        print(f"Creating FAISS index from arxiv documents in {INDEX_FILE}")
        docstore.save_local(INDEX_FILE)

        print(
            f"Constructed aggregate docstore with {len(docstore.docstore._dict)} chunks")
