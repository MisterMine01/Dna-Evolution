from tkinter import *
from core.entities.BasesEntity import BasesEntity

root = Tk()
root.title("Canvas")
root.attributes("-fullscreen", True)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

root.update_idletasks()


canvas = Canvas(root, bg="white", width=root.winfo_width(), height=root.winfo_height())
canvas.pack()

entity: list[BasesEntity] = []

for i in range(10):
    entity.append(BasesEntity())

def update():
    global entity
    canvas.delete("all")
    for i in entity:
        i.move()
        i.draw(canvas)
    root.after(100, update)


root.after(100, update)
root.mainloop()
