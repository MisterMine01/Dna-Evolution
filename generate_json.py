log = open("log.txt")
log_data = log.read().split("\n")
log.close()

log_entry = []
for i in log_data:
    dat = i.split(" -> ")
    dat[0] = dat[0].split(" + ")
    dat[1] = dat[1][1:-1].split(", ")
    log_entry.append(dat)

data = {"father": [], "mother": []}
for i in log_entry:
    for j in i[1]:
        data["father"].append([i[0][0], j])
        data["mother"].append([i[0][1], j])

    
from graphviz import Digraph

dot = Digraph(comment="Tree")

for father, child in data["father"]:
    print(father, child)
    "_point_".join(father.split(":"))
    "_point_".join(child.split(":"))
    "_minus_".join(father.split("-"))
    "_minus_".join(child.split("-"))
    dot.node(father)
    dot.node(child)
    dot.edge(father, child)

for mother, child in data["mother"]:
    print(mother, child)
    "_point_".join(mother.split(":"))
    "_point_".join(child.split(":"))
    "_minus_".join(mother.split("-"))
    "_minus_".join(child.split("-"))
    dot.node(mother)
    dot.node(child)
    dot.edge(mother, child)

dot.render(directory='doctest-output', view=True)  