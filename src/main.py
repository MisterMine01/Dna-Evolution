from tkinter import *
from core.entities import BasesEntity
import random

root = Tk()
root.title("Canvas")
root.attributes("-fullscreen", True)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

root.update_idletasks()


canvas = Canvas(root, bg="white", width=root.winfo_width(), height=root.winfo_height())
canvas.pack()

entity: list[BasesEntity] = []


for i in range(10):
    entity_new = BasesEntity()
    entity.append(entity_new)
    entity[-1].x = random.randint(0, root.winfo_width())
    entity[-1].y = random.randint(0, root.winfo_height())

for e in entity:
    print(e)

def update():
    global entity
    b = False
    canvas.delete("all")
    for i in entity:
        i.move()
        if not b:
            baby = i.make_babies(entity)
            if baby:
                entity.extend(baby)
                b = True
        i.draw(canvas)
    root.after(100, update)


root.after(100, update)
root.mainloop()
