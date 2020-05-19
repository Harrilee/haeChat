"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp
import send_code
from random import randint
from blackjack import *


class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        self.codes = {}

    def start_black(self):
        print('starting game')
        game(self.a, self.b)
        print('start game')

    def send_code(self, email):
        code = ''
        for i in range(6):
            code += str(randint(0, 9))
        print(code)
        send_code.send_code(email, code)
        self.codes[email] = code
        return True

    def new_client(self, sock):
        # add to all sockets and to new clients
        # print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        # read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    password = msg['password']

                    if self.group.validate(name, password) == True:
                        # move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        # add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        # load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name] = pkl.load(
                                    open(name + '.idx', 'rb'))
                            except IOError:  # chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        # self.group.join(name, password)
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "ok"}))
                    else:  # the password is incorrect
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "false"}))
                        print(name + ' Incorrect username or password')
                elif msg["action"] == "name_validation":
                    if self.group.is_member(msg['name']):
                        mysend(sock, json.dumps({"action": "name_validation", "status": "duplicated"}))
                    else:
                        mysend(sock, json.dumps({"action": "name_validation", "status": "ok"}))
                elif msg['action'] == "send_code_request":
                    try:
                        self.send_code(msg['email'])
                        mysend(sock, json.dumps({"action": "send_code_request", "status": "ok"}))
                    except:
                        mysend(sock, json.dumps({"action": "send_code_request", "status": "wrong"}))
                elif msg['action'] == "send_code_request_given_name":
                    print('send_code_request_given_name')
                    try:
                        email = self.group.members[msg['name']].email
                        self.send_code(email)
                        mysend(sock,
                               json.dumps({"action": "send_code_request_given_name", "status": "ok", 'email': email}))
                        print('message sent')
                    except:
                        mysend(sock, json.dumps({"action": "send_code_request_given_name", "status": "wrong"}))
                        print('sent failed')
                elif msg['action'] == 'code_validate':
                    if msg['code'] == self.codes[msg['email']]:
                        mysend(sock, json.dumps({"action": "code_validate", "status": "ok"}))
                    else:
                        mysend(sock, json.dumps({"action": "code_validate", "status": "wrong"}))
                elif msg['action'] == 'code_validate_given_name':
                    email = self.group.members[msg['name']].email
                    if msg['code'] == self.codes[email]:
                        mysend(sock, json.dumps({"action": "code_validate_given_name", "status": "ok"}))
                    else:
                        mysend(sock, json.dumps({"action": "code_validate_given_name", "status": "wrong"}))
                elif msg['action'] == "register":
                    try:
                        self.group.join(msg['name'], msg['password'], msg['email'])
                        mysend(sock, json.dumps({"action": "register", "status": "ok"}))
                    except:
                        mysend(sock, json.dumps({"action": "register", "status": "wrong"}))
                        print('A problem occurred while registering.')
                elif msg['action'] == "reset":
                    try:
                        email = self.group.members[msg['name']].email
                        self.group.join(msg['name'], msg['password'], email)
                        mysend(sock, json.dumps({"action": "reset", "status": "ok"}))
                    except:
                        mysend(sock, json.dumps({"action": "reset", "status": "wrong"}))
                        print('A problem occurred while registering.')
                else:
                    print('wrong code received')
            else:  # client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

    # ==============================================================================
    # main command switchboard
    # ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        msg = myrecv(from_sock)
        #print(msg)
        name = self.logged_sock2name[from_sock]
        group_name_list = []
        for each_number in self.group.members[name].groups:
            group_name_list.append(self.group.chat_grps[each_number]['name'])
        mysend(from_sock, json.dumps(
            {"action": "refresh_list", "users": list(self.group.members.keys()),
             'groups': group_name_list}))
        if len(msg) > 0:
            # ==============================================================================
            # handle connect request this is implemented for you
            # ==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action": "connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps(
                        {"action": "connect", "status": "success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps(
                            {"action": "connect", "status": "request", "from": from_name}))
                else:
                    msg = json.dumps(
                        {"action": "connect", "status": "no-user"})
                mysend(from_sock, msg)
            # ==============================================================================
            # handle messeage exchange: IMPLEMENT THIS
            # ==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                """
                Finding the list of people to send to and index message
                """
                # IMPLEMENTATION
                # ---- start your code ---- #
                msg_text = text_proc(msg['message'], from_name)
                self.indices[from_name].add_msg_and_index(msg_text)
                # ---- end of your code --- #
                if msg['type'] == 'group':
                    the_guys = self.group.chat_grps[self.group.name2group[msg['to']]]['members']
                    for g in the_guys:
                        if g == msg['from']:
                            continue
                        try:
                            to_sock = self.logged_name2sock[g]
                            mysend(to_sock, json.dumps(
                                {"action": "exchange", "from": from_name, 'to': msg['to'], "message": msg_text,
                                 'type': msg['type']}))
                        except:
                            print(g, 'is not online')
                elif msg['type'] == 'user':
                    try:
                        to_sock = self.logged_name2sock[msg['to']]
                        mysend(to_sock, json.dumps(
                            {"action": "exchange", "from": from_name, "message": msg_text, 'type': msg['type']}))
                    except:
                        mysend(from_sock, json.dumps(
                            {"action": "exchange", "from": msg['to'], "message": '(User is offline)\n\n',
                             'type': msg['type']}))
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                # self.indices[g].add_msg_and_index(msg_text)

                # ---- end of your code --- #

            # ==============================================================================
            # the "from" guy has had enough (talking to "to")!
            # ==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps(
                        {"action": "disconnect", "message": "everyone left, you are alone\n"}))
            # ==============================================================================
            #                 listing available peers: IMPLEMENT THIS
            # ==============================================================================
            elif msg["action"] == "list":

                # IMPLEMENTATION
                # ---- start your code ---- #
                msg = self.group.list_all(self.logged_sock2name[from_sock])
                # msg = "...needs to use self.group functions to work"

                # ---- end of your code --- #
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": msg}))
            # ==============================================================================
            #             retrieve a sonnet : IMPLEMENT THIS
            # ==============================================================================
            elif msg["action"] == "poem":

                # IMPLEMENTATION
                # ---- start your code ---- #
                # pass
                poem = self.sonnet.get_poem(int(msg['target']))
                print('here:\n', poem)

                # ---- end of your code --- #

                mysend(from_sock, json.dumps(
                    {"action": "poem", "results": poem}))
            # ==============================================================================
            #                 time
            # ==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps(
                    {"action": "time", "results": ctime}))
            # ==============================================================================
            #                 search: : IMPLEMENT THIS
            # ==============================================================================
            elif msg["action"] == "search":

                # IMPLEMENTATION
                # ---- start your code ---- #
                from_name = self.logged_sock2name[from_sock]
                search_rslt = str(self.indices[from_name].search(msg['target']))
                print('server side search: ' + search_rslt)

                # ---- end of your code --- #
                mysend(from_sock, json.dumps(
                    {"action": "search", "results": search_rslt}))
            # ==============================================================================
            #                 the "from" guy really, really has had enough
            # ==============================================================================
            elif msg['action'] == 'create_group':
                self.group.new_group(msg['name'], msg['member'])
            elif msg['action'] == 'edit_group':
                self.group.edit_group(msg['new_name'], msg['member'], msg['old_name'])
            elif msg['action'] == 'member_list':
                mysend(from_sock, json.dumps(
                    {"action": "member_list",
                     "member_list": self.group.chat_grps[self.group.name2group[msg['to']]]['members']}))
                print(self.group.chat_grps[self.group.name2group[msg['to']]]['members'])
            elif msg['action'] == 'leave_group':
                self.group.delete_people(msg['from'], msg['to'])
            elif msg['action'] == 'delete_group':
                self.group.delete_group_name(msg['to'])
            elif msg['action'] == 'refresh_list':
                pass
            elif msg['action'] == 'game':
                try:
                    self.group.members[msg['from']].game_status = 'prepared'
                    if self.group.members[msg['to']].game_status == 'prepared':
                        self.a = Players(msg['to'], self.logged_name2sock[msg['to']])
                        self.b = Players(msg['from'], self.logged_name2sock[msg['from']])
                        a_thread = threading.Thread(target=self.start_black)
                        a_thread.daemon = True
                        a_thread.start()
                        self.group.members[msg['from']].game_status = 'not prepared'
                        self.group.members[msg['to']].game_status = 'not prepared'
                except:
                    pass
            elif msg['action'] == 'exchange_g':
                if self.a.name == msg['from']:
                    self.a.action = msg['choice']
                if self.b.name == msg['from']:
                    self.b.action = msg['choice']
            else:
                print(msg)
                # client died unexpectedly
                self.logout(from_sock)

                # ==============================================================================
                # main loop, loops *forever*
                # ==============================================================================

    def run(self):
        print('starting server...')
        while (1):
            read, write, error = select.select(self.all_sockets, [], [])
            # print('checking logged clients..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            # print('checking new clients..')
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            # print('checking for new connections..')
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
