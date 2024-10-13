import gradio as gr


def queue_fake_streaming_gradio(chat_stream, history=[], max_questions=8):

    # Mimic of the gradio initialization routine, where a set of starter messages can be printed off
    for human_msg, agent_msg in history:
        if human_msg:
            print("\n[ Human ]:", human_msg)
        if agent_msg:
            print("\n[ Agent ]:", agent_msg)

    # Mimic of the gradio loop with an initial message from the agent.
    for _ in range(max_questions):
        print(f"{_=}")
        message = input("\n[ Human ]: ")
        print("\n[ Agent ]: ")
        history_entry = [message, ""]
        for token in chat_stream(message, history, return_buffer=False):
            print(token, end='')
            history_entry[1] += token
        history += [history_entry]
        print("\n")


def launch_gradio_chatbot(chat_gen, history=[]):
    chatbot = gr.Chatbot(value=history)
    demo = gr.ChatInterface(chat_gen, chatbot=chatbot).queue().launch(
        debug=True, share=False)
