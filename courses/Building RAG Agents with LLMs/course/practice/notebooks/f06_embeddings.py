import os
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from operator import itemgetter
from pydantic import BaseModel
from rich.console import Console
from rich.style import Style
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Console setup
console = Console()
base_style = Style(color="#76B900", bold=True)
pprint = partial(console.print, style=base_style)

# Constants
DB_PATH = 'db'
QUERY_FILE = os.path.join(DB_PATH, 'query_embeddings.json')
DOC_FILE = os.path.join(DB_PATH, 'document_embeddings.json')
LONG_DOC_FILE = os.path.join(DB_PATH, 'longer_docs.json')
EMBEDDING_MODEL = "text-embedding-3-small"
INSTRUCT_MODEL = "gpt-4o-mini"

# Embedder and LLM setup
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=512)
instruct_llm = ChatOpenAI(model=INSTRUCT_MODEL).bind(
    max_tokens=1024) | StrOutputParser()

# Example data
queries = [
    "¿Cuál es el clima en las Montañas Rocosas?",
    "¿Qué tipos de comida es famosa Italia?",
    "¿Cuál es mi nombre? Apuesto a que no te acuerdas...",
    "¿Cuál es el punto de la vida de todas maneras?",
    "El punto de la vida es divertirse :D"
]

documents = [
    "El clima de Komchatka es frío, con largos e intensos inviernos.",
    "Italia es famosa por la pasta, la pizza, el gelato y el espresso.",
    "No puedo recordar nombres personales, solo proporciono información.",
    "El propósito de la vida varía, a menudo visto como la realización personal.",
    "Disfrutar los momentos de la vida es en verdad un enfoque maravilloso.",
]

# Utility functions


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_embeddings():
    with open(QUERY_FILE, 'r') as qf, open(DOC_FILE, 'r') as df:
        return json.load(qf), json.load(df)


def save_embeddings(q_embeddings, d_embeddings):
    ensure_dir(DB_PATH)
    with open(QUERY_FILE, 'w') as qf, open(DOC_FILE, 'w') as df:
        json.dump(q_embeddings, qf)
        json.dump(d_embeddings, df)


def generate_embeddings(docs, is_query=True):
    return [embedder.embed_query(doc) if is_query else embedder.embed_documents([doc])[0] for doc in docs]


def plot_similarity_matrix(emb1, emb2, title):
    matrix = cosine_similarity(np.array(emb1), np.array(emb2))
    plt.imshow(matrix, cmap='Greens', interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.grid(True)


# Main code
if os.path.exists(QUERY_FILE) and os.path.exists(DOC_FILE):
    q_embeddings, d_embeddings = load_embeddings()
    pprint("Embeddings loaded from file")
else:
    q_embeddings = generate_embeddings(queries)
    d_embeddings = generate_embeddings(documents, is_query=False)
    save_embeddings(q_embeddings, d_embeddings)
    pprint("Generated and saved embeddings")

# Document expansion chain
expound_prompt = ChatPromptTemplate.from_template(
    "Genera parte de una historia más larga que podría razonablemente responder todas"
    " estas preguntas en algún lugar de su contenido: {questions}\n"
    " Asegúrate de que el pasaje solo responde concretamente a la siguiente: {q1}."
    " Dale un formato extraño, y trata de no responder a las demás."
    " No incluyas ningún comentario como 'Aquí está tu respuesta'"
)

expound_chain = (
    {'q1': itemgetter(0), 'questions': itemgetter(1)}
    | expound_prompt
    | instruct_llm
)

longer_docs = []

if not os.path.exists(LONG_DOC_FILE):
    for i, query in enumerate(queries):
        longer_doc = expound_chain.invoke([query, queries])
        longer_docs.append(longer_doc)

    with open(LONG_DOC_FILE, 'w') as f:
        json.dump(longer_docs, f)
else:
    with open(LONG_DOC_FILE, 'r') as f:
        longer_docs = json.load(f)
    pprint("Longer docs loaded from file")

# Cut longer docs for embedding
longer_docs_cut = [doc[:100] for doc in longer_docs]

# Generate embeddings for cut longer documents
q_long_embs = generate_embeddings(longer_docs_cut)
d_long_embs = generate_embeddings(longer_docs_cut, is_query=False)


plt.figure(figsize=(8, 6))
plot_similarity_matrix(q_embeddings, d_embeddings,
                       "Query Embeddings vs Document Embeddings")
plt.savefig('plots/similarity_matrix_queries_vs_docs.png')

# Plotting similarity matrices
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plot_similarity_matrix(q_embeddings, q_long_embs,
                       "Query Embeddings vs Long Query Docs")
plt.subplot(1, 2, 2)
plot_similarity_matrix(q_embeddings, d_long_embs,
                       "Query Embeddings vs Long Docs")
plt.savefig('plots/similarity_matrices_comparison.png')
