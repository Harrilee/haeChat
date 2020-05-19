from tkinter import *
import threading
import json
from chat_utils import *
from tkinter import messagebox

def main(self):
    # --------------------------------------------functions-------------------------------------------- #
    def initial_task():
        input_thread = threading.Thread(target=looptask)
        input_thread.daemon = True
        input_thread.start()

    def looptask():
        msg = json.dumps({"action": "game", "from": self.name, 'to': self.to})
        mysend(self.socket, msg)
        while self.sm.get_state() != S_OFFLINE:
            my_msg, peer_msg = self.get_msgs()
            output(my_msg, peer_msg)


    def output(my_msg, peer_msg):  # this function maps the received message to the tk window

        if len(peer_msg) > 0:
            peer_msg = json.loads(peer_msg)
            if peer_msg['action'] == 'exchange_g':
                text1.insert(END,peer_msg['message'])

    def button1_click():
        msg = json.dumps({"action": "exchange_g", "from": self.name, 'choice': 'h'})
        mysend(self.socket, msg)

    def button2_click():
        msg = json.dumps({"action": "exchange_g", "from": self.name, 'choice': 's'})
        mysend(self.socket, msg)

    window = Tk()
    window.iconbitmap('logo.ico')
    window.title('BlackJack')

    text1 = Text(window, height=20, width=50)
    text1.pack(padx=30, pady=20)

    frame1=Frame(window)
    frame1.pack(padx=30, pady=10)

    button1=Button(frame1, text='Hit', width=15, command=button1_click)
    button1.pack(side=LEFT, padx=10, pady=10)

    button2=Button(frame1, text='Hold', width= 15, command=button2_click)
    button2.pack(side=RIGHT, padx=10, pady=10)

    window.after(0, initial_task)
    window.mainloop()

if __name__ == '__main__':
    main(0)