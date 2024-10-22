from typing import List
from langchain_core.runnables.passthrough import RunnableAssign
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ArxivLoader
from langchain_community.document_loaders import UnstructuredFileLoader
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

# from langchain_nvidia_ai4_endpoints import ChatNVIDIA


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


def loading_in_the_file():
    # Loading in the file

    # Unstructured File Loader: Good for arbitrary "probably good enough" loader
    # documents = UnstructuredFileLoader("llama2_paper.pdf").load()

    # More specialized loader, won't work for everything, but simple API and usually better results
    documents = ArxivLoader(query="2404.16130").load()  # GraphRAG
    # documents = ArxivLoader(query="2404.03622").load()  ## Visualization-of-Thought
    # documents = ArxivLoader(query="2404.19756").load()  ## KAN: Kolmogorov-Arnold Networks
    # documents = ArxivLoader(query="2404.07143").load()  # Infini-Attention
    # documents = ArxivLoader(query="2210.03629").load()  ## ReAct

    # Printing out a sample of the content
    # print("Number of Documents Retrieved:", len(documents))
    # print(
    #     f"Sample of Document 1 Content (Total Length: {len(documents[0].page_content)}):")
    # print(documents[0].page_content[:1000])

    pprint(documents[0].metadata)


def splitting_the_documents():

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", ";", ",", " ", ""],
    )

    documents = ArxivLoader(query="2404.16130").load()  # GraphRAG

    # Some nice custom preprocessing
    # documents[0].page_content = documents[0].page_content.replace(". .", "")
    docs_split = text_splitter.split_documents(documents)

    # def include_doc(doc):
    #     ## Some chunks will be overburdened with useless numerical data, so we'll filter it out
    #     string = doc.page_content
    #     if len([l for l in string if l.isalpha()]) < (len(string)//2):
    #         return False
    #     return True

    # docs_split = [doc for doc in docs_split if include_doc(doc)]
    print(len(docs_split))

    for i in (0, 1, 2, 15, -1):
        pprint(f"[Document {i}]")
        print(docs_split[i].page_content)
        pprint("="*64)


def RExtract(pydantic_class, llm, prompt):
    '''
    Runnable Extraction module
    Returns a knowledge dictionary populated by slot-filling extraction
    '''
    parser = PydanticOutputParser(pydantic_object=pydantic_class)
    instruct_merge = RunnableAssign(
        {'format_instructions': lambda x: parser.get_format_instructions()})

    def preparse(string):
        if '{' not in string:
            string = '{' + string
        if '}' not in string:
            string = string + '}'
        string = (string
                  .replace("\\_", "_")
                  .replace("\n", " ")
                  .replace("\]", "]")
                  .replace("\[", "[")
                  )
        # print(string)  ## Good for diagnostics
        return string
    return instruct_merge | prompt | llm | preparse | parser


class DocumentSummaryBase(BaseModel):
    running_summary: str = Field(
        "", description="Descripción en curso del documento. ¡No lo sobrescribas; solo actualiza!")
    main_ideas: List[str] = Field(
        [], description="Información más importante del documento (máx. 3)")
    loose_ends: List[str] = Field(
        [], description="Preguntas abiertas que sería bueno incorporar en el resumen, pero que aún son desconocidas (máx. 3)")


summary_prompt = ChatPromptTemplate.from_template(
    "Estás generando un resumen en curso del documento. Hazlo legible para un usuario técnico."
    " Después de esto, la antigua base de conocimientos será reemplazada por la nueva. Asegúrate de que un lector aún pueda entender todo."
    " Mantenlo corto, pero tan denso y útil como sea posible. La información debe fluir de fragmento a (preguntas abiertas o ideas principales) a resumen en curso."
    " La base de conocimientos actualizada mantiene toda la información del resumen en curso aquí: {info_base}."
    "\n\n{format_instructions}. Sigue el formato con precisión, incluyendo citas y comas"
    "\n\nSin perder ninguna de la información, actualiza la base de conocimientos con lo siguiente: {input}"
)


latest_summary = ""


def RSummarizer(knowledge, llm, prompt, verbose=False):
    '''
    Exercise: Create a chain that summarizes
    '''
    def summarize_docs(docs):
        # Initialize the parse_chain appropriately;
        parse_chain = (RunnableAssign({'info_base': RExtract(
            DocumentSummaryBase, llm, summary_prompt)}))

        # Initialize a valid starting state. Should be similar to notebook 4
        state = {'info_base': DocumentSummaryBase()}

        global latest_summary  # If your loop crashes, you can check out the latest_summary

        for i, doc in enumerate(docs):
            #  Update the state as appropriate using your parse_chain component
            state['input'] = doc.page_content
            state = parse_chain.invoke(state)

            assert 'info_base' in state
            if verbose:
                print(f"Considered {i+1} documen ts")
                pprint(state['info_base'])
                latest_summary = state['info_base']

        return state['info_base']

    return RunnableLambda(summarize_docs)


def refining():
    instruct_model = ChatOpenAI(model="gpt-4o-mini").bind(max_tokens=1024)
    instruct_llm = instruct_model | StrOutputParser()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", ";", ",", " ", ""],
    )

    documents = ArxivLoader(query="2404.16130").load()  # GraphRAG

    # Some nice custom preprocessing
    documents[0].page_content = documents[0].page_content.replace(". .", "")
    docs_split = text_splitter.split_documents(documents)

    print(f"{docs_split[0]=}")

    # # Take the first 10 document chunks and accumulate a DocumentSummaryBase
    # summarizer = RSummarizer(DocumentSummaryBase(
    # ), instruct_llm, summary_prompt, verbose=True)

    # summary = summarizer.invoke(docs_split[:15])


pprint(latest_summary)
