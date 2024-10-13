from langchain_community.vectorstores import FAISS
from operator import itemgetter
from functools import partial
from langchain_community.document_transformers import LongContextReorder
from langchain_core.runnables.passthrough import RunnableAssign
from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnablePassthrough
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from fastapi import FastAPI
# https://python.langchain.com/docs/langserve#server

# May be useful later


# TODO: Make sure to pick your LLM and do your prompt engineering as necessary for the final assessment
embedder = NVIDIAEmbeddings(model="nvidia/nv-embed-v1", truncate="END")
instruct_llm = ChatNVIDIA(model="mistralai/mixtral-8x22b-instruct-v0.1")

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# PRE-ASSESSMENT: Run as-is and see the basic chain in action


# @app.route("/health")
async def health():
    return {"success": True}, 200


add_routes(
    app,
    RunnableLambda(lambda _: health()),
    path="/health",
)

add_routes(
    app,
    instruct_llm,
    path="/basic_chat",
)

# ASSESSMENT TODO: Implement these components as appropriate

add_routes(
    app,
    RunnableLambda(lambda x: "Not Implemented"),
    path="/generator",
)

add_routes(
    app,
    RunnableLambda(lambda x: []),
    path="/retriever",
)

# Might be encountered if this were for a standalone python file...
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9012)
