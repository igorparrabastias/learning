from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
# from langchain.output_parsers import StrOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, max_tokens=100)


def run_chat_llm():
    chat_llm = ChatOpenAI(model="gpt-4o-mini",
                          temperature=0) | StrOutputParser()
    text = "What would be a good company name for a company that makes colorful socks?"
    print(chat_llm.invoke(text))


def run_llm_chain():

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant about company names."),
            ("human",
             "What is a good name for a company that makes {product}?"),
        ]
    )

    chain = prompt | llm
    r = chain.invoke(
        {
            "product": "eco-friendly water bottles",
        }
    )
    print(r.content)


run_llm_chain()
