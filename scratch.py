from tkinter import *
import tkinter as tk
from tkinter import ttk

first = Tk()
first.geometry("132x110")

textboxes = tk.Canvas(first, width = 430, height = 330,  relief = 'raised')
textboxes.pack()
lbel = tk.Label(first, text='Welcome To My Domain:')
lbel.config(font=('helvetica', 17))
textboxes.create_window(213, 104, window=lbel)
e = tk.Entry (first)
textboxes.create_window(303, 146, window=e)
frm = Frame(first)
frm.pack()
frm1 = Frame(first)
frm1.pack(side = RIGHT)
frm2 = Frame(first)
frm2.pack(side = LEFT)
# imge = PhotoImage(file = r"C:\Users\Kripya-PC\Downloads\MicrosoftTeams-image (11).png")
# Button(first, text = 'Have a Nice Day !', image = imge).pack(side = LEFT)
# labels=Label(first, image=imge, width=320, height=350)
# labels.pack(side=BOTTOM)
btn1=Button(first, text=" +" )
btn1.pack(side=TOP)
btn2=Button(first, text=" - ")
btn2.pack(side=RIGHT)
first.mainloop()
