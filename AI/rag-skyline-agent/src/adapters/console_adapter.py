from rich.console import Console
from rich.style import Style
from functools import partial

# Crear un estilo para la consola
base_style = Style(color="#76B900", bold=True)
console = Console()

# Crear una función para imprimir en consola con el estilo especificado
pprint = partial(console.print, style=base_style)
