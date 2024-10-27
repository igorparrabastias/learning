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
    for _, item in docstore.docstore._dict.items():
        pprint(f"{i=}: {item.page_content[:100]}")
        i += 1


if os.path.exists(INDEX_FILE):
    pprint(f"FAISS index loading from {INDEX_FILE}")
    docstore = FAISS.load_local(
        INDEX_FILE, embedder, allow_dangerous_deserialization=True
    )
    pprint(f"Vectors in the vector store: {len(docstore.docstore._dict)}")
    view_docstore(docstore)
else:
    pprint("No index file found, use load_arxiv_docs()")
    sys.exit()
