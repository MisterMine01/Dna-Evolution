import random

class Gene:
    value: chr = None

    def __init__(self) -> None:
        self.value = None

    def __add__(self, other):
        new_gene = Gene()
        if random.random() < 0.5:
            new_gene.value = self.value
        else:
            new_gene.value = other.value
        return new_gene
    
    def mutate(self):
        self.value = chr(random.randint(32, 126))
    
    def to_int(self) -> int:
        return ord(self.value) - 32