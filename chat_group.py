# -*- coding: utf-8 -*-
import time
import pickle as pkl

S_ALONE = 0
S_TALKING = 1


class User():
    def __init__(self, name, password, email, status=S_ALONE):
        self.name = name
        self.password = password
        self.email = email
        self.time = (time.localtime(), time.timezone)
        self.status = S_ALONE
        self.groups = []

    def __str__(self):
        out = ''
        out += 'Name:' + self.name
        out += '\nPassword:' + self.password
        out += '\nEmail:' + self.email
        out += '\nTime:' + str(self.time) + '\n'
        return out


class Group:

    def __init__(self):
        try:
            self.members = pkl.load(open('user_info.dat', 'rb'))
        except:
            self.members = {}
        self.chat_grps = {}  # {'name': group_name, 'members': group_members}
        try:
            load = pkl.load(open('group_info.dat', 'rb'))
            self.chat_grps, self.grp_ever = load[0], load[1]
        except Exception as e:
            print(e)
            self.chat_grps = {}
            self.grp_ever = 0
        self.name2group={}
        for each_number in self.chat_grps.keys():
            self.name2group[self.chat_grps[each_number]['name']]=each_number

    def is_member(self, name):
        return name in self.members.keys()

    def validate(self, name, password):

        if not name in self.members:
            print('User dose not exist.')
            return False
        else:
            if self.members[name].password != password:
                print('Incorrect password.')
                print('Input:', password)
                print('Correct:', self.members[name].password)
                return False
            else:
                return True

    def join(self, name, password, email):  # register new user
        self.members[name] = User(name, password, email)
        file = open('user_info.dat', 'wb')
        pkl.dump(self.members, file)
        file.close()

        return

    def save_grps(self):
        file = open('group_info.dat', 'wb')
        pkl.dump([self.chat_grps, self.grp_ever], file)
        file.close()
        file = open('user_info.dat', 'wb')
        pkl.dump(self.members, file)
        file.close()

    def new_group(self, grp_name, members):
        self.chat_grps[self.grp_ever] = {'name': grp_name, 'members': members}
        for each_member in members:
            self.members[each_member].groups.append(self.grp_ever)
        self.name2group[grp_name] = self.grp_ever
        self.grp_ever += 1
        self.save_grps()
        return

    def edit_group(self, grp_name, members, old_name):
        number=self.name2group[old_name]
        self.delete_group(number)
        self.chat_grps[number] = {'name': grp_name, 'members': members}
        for each_member in members:
            self.members[each_member].groups.append(number)
        self.name2group[grp_name] = number
        self.save_grps()
        return

    def add_people(self, people, group_number):
        self.chat_grps[group_number]['members'].append(people)
        self.members[people].groups.append(group_number)
        self.save_grps()
        return

    def delete_people(self, people, group_number):
        try:
            self.chat_grps[group_number]['members'].remove(people)
        except:
            print('failed to remove', people, 'from group', group_number)
        try:
            self.members[people].groups.remove(group_number)
        except:
            print('failed to remove', group_number, 'from people', people)
        self.save_grps()
        return

    def delete_group(self, group_number):
        self.name2group.pop(self.chat_grps[group_number]['name'])
        for each_member in self.chat_grps[group_number]['members']:
            self.members[each_member].groups.remove(group_number)
        self.chat_grps.pop(group_number)
        print(self.chat_grps)

        self.save_grps()
        return
