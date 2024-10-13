import config
from core.knowledge_base import KnowledgeBase
from adapters.gradio_adapter import queue_fake_streaming_gradio, launch_gradio_chatbot
from adapters.console_adapter import pprint
from core.pipeline import internal_chain, external_chain


state = {'know_base': KnowledgeBase()}


def chat_gen(message, history=[], return_buffer=True):

    # Pulling in, updating, and printing the state
    global state
    state['input'] = message
    state['history'] = history
    state['output'] = "" if not history else history[-1][1]

    # Generating the new state from the internal chain
    state = internal_chain.invoke(state)
    print("State after chain run:")
    pprint({k: v for k, v in state.items() if k != "history"})

    # Streaming the results
    buffer = ""
    for token in external_chain.stream(state):
        buffer += token
        yield buffer if return_buffer else token


if __name__ == "__main__":
    starter_message = "Hola! Soy tu agente de SkyFlow. ¿Cómo puedo ayudarte?"
    chat_history = [[None, starter_message]]
    # queue_fake_streaming_gradio(chat_gen, history=chat_history)
    launch_gradio_chatbot(chat_gen, history=chat_history)
