from core.extractor import RExtract
from core.knowledge_base import KnowledgeBase
from core.prompt import external_prompt, parser_prompt
from adapters.llm_adapter import LLMAdapter
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable.passthrough import RunnableAssign
from infrastructure.database import database_getter


def knowbase_getter(x):
    y = extractor.invoke(x)
    return y


chat_llm = LLMAdapter() | StrOutputParser()
instruct_llm = LLMAdapter() | StrOutputParser()

extractor = RExtract(KnowledgeBase, instruct_llm, parser_prompt)

external_chain = external_prompt | chat_llm

internal_chain = (
    RunnableAssign({'know_base': knowbase_getter})
    | RunnableAssign({'context': database_getter})
)
