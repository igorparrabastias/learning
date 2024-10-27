import gradio as gr
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
from faiss import IndexFlatL2
import sys

# Console setup
console = Console()
base_style = Style(color="#76B900", bold=True)
norm_style = Style(bold=True)
pprint = partial(console.print, style=base_style)
pprint2 = partial(console.print, style=norm_style)

# Constants
DB_PATH = 'db'
EMBEDDING_MODEL = "text-embedding-3-small"
INSTRUCT_MODEL = "gpt-4o-mini"

INDEX_FILE = os.path.join(DB_PATH, "docstore_index")

# Embedder and LLM setup
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=512)
instruct_llm = ChatOpenAI(model=INSTRUCT_MODEL).bind(
    max_tokens=1024) | StrOutputParser()


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


def view_docstore(docstore):
    i = 0
    # for _, item in docstore.docstore._dict.items():
    #     pprint(f"{i=}: {item.page_content[:100]}")
    #     i += 1

    docs = list(docstore.docstore._dict.values())
    print(f"size: {len(docs)}")

    def format_chunk(doc):
        return (
            f"Paper: {doc.metadata.get('Title', 'unknown')}"
            f"\n\nSummary: {doc.metadata.get('Summary', 'unknown')}"
            f"\n\nPage Body: {doc.page_content}"
        )

    pprint(f"Constructed docstore with {len(docstore.docstore._dict)} chunks")
    for doc in docs:
        if doc.metadata:
            print(f"\ntitle: {doc.metadata.get('Title', 'unknown')}" +
                  f"\ncontent: {doc.page_content[:100]}")
    # print(format_chunk(docs[len(docs)//2]))
    # print(format_chunk(docs[0]))
    # print(format_chunk(docs[1]))
    # print(format_chunk(docs[2]))
    # print(format_chunk(docs[len(docs)-1]))


if os.path.exists(INDEX_FILE):
    pprint(f"FAISS index loading from {INDEX_FILE}")
    docstore = FAISS.load_local(
        INDEX_FILE, embedder, allow_dangerous_deserialization=True
    )
    # view_docstore(docstore)
else:
    pprint("No index file found, use load_arxiv_docs()")
    sys.exit()

# ############################################################
# Task 2: [Exercise] Pull In Your RAG Chain
#####################################################################


def docs2str(docs, title="Document"):
    """Useful utility for making chunks into context string. Optional, but useful"""
    out_str = ""
    for doc in docs:
        doc_name = getattr(doc, 'metadata', {}).get('Title', title)
        if doc_name:
            out_str += f"[Quote from {doc_name}] "
        out_str += getattr(doc, 'page_content', str(doc)) + "\n"
    return out_str


chat_prompt = ChatPromptTemplate.from_template(
    "You are a document chatbot. Help the user as they ask questions about documents."
    " User messaged just asked you a question: {input}\n\n"
    " The following information may be useful for your response: "
    " Document Retrieval:\n{context}\n\n"
    " (Answer only from retrieval. Only cite sources that are used. Make your response conversational)"
    "\n\nUser Question: {input}"
)


def output_puller(inputs):
    """
    Output generator. Useful if your chain returns a dictionary with key 'output'
    """
    if isinstance(inputs, dict):
        inputs = [inputs]
    for token in inputs:
        if token.get('output'):
            yield token.get('output')

#####################################################################
# TODO: Pull in your desired RAG Chain. Memory not necessary


# Chain 1 Specs: "Hello World" -> retrieval_chain
# -> {'input': <str>, 'context' : <str>}
long_reorder = RunnableLambda(
    LongContextReorder().transform_documents)  # GIVEN
context_getter = RunnableLambda(lambda x: x)  # TODO
retrieval_chain = {'input': (lambda x: x)} | RunnableAssign({
    'context': context_getter})

# Chain 2 Specs: retrieval_chain -> generator_chain
# -> {"output" : <str>, ...} -> output_puller
generator_chain = RunnableLambda(lambda x: x)  # TODO
generator_chain = {'output': generator_chain} | RunnableLambda(
    output_puller)  # GIVEN

# END TODO
#####################################################################

rag_chain = retrieval_chain | generator_chain

# pprint(rag_chain.invoke("Tell me something interesting!"))
for token in rag_chain.stream("Tell me something interesting!"):
    print(token, end="")
