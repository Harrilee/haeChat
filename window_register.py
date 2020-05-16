from tkinter import *
import json


def register_window(self):
    register_window = Toplevel()
    register_window.iconbitmap('logo.ico')

    def register_button_click():
        button2.focus_set()
        validated = True
        if not username_validate(entry1.get()):
            validated = False
        if entry1.get() == '':
            string1.set('Please enter your username.')
            validated = False
        if entry2.get() == '':
            string2.set('Please enter your password.')
            validated = False
        if entry3.get() != entry2.get():
            string3.set('The password inputs are not consistent.')
            validated = False
        if entry2.get() == '':
            string3.set('Please enter your password.')
            validated = False
        if entry4.get() == '':
            string4.set('Please enter your email.')
            validated = False
        if not code_validate():
            validated = False
        if entry5.get() == '':
            string5.set('Please enter the code sent to your mailbox.')
            validated = False
        if not validated:
            return False
        else:
            '''send register info'''
            # ----------------------------------------------------------#
            msg = json.dumps({"action": "register", "email": entry4.get(), 'name': entry1.get(),\
                              'password':entry2.get()})
            self.send(msg)
            response = json.loads(self.recv())
            # ----------------------------------------------------------#
            if response["status"] == 'ok':
                register_window.destroy()
                return True
            elif response["status"] == 'wrong':
                print('Validation Failed')
                return False

    def code_validate():
        if entry5.get() == '':
            string5.set('')
            return False
        '''send "send code" request'''
        # ----------------------------------------------------------#
        msg = json.dumps({"action": "code_validate", "email": entry4.get(), 'code': entry5.get()})
        self.send(msg)
        response = json.loads(self.recv())
        # ----------------------------------------------------------#
        if response["status"] == 'ok':
            string5.set('√')
            return True
        elif response["status"] == 'wrong':
            string5.set('Invalid code.')
            return False

    CMDcode_validate = register_window.register(code_validate)

    def send_button_click():
        if entry4.get()=='':
            string4.set('Please enter your email address.')
            return
        button1.focus_set()
        '''send "send code" request'''
        # ----------------------------------------------------------#
        msg = json.dumps({"action": "send_code_request", "email": entry4.get()})
        self.send(msg)
        response = json.loads(self.recv())
        # ----------------------------------------------------------#
        if response["status"] == 'ok':
            string4.set('Successfully sent.')
        elif response["status"] == 'wrong':
            string4.set('A problem occurred.')
        # except:string4='Error: please check...'
        # else:string4='Successfully sent.'

    def username_validate(input):
        if input == '':
            string1.set('')
            return False
        if username_duplicate_validation(input):
            string1.set('√')
            return True
        else:
            string1.set('The name is registered.')
            return False

    def username_duplicate_validation(input):
        '''get the username validated'''
        # ----------------------------------------------------------#
        msg = json.dumps({"action": "name_validation", "name": input})
        self.send(msg)
        response = json.loads(self.recv())
        # ----------------------------------------------------------#
        if response["status"] == 'ok':
            return True
        elif response["status"] == 'duplicated':
            return False

    CMDusername_validate = register_window.register(username_validate)

    def confirm_validate():
        if entry3.get() == '' or entry2.get() == '':
            string3.set('')
            return False
        if entry3.get() == entry2.get():
            string3.set('√')
            return True
        else:
            string3.set('The password inputs are not consistent.')
            return False

    CMDconfirm_validate = register_window.register(confirm_validate)

    string1 = StringVar()
    string2 = StringVar()
    string3 = StringVar()
    string4 = StringVar()
    string5 = StringVar()
    register_window.title('Register')
    label0 = Label(register_window, text="Create a New Account", padx=10, pady=20, font=('Arial', 15))
    label0.pack()
    frame2 = Frame(register_window)
    label1 = Label(frame2, text="Username:", padx=10, pady=0)
    label1.grid(row=0, column=0, sticky=W)
    label1_r = Label(frame2, padx=10, pady=0, textvariable=string1, justify=LEFT)
    label1_r.grid(row=0, column=2, sticky=W)
    label2 = Label(frame2, text='Password:', padx=10, pady=10)
    label2.grid(row=1, column=0, sticky=W)
    label2_r = Label(frame2, padx=10, pady=10, textvariable=string2, justify=LEFT)
    label2_r.grid(row=1, column=2, sticky=W)
    label3 = Label(frame2, text='Confirm Password:', padx=10, pady=10)
    label3.grid(row=2, column=0, sticky=W)
    label3_r = Label(frame2, padx=10, pady=10, textvariable=string3, justify=LEFT)
    label3_r.grid(row=2, column=2, sticky=W)
    label4 = Label(frame2, text='Email Address:', padx=10, pady=10)
    label4.grid(row=3, column=0, sticky=W)
    label4_r = Label(frame2, padx=10, pady=10, textvariable=string4, justify=LEFT)
    label4_r.grid(row=3, column=2, sticky=W)
    label5 = Label(frame2, text='Verification Code:', padx=10, pady=10)
    label5.grid(row=4, column=0, sticky=W)
    label5_r = Label(frame2, padx=10, pady=10, textvariable=string5, justify=LEFT)
    label5_r.grid(row=4, column=2, sticky=W)
    entry1 = Entry(frame2, width=35, validate='focusout', validatecommand=(CMDusername_validate, '%P'))
    entry1.grid(row=0, column=1, padx=10, pady=10, sticky=W)
    entry2 = Entry(frame2, show='●', width=35, validate='focusout', validatecommand=CMDconfirm_validate)
    entry2.grid(row=1, column=1, padx=10, pady=10, sticky=W)
    entry3 = Entry(frame2, show='●', width=35, validate='focusout', validatecommand=CMDconfirm_validate)
    entry3.grid(row=2, column=1, padx=10, pady=10, sticky=W)
    entry4 = Entry(frame2)
    entry4.grid(row=3, column=1, padx=10, pady=10, sticky=W)
    button1 = Button(frame2, text='Send Code', command=send_button_click)
    button1.grid(row=3, column=1, padx=10, pady=10, sticky=E)
    entry5 = Entry(frame2, width=35, validate='focusout', validatecommand=CMDcode_validate)
    entry5.grid(row=4, column=1, padx=10, pady=10, sticky=W)
    frame2.pack()
    button2 = Button(register_window, text='Register', width=10, command=register_button_click)
    button2.pack(padx=10, pady=10)
    register_window.mainloop()
