from langchain_core.prompts import ChatPromptTemplate

external_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Eres un chatbot de SkyFlow Airlines y estás ayudando a un cliente con su problema."
        " ¡Por favor, chatea con ellos! ¡Mantente conciso y claro!"
        " Tu base de conocimiento en ejecución es: {know_base}."
        " Esto es solo para ti; ¡No lo menciones!"
        " \nUsando eso, recuperamos lo siguiente: {context}\n"
    )),
    ("assistant", "{output}"),
    ("user", "{input}"),
])

parser_prompt = ChatPromptTemplate.from_template(
    "Eres un asistente de chat que representa a la aerolínea SkyFlow y estás tratando de rastrear información sobre la conversación."
    " Acabas de recibir un mensaje del usuario. Por favor, completa el esquema basado en el chat."
    "\n\n{format_instructions}"
    "\n\nOLD KNOWLEDGE BASE: {know_base}"
    "\n\nASSISTANT RESPONSE: {output}"
    "\n\nUSER MESSAGE: {input}"
    "\n\nNEW KNOWLEDGE BASE: "
)
