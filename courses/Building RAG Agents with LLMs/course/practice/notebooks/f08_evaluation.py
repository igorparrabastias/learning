import random
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
llm = instruct_llm | StrOutputParser()


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


def format_chunk(doc):
    return (
        f"Paper: {doc.metadata.get('Title', 'unknown')}"
        f"\n\nSummary: {doc.metadata.get('Summary', 'unknown')}"
        f"\n\nPage Body: {doc.page_content}"
    )


def view_docstore(docstore):
    i = 0
    # for _, item in docstore.docstore._dict.items():
    #     pprint(f"{i=}: {item.page_content[:100]}")
    #     i += 1

    for doc in docs:
        if doc.metadata:
            print(f"\ntitle: {doc.metadata.get('Title', 'unknown')}" +
                  f"\ncontent: {doc.page_content[:100]}")
    # print(format_chunk(docs[len(docs)//2]))


if os.path.exists(INDEX_FILE):
    pprint(f"FAISS index loading from {INDEX_FILE}")
    docstore = FAISS.load_local(
        INDEX_FILE, embedder, allow_dangerous_deserialization=True
    )
    pprint(f"Constructed docstore with {len(docstore.docstore._dict)} chunks")

    # docs queda en el scope global!
    # y es accesible en view_docstore()!
    docs = list(docstore.docstore._dict.values())
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
    "Eres un chatbot de documentos. Ayuda al usuario según vayan preguntando sobre documentos."
    " El usuario acaba de preguntarte una pregunta: {input}\n\n"
    " La siguiente información puede ser útil para tu respuesta: "
    " Recuperación de Documentos:\n{context}\n\n"
    " (Respuesta solo desde la recuperación. Solo cita fuentes que se hayan utilizado. Haz que tu respuesta sea conversacional)"
    "\n\nPregunta del Usuario: {input}"
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
long_reorder = RunnableLambda(LongContextReorder().transform_documents)

context_getter = (
    itemgetter('input')
    # Interfaz estándar de LangChain: LangChain sigue una interfaz de retrievers, donde objetos como el que se genera con as_retriever() implementan un método estándar que procesa las consultas. En la implementación de estos objetos, se define un método __call__ o invoke que, cuando se llama al objeto, automáticamente invoca get_relevant_documents().
    | docstore.as_retriever()
    | long_reorder
    | docs2str)

retrieval_chain = {'input': (lambda x: x)} | RunnableAssign({
    'context': context_getter})

# intermediate_result = {'input': "What is holon?"}
# pprint(context_getter.invoke(intermediate_result['input']))


# print(context_getter.invoke({'input': "What is holon?"}))
# pprint(retrieval_chain.invoke("What is holon?"))
# sys.exit()

# Chain 2 Specs: retrieval_chain -> generator_chain
# -> {"output" : <str>, ...} -> output_puller
generator_chain = (
    chat_prompt | RPrint() | instruct_llm | StrOutputParser()
)
# pprint(generator_chain.invoke(
#     {'input': "What is holon?", 'context': context_getter.invoke({'input': "What is holon?"})}))
# sys.exit()

generator_chain = {'output': generator_chain} | RunnableLambda(
    output_puller)

# END TODO
#####################################################################

rag_chain = retrieval_chain | generator_chain

# pprint(rag_chain.invoke("¡Dime algo interesante!"))
# for token in rag_chain.stream("Tell me something interesting!"):
#     print(token, end="")
# sys.exit()

#####################################################################
# Use those two document chunks to generate a synthetic "baseline" question-answer pair.
#####################################################################

num_questions = 1
synth_questions = []
synth_answers = []

simple_prompt = ChatPromptTemplate.from_messages(
    [('system', '{system}'), ('user', 'INPUT: {input}')])

for i in range(num_questions):
    doc1, doc2 = random.sample(docs, 2)
    sys_msg = (
        "Utiliza los documentos proporcionados por el usuario para generar un par de pregunta y respuesta interesante."
        " Intenta usar ambos documentos si es posible, y confía más en los cuerpos de los documentos que en el resumen."
        " Utiliza el formato:\nPregunta: (buena pregunta, 1-3 oraciones, detallada)\n\nRespuesta: (respuesta derivada de los documentos)"
        " ¡NO DIGAS: \"Aquí está un par de pregunta interesante\" o similar. ¡SIGUE EL FORMATO!"
    )
    usr_msg = (
        f"Document1: {format_chunk(doc1)}\n\n"
        f"Document2: {format_chunk(doc2)}"
    )

    qa_pair = (simple_prompt | llm).invoke(
        {'system': sys_msg, 'input': usr_msg})
    synth_questions += [qa_pair.split('\n\n')[0]]
    synth_answers += [qa_pair.split('\n\n')[1]]
    pprint2(f"QA Pair {i+1}")
    pprint2(synth_questions[-1])
    pprint(synth_answers[-1])
    print()

# #####################################################################
# Use the RAG agent to generate its own answer.
# #####################################################################

# pprint(rag_chain.invoke(synth_questions[0]))

rag_answers = []
for i, q in enumerate(synth_questions):
    rag_answer = (simple_prompt | llm).invoke(
        {'system': sys_msg, 'input': q})
    rag_answers += [rag_answer]
    pprint2(f"QA Pair {i+1}", q, "", sep="\n")
    pprint(f"RAG Answer: {rag_answer}", "", sep='\n')

# #####################################################################
# Use a judge LLM to compare the two responses while grounding the synthetic generation as "ground-truth correct."
# #####################################################################

# TODO: Adapt this prompt for whichever LLM you're actually interested in using.
# If it's llama, maybe system message would be good?
eval_prompt = ChatPromptTemplate.from_template("""INSTRUCCIONES:
Evalúa el siguiente par de pregunta y respuesta para preferencia y consistencia humanas.
Asume que la primera respuesta es una respuesta de verdad y tiene que ser correcta.
Asume que la segunda respuesta puede ser o no ser verdadera.
[1] La segunda respuesta miente, no responde la pregunta, o es inferior a la primera respuesta.
[2] La segunda respuesta es mejor que la primera y no introduce ninguna inconsistencia.

Formato de Salida:
[Puntuación] Justificación

{qa_trio}

EVALUACION:
""")

pref_score = []

trio_gen = zip(synth_questions, synth_answers, rag_answers)
for i, (q, a_synth, a_rag) in enumerate(trio_gen):
    pprint2(f"Conjunto {i+1}\n\nPregunta: {q}\n\n")

    qa_trio = f"Pregunta: {q}\n\nRespuesta 1 (Verdad Absoluta): {a_synth}\n\n Respuesta 2 (Nueva Respuesta): {a_rag}"
    pref_score += [(eval_prompt | llm).invoke({'qa_trio': qa_trio})]
    pprint(f"Respuesta Sintética: {a_synth}\n\n")
    pprint(f"Respuesta RAG: {a_rag}\n\n")
    pprint2(f"Evaluación Sintética: {pref_score[-1]}\n\n")

pref_score = sum(("[2]" in score) for score in pref_score) / len(pref_score)
print(f"Puntuación de Preferencia: {pref_score}")
