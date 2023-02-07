from .Gene import Gene
import random

class Dna:
    _genes: list[Gene] = []

    def size(self) -> int:
        return len(self._genes)
    
    def get_gene(self, index: int) -> Gene:
        return self._genes[index]

    def get_dna(self) -> list[Gene]:
        return self._genes

    def join(self, other_dna):
        if not isinstance(other_dna, Dna):
            raise TypeError("Other dna must be a Dna object")
        if other_dna.size() != self.size():
            raise ValueError("Other dna must have the same size")
        new_dna = Dna()
        for i in range(self.size()):
            new_dna._genes.append(self._genes[i] + other_dna._genes[i])
        return new_dna

    def mutate(self, mutation_rate: float):
        if random.random() < mutation_rate:
            self._genes[random.randint(0, self.size() - 1)].mutate()