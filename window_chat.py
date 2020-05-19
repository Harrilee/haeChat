from tkinter import *
from tkinter.font import *
from tkinter import messagebox
import socket
import time
import client_state_machine as csm
import threading
from chat_utils import *
import select
import json
import window_add_group
import window_modify_group
import window_game_menu
import window_emoji


def chat(self):
    # --------------------------------------------functions-------------------------------------------- #
    def initial_task():
        input_thread = threading.Thread(target=looptask)
        input_thread.daemon = True
        input_thread.start()

    def looptask():
        msg = json.dumps({"action": "refresh_list", "from": self.name})
        mysend(self.socket, msg)
        button2_click()
        while self.sm.get_state() != S_OFFLINE:
            # set button5
            if self.to != '':
                button5.pack(side=RIGHT)
            else:
                button5.pack_forget()
                label1_string.set('')
            my_msg, peer_msg = self.get_msgs()
            output(my_msg, peer_msg)
            msg = json.dumps({"action": "refresh_list", "from": self.name})
            mysend(self.socket, msg)
            my_msg, peer_msg = self.get_msgs()
            output(my_msg, peer_msg)
            time.sleep(CHAT_WAIT)

    def output(my_msg, peer_msg):  # this function maps the received message to the tk window
        if len(my_msg) > 0:  # my stuff going out
            try:
                if self.to == '':
                    0 / 0
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
            # -----------------------------deal with user and group list-----------------------------------#
            try:
                if peer_msg['users'] == self.user and peer_msg['groups'] == self.group:
                    0 / 0
                if peer_msg['users'] != self.user:
                    self.user = peer_msg['users']
                if peer_msg['groups'] != self.group:
                    self.group = peer_msg['groups']
                listbox1.delete(0, END)
                if self.type == 'group':
                    for each in self.group:
                        listbox1.insert(END, each)
                    listbox1.insert(END, '*Add a group...')
                elif self.type == 'user':
                    for each in self.user:
                        if each != self.name:
                            listbox1.insert(END, each)
            except:
                pass
            # --------------------------store local chat history with chat_history---------------------------#
            if peer_msg['action'] == 'exchange':
                try:
                    if peer_msg['type'] == 'user':
                        self.chat_history[peer_msg['from']] = \
                            self.chat_history[peer_msg['from']] + peer_msg['message']
                    if peer_msg['type'] == 'group':
                        self.chat_history[peer_msg['to']] = \
                            self.chat_history[peer_msg['to']] + peer_msg['message']
                    print('message received:', peer_msg)
                except Exception as inst:
                    try:
                        print(inst)
                        if peer_msg['type'] == 'user':
                            self.chat_history[peer_msg['from']] = peer_msg['message']
                        if peer_msg['type'] == 'group':
                            self.chat_history[peer_msg['to']] = peer_msg['message']
                        print('message received:', peer_msg)
                    except:
                        pass
            elif peer_msg['action'] == 'member_list':
                self.member_list=peer_msg['member_list']
                print('member_list:', peer_msg)
        # --------------------------update text2 with chat_history----------------------------------------------#


        try:
            if text1.get(0.0, END) != self.chat_history[self.to] + '\n':
                text1.delete(0.0, END)
                text1.insert(END, self.chat_history[self.to])
        except KeyError:
            self.chat_history[self.to] = ''
            text1.insert(END, self.chat_history[self.to])
        except:
            self.chat_history[self.to] = '[system] Your friend sent an emoji.\n\n'
            text1.insert(END, self.chat_history[self.to])
            

    def button4_click():
        self.console_input.append(text2.get(0.0, END))
        text2.delete(0.0, END)

    def button3_click():
        label2_string.set('Group')
        self.type = 'group'
        self.to = ''
        listbox1.delete(0, END)
        button5_string.set('Group Settings')
        for each in self.group:
            listbox1.insert(END, each)
        listbox1.insert(END, '*Add a group...')

    #game button
    def button2_click():
        self.type = 'user'
        self.to = ''
        label2_string.set('User')
        listbox1.delete(0, END)
        button5_string.set('Play Game')
        for each in self.user:
            if each != self.name:
                listbox1.insert(END, each)

    def button5_click():
        if button5_string.get()=='Group Settings':
            msg = json.dumps({"action": "member_list", "from": self.name, 'to': self.to})
            mysend(self.socket, msg)
            while True:
                my_msg, peer_msg = self.get_msgs()
                if len(peer_msg)==0:
                    continue
                peer_msg = json.loads(peer_msg)
                if peer_msg['action'] == 'member_list':
                    self.member_list = peer_msg['member_list']
                    print('member_list:', peer_msg)
                    break
            window_modify_group.main(self, self.to, self.member_list)
            self.to = ''
        elif button5_string.get()=='Play Game':
            window_game_menu.main(self)

    def button6_click():
        window_emoji.main(text2)

    def refresh_selection(x):
        selection = listbox1.curselection()
        if selection != ():
            if listbox1.get(selection) == '*Add a group...':
                button3_click()
                window_add_group.main(self)

            else:
                self.to = listbox1.get(selection)
                label1_string.set(self.to)

    # -----------------------------------------------end---------------------------------------------- #

    # --------------------------------------------UI_Setup-------------------------------------------- #
    chat_window = Tk()
    chat_window.iconbitmap('logo.ico')
    chat_window.title('haeChat' + ' [' + self.name + ']')

    frame4 = Frame(chat_window)
    frame4.pack(fill=X, anchor=W)

    entry1_string = StringVar()
    entry1 = Entry(frame4, textvariable=entry1_string)
    entry1_string.set('Type here to search...')
    entry1.place(relwidth=1, y=5)

    button1 = Button(frame4, width=10, height=1, text='Search')
    button1.pack(side=RIGHT, fill=Y)

    canvas1 = Canvas(chat_window, height=10)
    canvas1.create_line(0, 10, 800, 10, width=2, fill='grey')
    canvas1.pack(fill=X)

    pan1 = PanedWindow(chat_window, orient=HORIZONTAL)
    pan1.pack(anchor=W, fill=BOTH)

    frame1 = Frame(pan1)
    pan1.add(frame1)

    frame2 = Frame(pan1)
    pan1.add(frame2)

    label2_string = StringVar()
    label2 = Label(frame1, textvariable=label2_string, font=Font(font='Arial', size=12))
    label2.pack(anchor=W, fill=Y)

    listbox1 = Listbox(frame1, height=20, width=30)
    listbox1.bind("<Button-1>", refresh_selection)
    listbox1.pack(fill=X)

    frame3 = Frame(frame1, height=30)
    frame3.pack(fill=BOTH, side=BOTTOM)

    button2 = Button(frame3, width=10, text='User', command=button2_click)
    button2.place(rely=0.5, relx=0, relwidth=0.5, anchor=W, relheight=1)

    button3 = Button(frame3, width=10, text='Group', command=button3_click)
    button3.place(rely=0.5, relx=0.5, relwidth=0.5, anchor=W, relheight=1)

    frame5 = Frame(frame2)
    frame5.pack(fill=X)

    label1_string = StringVar()
    label1_string.set('')
    label1 = Label(frame5, textvariable=label1_string, font=Font(font='Arial', size=12))
    label1.pack(side=LEFT)

    button5_string = StringVar()
    button5 = Button(frame5, width=15, textvariable=button5_string, command=button5_click)

    pan2 = PanedWindow(frame2, orient=VERTICAL)
    pan2.pack(fill=BOTH)

    text1 = Text(height=21)
    pan2.add(text1)  

    text2 = Text(height=5)
    pan2.add(text2)

    button4 = Button(chat_window, text='Send', width=10, command=button4_click)
    button4.place(anchor=SE, relx=1, rely=1, height=25, width=80)
    
    emoji_frame = Button(chat_window, text = '\ud83d\ude00', width=4, command=button6_click)
    emoji_frame.place(anchor = S, rely = 1, relx = 0.8, x = 65)

    chat_window.after(0, initial_task)
    chat_window.mainloop()
    # -----------------------------------------------end---------------------------------------------- #


if __name__ == '__main__':
    chat(0)
