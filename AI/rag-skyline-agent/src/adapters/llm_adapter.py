from langchain_openai import ChatOpenAI


def LLMAdapter(model="gpt-4o-mini"):
    return ChatOpenAI(model=model)
