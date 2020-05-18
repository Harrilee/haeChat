from tkinter import *
import window_register
import window_reset
from chat_utils import *
import json


def login(self):
    def login_fun():
        if entry2.get() == '' or entry1.get() == '':
            string_label5.set('Please enter your username and password.')
            return False
        try:
            '''get the password and username validated'''
            # ----------------------------------------------------------#
            self.name = entry1.get()
            msg = json.dumps({"action": "login", "name": entry1.get(), 'password': entry2.get()})
            self.send(msg)
            response = json.loads(self.recv())
            # ----------------------------------------------------------#
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                login.destroy()
                return True
            elif response["status"] == 'false':
                string_label5.set('Incorrect username or password.')
                return False
        except KeyError:
            string_label5.set('Incorrect username or password.')

    def register(event):
        return window_register.register_window(self)

    def reset(event):
        return window_reset.reset_window(self)

    login = Tk()
    login.iconbitmap('logo.ico')
    username_entry = StringVar()
    password_entry = StringVar()
    string_label5 = StringVar()
    login.title('haeChat Login')
    frame1 = Frame(login)
    label0 = Label(frame1, text="haeChat", padx=10, pady=20, font=('Arial', 20))
    label0.grid(row=0, column=1)
    label1 = Label(frame1, text="Username:", padx=10, pady=0)
    label1.grid(row=1, column=0, sticky=W)
    label2 = Label(frame1, text='Password:', padx=10, pady=10)
    label2.grid(row=2, column=0, sticky=W)
    label3 = Label(frame1, text='Create', fg='blue', padx=20, pady=0)
    label3.grid(row=1, column=2, sticky=W)
    label3.bind("<Button-1>", register)
    label4 = Label(frame1, text='Forget', fg='blue', padx=20, pady=10)
    label4.grid(row=2, column=2, sticky=W)
    label4.bind("<Button-1>", reset)

    entry1 = Entry(frame1, textvariable=username_entry)

    entry2 = Entry(frame1, textvariable=password_entry, show='●')
    entry1.grid(row=1, column=1, padx=10, pady=10)
    entry2.grid(row=2, column=1, padx=10, pady=10)
    button1 = Button(frame1, text='Login', width=10, command=login_fun)
    button1.grid(row=3, column=1, pady=10)
    frame1.pack()
    label5 = Label(login, textvariable=string_label5, padx=20, pady=10)
    label5.pack()
    login.mainloop()


if __name__ == '__main__':
    login()
