from ..simply_entities import Entity, Dna, Gene
from tkinter import Canvas
from math import cos, sin, pi
import random

MAX_SIZE = 100
MAX_SPEED = 100
MAX_BABIES = 2
MAX_PERCENT_BABIES = 1
MAX_X_Y_SEX = 5
PERCENT_MUTATION = 0.1

def generate_dna(size: int) -> Dna:
    dna = Dna()
    for i in range(size):
        dna.genes.append(Gene())
        dna.genes[i].mutate()
    return dna


class BasesEntity(Entity):
    x: int = 0
    y: int = 0
    orientation: float = 0


    # dna
    size: int = 0
    speed: int = 0
    color: tuple[int, int, int]
    orientation_percent: float = 0
    orientation_radian: float = 0

    babies_percent: float = 0
    sex: bool = False


    test_baby: bool = False

    baby: list[Entity] = []

    def __init__(self, dna: Dna or None = None) -> None:
        if dna is None:
            dna = generate_dna(12)
        super().__init__(dna)
        self.decode_dna()

    def decode_dna(self) -> None:
        self.size = self.dna.get_gene(0).to_int() + 1
        self.speed = self.dna.get_gene(1).to_int()

        # decode color
        r: int = self.dna.get_gene(2).to_int() + self.dna.get_gene(3).to_int()
        g: int = self.dna.get_gene(4).to_int() + self.dna.get_gene(5).to_int()
        b: int = self.dna.get_gene(6).to_int() + self.dna.get_gene(7).to_int()
        self.color = (r, g, b)

        # decode orientation
        self.orientation_percent = self.dna.get_gene(8).to_int() / 94
        self.orientation_radian = (self.dna.get_gene(9).to_int() / 94) * 2 * pi

        # decode babies
        self.babies_percent = self.dna.get_gene(10).to_int() / 94
        self.sex = self.dna.get_gene(11).to_int() % 2 == 0

    
    def make_babies(self, other: list) -> list:
        global MAX_X_Y_SEX, MAX_BABIES, MAX_PERCENT_BABIES
        babies: list[Entity] = []
        for i in other:
            if (
                self.x + self.size < i.x - i.size or
                self.x - self.size > i.x + i.size or
                self.y + self.size < i.y - i.size or
                self.y - self.size > i.y + i.size
            ):
                continue
            if (
                (i is self) or
                self.sex == i.sex or
                i in self.baby
            ):
                continue
            if random.random() < ((self.babies_percent + i.babies_percent) / 2) * MAX_PERCENT_BABIES:
                print("baby")
                i.baby.append(self)
                self.baby.append(i)
                for j in range(random.randint(1, MAX_BABIES)):
                    babies.append(BasesEntity(self.dna.join(i.dna)))
                    babies[-1].x = self.x
                    babies[-1].y = self.y
                    babies[-1].dna.mutate(PERCENT_MUTATION)
                    babies[-1].decode_dna()
                    babies[-1].test_baby = True
                    self.baby.append(babies[-1])
            break
        return babies

    def draw(self, canvas: Canvas) -> None:
        canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.get_hex_color())
        if self.test_baby:
            canvas.create_text(self.x + self.size / 2, self.y + self.size / 2, text="baby", fill="black")

    def get_hex_color(self) -> str:
        return '#%02x%02x%02x' % self.color


    def move(self) -> None:
        rand = random.random()
        if rand < self.orientation_percent or self.x < 0 or self.x > 1000 or self.y < 0 or self.y > 1000:
            if rand < self.orientation_percent / 2:
                self.orientation += self.orientation_radian
            else:
                self.orientation -= self.orientation_radian
        self.x += self.speed * cos(self.orientation) / (self.size / 10)
        self.y += self.speed * sin(self.orientation) / (self.size / 10)