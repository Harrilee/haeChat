from tkinter import *
from tkinter import messagebox
import socket
import time
import client_state_machine as csm
import threading
from chat_utils import *
import select
import json


def chat(self):
    # --------------------------------------------functions-------------------------------------------- #
    def initial_task():
        input_thread = threading.Thread(target=looptask)
        input_thread.daemon = True
        input_thread.start()

    def looptask():
        msg = json.dumps({"action": "refresh_list", "from": self.name})
        mysend(self.socket, msg)
        while self.sm.get_state() != S_OFFLINE:
            my_msg, peer_msg = self.get_msgs()
            output(my_msg, peer_msg)
            time.sleep(CHAT_WAIT)

    def output(my_msg, peer_msg):  # this function maps the received message to the tk window
        if len(my_msg) > 0:  # my stuff going out
            try:
                if self.to == '':
                    0/0
                msg = json.dumps({"action": "exchange", "from": self.name, 'type': self.type, \
                                  'to': self.to, "message": my_msg})
                mysend(self.socket, msg)
                current_time = time.localtime()
                display = 'Me ' + time.strftime('%H:%M:%S', time.localtime()) + '\n' + my_msg + '\n'
                try:
                    self.chat_history[self.to] = \
                        self.chat_history[self.to] + display
                except KeyError:
                    self.chat_history[self.to] = display
                print('message sent:', msg)
            except:
                messagebox.showerror('Warning', 'Please select a person to send.')
                return

        if len(peer_msg) > 0:
            peer_msg = json.loads(peer_msg)
            print(peer_msg)
            # -----------------------------deal with user and group list-----------------------------------#
            try:
                if peer_msg['users'] != self.user:
                    self.user = peer_msg['users']
                if peer_msg['groups'] != self.group:
                    self.group = peer_msg['groups']
                listbox1.delete(0, END)
                if self.type == 'group':
                    for each in self.group:
                        listbox1.insert(END, each)
                elif self.type == 'user':
                    for each in self.user:
                        if each!=self.name:
                            listbox1.insert(END, each)
            except:
                pass
            # --------------------------store local chat history with chat_history---------------------------#
            try:
                self.chat_history[peer_msg['from']] = \
                    self.chat_history[peer_msg['from']] + peer_msg['message']
                print('message received:', peer_msg)
            except Exception as inst:
                try:
                    print(inst)
                    self.chat_history[peer_msg['from']] = peer_msg['message']
                    print('message received:', peer_msg)
                except:
                    print('failed to process message:', peer_msg)

        # --------------------------update text2 with chat_history----------------------------------------------#

        try:
            if text1.get(0.0, END) != self.chat_history[self.to]+'\n':
                text1.delete(0.0, END)
                text1.insert(END, self.chat_history[self.to])
        except KeyError:
            self.chat_history[self.to]=''
            text1.insert(END, self.chat_history[self.to])

    def button4_click():
        self.console_input.append(text2.get(0.0, END))
        text2.delete(0.0, END)

    def button3_click():
        self.type = 'group'
        listbox1.delete(0, END)
        for each in self.group:
            listbox1.insert(END, each)

    def button2_click():
        self.type = 'user'
        listbox1.delete(0, END)
        for each in self.user:
            if each!=self.name:
                listbox1.insert(END, each)

    def refresh_selection(x):
        selection=listbox1.curselection()
        if selection!=():
            self.to=listbox1.get(selection)
            label1_string.set(self.to)


    # -----------------------------------------------end---------------------------------------------- #

    # --------------------------------------------UI_Setup-------------------------------------------- #
    chat_window = Tk()
    chat_window.iconbitmap('logo.ico')
    chat_window.title('haeChat'+' ['+self.name+']')

    frame4 = Frame(chat_window)
    frame4.pack(fill=X, anchor=W)

    entry1_string = StringVar()
    entry1 = Entry(frame4, textvariable=entry1_string)
    entry1_string.set('Type here to search...')
    entry1.place(relwidth=1)

    button1 = Button(frame4, width=10, text='Search')
    button1.pack(side=RIGHT)

    pan1 = PanedWindow(chat_window, orient=HORIZONTAL)
    pan1.pack(anchor=W, fill=BOTH)

    frame1 = Frame(pan1)
    pan1.add(frame1)

    frame2 = Frame(pan1)
    pan1.add(frame2)

    listbox1 = Listbox(frame1, height=20, width=30)
    listbox1.bind("<Button-1>", refresh_selection)
    listbox1.pack(fill=X)

    frame3 = Frame(frame1, height=30)
    frame3.pack(fill=BOTH, side=BOTTOM)

    button2 = Button(frame3, width=10, text='User', command=button2_click)
    button2.place(rely=0.5, relx=0, relwidth=0.5, anchor=W, relheight=1)

    button3 = Button(frame3, width=10, text='Group', command=button3_click)
    button3.place(rely=0.5, relx=0.5, relwidth=0.5, anchor=W, relheight=1)

    label1_string = StringVar()
    label1_string.set('User')
    label1 = Label(frame2, textvariable=label1_string)
    label1.pack(anchor=W)

    pan2 = PanedWindow(frame2, orient=VERTICAL)
    pan2.pack(fill=BOTH)

    text1 = Text(height=20)
    pan2.add(text1)

    text2 = Text(height=5)
    pan2.add(text2)

    button4 = Button(chat_window, text='Send', width=10, command=button4_click)
    button4.place(anchor=SE, relx=1, rely=1, height=25, width=80)

    chat_window.after(0, initial_task)
    chat_window.mainloop()
    # -----------------------------------------------end---------------------------------------------- #


if __name__ == '__main__':
    chat(0)