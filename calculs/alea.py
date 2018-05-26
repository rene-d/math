from tkinter import *
import platform
import subprocess
import os
import random


def raise_app():
    if platform.system() == 'Darwin':
        subprocess.call([
            '/usr/bin/osascript', '-e',
            'tell app "System Events" to set frontmost of every process whose unix id is {} to true'.format(os.getpid())  # noqa
        ])


n1, n2 = 3.14159, 2.71828
sign = "+"

window = Tk()
window.title("Entrainement au calcul décimal")
window.geometry('600x400')

alea = StringVar()
alea.set(str(n1))
lbl = Label(window, textvariable=alea, font=("Andale Mono", 50))
lbl.pack()

plus = StringVar()
plus.set(sign)
lbl1 = Label(window, textvariable=plus, font=("Andale Mono", 50))
lbl1.pack()

alea2 = StringVar()
alea2.set(str(n2))
lbl2 = Label(window, textvariable=alea2, font=("Andale Mono", 50))
lbl2.pack()

egal = Label(window, text="=", font=("Andale Mono", 50))
egal.pack()

alea3 = StringVar()
alea3.set("?")
lbl3 = Label(window, textvariable=alea3, font=("Andale Mono", 50))
lbl3.pack()


def callback(event):
    global n1, n2, sign
    if event.keysym == "Return":
        sign = "+" if random.randint(0, 1) == 0 else "-"
        n1 = round(random.random(), 5) + random.randint(99, 99999)
        n2 = round(random.random(), 5) + random.randint(99, 99999)
        alea3.set("?")
        alea.set(str(n1))
        plus.set(sign)
        alea2.set(str(n2))
    elif event.keysym == "equal":
        if sign == "+":
            x = n1 + n2
        else:
            x = n1 - n2
        alea3.set(str(round(x, 5)))


window.bind('<Key>', callback)

raise_app()
window.mainloop()
