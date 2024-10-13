from rich.style import Style
from rich.console import Console
from functools import partial
from operator import itemgetter

console = Console()
base_style = Style(color="#76B900", bold=True)
pprint = partial(console.print, style=base_style)

# initialize
a = []

# create the table (name, age, job)
a.append(["Nick", 30, "Doctor"])
a.append(["John",  8, "Student"])
a.append(["Paul", 22, "Car Dealer"])
a.append(["Mark", 66, "Retired"])

# sort the table by age
a.sort(key=itemgetter(0))
pprint(a)
a.sort(key=lambda x: x[1])
pprint(a)

# operator.itemgetter(1, 2)
# lambda elem: (elem[1], elem[2])
