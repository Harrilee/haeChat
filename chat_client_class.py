import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm

import threading

import window_login
import window_chat


class Client:
    def __init__(self, args):
        self.name = ''
        self.user = ['Alice', 'Bob']
        self.group = ['Group 1', 'Group 2']
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        self.type = ''  # 'user' / 'group'
        self.to = ''  # username or group name
        self.chat_history = {}

    def login(self):
        return window_login.login(self)

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text)  # no need for lock, append is thread safe

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        # peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def chat(self):
        return window_chat.chat(self)

    def run_chat(self):
        self.init_chat()
        self.login()
        self.system_msg += 'Welcome, ' + self.name + '!'
        self.output()
        self.chat()

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.system_msg = ''

    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
