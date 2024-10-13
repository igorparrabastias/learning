import os

# Definir la estructura del proyecto
project_structure = {
    "src": {
        "adapters": {
            "__init__.py": "",
            "llm_adapter.py": "",
            "gradio_adapter.py": ""
        },
        "core": {
            "__init__.py": "",
            "prompt.py": "",
            "knowledge_base.py": "",
            "extractor.py": "",
            "pipeline.py": ""
        },
        "infrastructure": {
            "__init__.py": "",
            "flight_info.py": "",
            "database.py": ""
        },
        "preprocessors": {
            "__init__.py": "",
            "text_cleaner.py": ""
        },
        "main.py": ""
    }
}

# Función para crear la estructura de archivos y carpetas


def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Crear carpeta
            os.makedirs(path, exist_ok=True)
            # Crear contenido recursivamente
            create_project_structure(path, content)
        else:
            # Crear archivo vacío
            with open(path, 'w') as f:
                f.write(content)


# Crear la estructura en el directorio actual
base_path = os.getcwd()
create_project_structure(base_path, project_structure)

print("Estructura del proyecto creada exitosamente.")
