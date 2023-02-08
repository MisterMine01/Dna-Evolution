from ..simply_entities import Entity, Dna, Gene
from tkinter import Canvas
from math import cos, sin, pi
import random

MAX_SIZE = 100
MAX_SPEED = 100
MAX_BABIES = 2
MAX_PERCENT_BABIES = 1
MAX_X_Y_SEX = 5
PERCENT_MUTATION = 0.001
MIN_TIME_TO_LIVE = 0
MULTIPLIER_TIME_TO_LIVE = 0.2


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
    generation: int = 0
    baby: list[Entity]
    dead: bool = False
    energy: int = 0


    # dna
    size: int = 0
    speed: int = 0
    color: tuple[int, int, int]
    orientation_percent: float = 0
    orientation_radian: float = 0

    babies_percent: float = 0
    sex: bool = False

    time_to_live: int = 0

    need_energy: int = 0
    give_energy: int = 0
    percent_eat: float = 0
    carnivore: bool = False


    def __init__(self, dna: Dna or None = None) -> None:
        self.baby = []
        if dna is None:
            dna = generate_dna(17)
        super().__init__(dna)
        self.decode_dna()

    def decode_dna(self) -> None:
        self.size = (self.dna.get_gene(0).to_int() + 1) * MAX_SIZE / 94
        self.speed = self.dna.get_gene(1).to_int() * MAX_SPEED / 94

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

        # decode death
        self.time_to_live = int((MIN_TIME_TO_LIVE + self.dna.get_gene(12).to_int()) * MULTIPLIER_TIME_TO_LIVE)

        # decode eat
        self.need_energy = self.dna.get_gene(13).to_int()
        self.percent_eat = self.dna.get_gene(14).to_int() / 94
        self.carnivore = self.dna.get_gene(15).to_int() % 2 == 0


    
    def make_babies(self, other: list) -> tuple[Entity, list]:
        if self.dead:
            return (None, [])
        global MAX_X_Y_SEX, MAX_BABIES, MAX_PERCENT_BABIES
        babies: list[Entity] = []
        for i in other:
            if (
                self.x + self.size < i.x - i.size or
                self.x - self.size > i.x + i.size or
                self.y + self.size < i.y - i.size or
                self.y - self.size > i.y + i.size or
                i.dead
            ):
                continue
            if (
                (i is self) or
                self.sex == i.sex or
                i in self.baby
            ):
                continue

            if random.random() < ((self.babies_percent + i.babies_percent) / 2) * MAX_PERCENT_BABIES:
                i.baby.append(self)
                self.baby.append(i)
                for j in range(random.randint(1, MAX_BABIES)):
                    babies.append(BasesEntity(self.dna.join(i.dna)))
                    babies[-1].x = self.x
                    babies[-1].y = self.y
                    babies[-1].dna.mutate(PERCENT_MUTATION)
                    babies[-1].decode_dna()
                    babies[-1].generation = max(self.generation, i.generation)+1
                    self.baby.append(babies[-1])
                    i.baby.append(babies[-1])
            return (i, babies)
        return (None, babies)
    
    def get_names(self) -> str:
        return str(self.generation) + ("M" if self.sex else "F")
    
    def is_dead(self) -> bool:
        if self.dead:
            return True
        #if random.random() < self.percent_death:
        #    self.dead = True
        #    return True
        if self.time_to_live < 0:
            self.dead = True
            return True
        return False


    def draw(self, canvas: Canvas) -> None:
        if self.is_dead():
            canvas.create_rectangle(self.x - self.size // 2, self.y - self.size // 2, self.x + self.size // 2, self.y + self.size // 2, fill="white")
            canvas.create_text(self.x + self.size // 4, self.y + self.size // 4, text=self.get_names(), fill="black")
        else:
            canvas.create_oval(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill=self.get_hex_color())
            canvas.create_text(self.x + self.size / 2, self.y + self.size / 2, text=self.get_names(), fill="black")

    def get_hex_color(self) -> str:
        return '#%02x%02x%02x' % self.color


    def move(self) -> None:
        if self.is_dead():
            return
        rand = random.random()
        if rand < self.orientation_percent or self.x < 0 or self.x > 1000 or self.y < 0 or self.y > 1000:
            if rand < self.orientation_percent / 2:
                self.orientation += self.orientation_radian
            else:
                self.orientation -= self.orientation_radian
        self.time_to_live -= 1
        self.x += self.speed * cos(self.orientation) / (self.size / 10)
        self.y += self.speed * sin(self.orientation) / (self.size / 10)