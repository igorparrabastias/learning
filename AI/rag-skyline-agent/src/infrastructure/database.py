from core.knowledge_base import KnowledgeBase


def get_key_fn(base: KnowledgeBase) -> dict:
    """
    Dado un objeto KnowledgeBase, devuelve un diccionario con la clave
    para realizar la consulta de información.
    """
    return {
        'first_name': base.first_name,
        'last_name': base.last_name,
        'confirmation': base.confirmation,
    }


# get_key = RunnableLambda(get_key_fn)
# (get_key | get_flight_info).invoke(know_base)
# database_getter = itemgetter('know_base') | get_key | get_flight_info


def database_getter(state: dict):
    """
    Función que extrae datos de la base de datos usando la base de conocimiento proporcionada en el estado.
    """
    know_base = state['know_base']  # Obtener la base de conocimiento actual del estado

    # Generar la clave para la consulta
    key = get_key_fn(know_base)

    # Simular la llamada a una función externa para obtener la información del vuelo
    flight_info = get_flight_info(key)

    return flight_info


def get_flight_info(d: dict) -> str:
    """
    Función que simula la recuperación de información de vuelos. Eventualmente,
    una base de datos real será usada.
    """
    req_keys = ['first_name', 'last_name', 'confirmation']

    # Verificar que las claves necesarias están presentes en el diccionario
    assert all((key in d)
               for key in req_keys), f"Se esperaba un diccionario con las claves {req_keys}, pero se obtuvo {d}"

    # Datos simulados de vuelos
    keys = ['first_name', 'last_name', 'confirmation', 'departure',
            'destination', 'departure_time', 'arrival_time', 'flight_day']
    values = [
        ["Jane", "Doe", 12345, "San Jose", "New Orleans",
            "12:31 PM", "9:31 PM", "mañana"],
        ["John", "Smith", 54321, "Nueva York",
            "Los Ángeles", "8:00 AM", "11:00 AM", "domingo"],
        ["Alice", "Johnson", 98765, "Chicago", "Miami",
            "7:00 PM", "11:00 PM", "la próxima semana"],
        ["Bob", "Brown", 56789, "Dallas", "Seattle", "1:00 PM", "4:00 PM", "ayer"],
    ]

    # Funciones auxiliares para obtener la clave y el valor
    def get_key(d): return "|".join(
        [d['first_name'], d['last_name'], str(d['confirmation'])])

    def get_val(l): return {k: v for k, v in zip(keys, l)}

    # Simular la base de datos
    db = {get_key(get_val(entry)): get_val(entry) for entry in values}

    # Buscar el registro correspondiente en la base de datos
    data = db.get(get_key(d))

    if not data:
        return f"Basado en {req_keys} = {get_key(d)}, no se encontró información sobre el vuelo del usuario."

    return (
        f"El vuelo de {data['first_name']} {data['last_name']} desde {data['departure']} a {data['destination']} "
        f"sale a las {data['departure_time']} {data['flight_day']} y llega a las {data['arrival_time']}."
    )
