from tkinter import *
root=Tk()
text1=Text(root)
text1.insert(END,'asdasfsafasfasf\nasfassfasfsafas')
print(text1.get(0.0, END))
mainloop()
