import tkinter as tk
from tkinter import messagebox

main_window = tk.Tk()
main_window.geometry('200x100')

tk.Label(main_window, text='我是一个窗口').pack()

def my_close():
    # True or Flase
    res = messagebox.askokcancel('提示', '是否关闭窗口')
    if res == True:
        main_window.destroy()

# 为右上角的关闭事件添加一个响应函数
main_window.protocol('WM_DELETE_WINDOW', my_close)

main_window.mainloop()