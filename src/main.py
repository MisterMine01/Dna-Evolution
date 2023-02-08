from tkinter import *
from core.entities import BasesEntity
import random

root = Tk()
root.title("Canvas")
 #root.attributes("-fullscreen", True)
root.geometry(f"{root.winfo_screenwidth()//2}x{root.winfo_screenheight()//2}")

root.update_idletasks()


canvas = Canvas(root, bg="white", width=root.winfo_width(), height=root.winfo_height())
canvas.pack()

entity: list[BasesEntity] = []


for i in range(10):
    entity_new = BasesEntity()
    entity.append(entity_new)
    entity[-1].x = random.randint(0, root.winfo_width())
    entity[-1].y = random.randint(0, root.winfo_height())


log = open("log.txt", "w")

log_data = []
log_refrech = 0

def update():
    global entity, log_refrech, log_data, log
    b = False
    canvas.delete("all")
    if log_refrech > 100:
        log.write("\n".join(log_data))
        log_data.clear()
        log.flush()
        log_refrech = 0
    for i in entity:
        if i.x < 0 or i.x > root.winfo_width() or i.y < 0 or i.y > root.winfo_height():
            i.x = random.randint(0, root.winfo_width())
            i.y = random.randint(0, root.winfo_height())
        i.move()
        i.is_dead()
        if not b:
            baby = i.make_babies(entity)
            if baby[0] is not None and len(baby[1]) > 0:
                entity.extend(baby[1])
                b = True
                men = i if i.sex else baby[0]
                women = baby[0] if i.sex else i
                print(men.get_names() + " + " + women.get_names())
                print(" -> " + " + ".join([i.get_names() for i in baby[1]]))
                log_data.append(str(men) + " + " + str(women) + " -> " + str(baby[1]))
                log_refrech += 1
        i.draw(canvas)
    
    root.after(100, update)


root.after(100, update)
root.mainloop()
