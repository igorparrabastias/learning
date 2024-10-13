from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.passthrough import RunnableAssign


def RExtract(pydantic_class, llm, prompt):
    '''
    Módulo de extracción ejecutable que devuelve un diccionario de conocimiento
    poblado mediante extracción de llenado de espacios.
    '''
    # Crear un parser de salida de Pydantic con la clase pydantic proporcionada
    parser = PydanticOutputParser(pydantic_object=pydantic_class)

    # Asignar instrucciones de formato utilizando una función lambda para obtener
    # las instrucciones de formato del parser
    # La lambda se ejecutará cuando RunnableAssign sea invocado o utilizado dentro de ese flujo de trabajo. E
    instruct_merge = RunnableAssign(
        {'format_instructions': lambda x: parser.get_format_instructions()})

    # Definir una función para preprocesar la cadena de entrada
    def preparse(string):
        # Si la cadena no contiene '{', agregar '{' al inicio
        if '{' not in string:
            string = '{' + string
        # Si la cadena no contiene '}', agregar '}' al final
        if '}' not in string:
            string = string + '}'
        # Reemplazar caracteres específicos en la cadena
        string = (string
                  .replace("\\_", "_")  # Reemplazar "\_" con "_"
                  # Reemplazar saltos de línea con espacios
                  .replace("\n", " ")
                  .replace("\]", "]")   # Reemplazar "\]" con "]"
                  .replace("\[", "[")   # Reemplazar "\[" con "["
                  )
        print(string)  # Bueno para diagnósticos
        return string

    # Devolver una cadena de operaciones que incluye las instrucciones de formato,
    # el prompt, el modelo de lenguaje y la función de preprocesamiento
    # return instruct_merge | prompt | llm | PPrint | preparse | parser
    return instruct_merge | prompt | llm | preparse | parser
