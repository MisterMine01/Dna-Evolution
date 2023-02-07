from ..simply_entities import Entity, Dna, Gene
from tkinter import Canvas
from math import cos, sin


class BasesEntity(Entity):
    x: int = 0
    y: int = 0
    orientation: float = 0
    size: int = 0
    speed: int = 0
    color: tuple[int, int, int]

    def __init__(self, dna: Dna or None = None) -> None:
        if dna is None:
            dna = self.generate_dna()
        print(dna)
        super().__init__(dna)
        self.color = (0, 0, 0)
        self.size = self.dna.get_gene(0).to_int()
        self.speed = self.dna.get_gene(1).to_int()
        r: int = self.dna.get_gene(2).to_int() + self.dna.get_gene(3).to_int()
        g: int = self.dna.get_gene(4).to_int() + self.dna.get_gene(5).to_int()
        b: int = self.dna.get_gene(6).to_int() + self.dna.get_gene(7).to_int()
        self.color = (r, g, b)

    def generate_dna(self) -> Dna:
        dna = Dna()
        for i in range(8):
            dna._genes.append(Gene())
            dna._genes[i].mutate()
        return dna

    def draw(self, canvas: Canvas) -> None:
        canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.get_hex_color())

    def get_hex_color(self) -> str:
        return '#%02x%02x%02x' % self.color
    
    def move(self) -> None:
        self.x += self.speed * cos(self.orientation) / (self.size / 10)
        self.y += self.speed * sin(self.orientation) / (self.size / 10)