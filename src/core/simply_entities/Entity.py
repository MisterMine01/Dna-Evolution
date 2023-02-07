from .dna import Dna, Gene


class Entity:
    dna: Dna = None
    fitness: float = 0

    def __init__(self, dna: Dna) -> None:
        self.dna = dna
    
    def from_dna(dna: Dna):
        return Entity(dna)

    def from_string(string: str):
        dna = Dna()
        for char in string:
            gene = Gene()
            gene.value = char
            dna._genes.append(gene)
        return Entity(dna)
    
    def from_nothing(size: int):
        dna = Dna()
        for _ in range(size):
            dna._genes.append(Gene())
        return Entity(dna)
    
    def get_gene_value(self, index: int) -> int or None:
        return self.dna.get_gene(index).to_int()

    def __str__(self) -> str:
        return ''.join([str(gene) for gene in self.dna.get_dna()])

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__str__() == other.__str__()

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __add__(self, other):
        return Entity(self.dna.join(other.dna))

    def mutate(self, mutation_rate: float):
        self.dna.mutate(mutation_rate)