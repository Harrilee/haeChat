from tkinter import *
import json
import chat_utils


def main(self):
    window = Toplevel()
    window.iconbitmap('logo.ico')
    window.title('Create a Group')

    frame1 = Frame(window)
    frame1.pack(anchor=W, padx=20, pady=20)

    label1 = Label(frame1, text='Group name:')
    label1.pack(side=LEFT, padx=5, pady=5)

    entry1 = Entry(frame1)
    entry1.pack(side=RIGHT, pady=5, padx=5)

    label2 = Label(window, text='Select members:')
    label2.pack(anchor=W, padx=25, pady=5)

    labelframe1 = LabelFrame(window)
    labelframe1.pack(padx=30, pady=5, fill=X)

    choices = []
    for each in self.user:
        if each != self.name:
            choices.append(each)
    values = []
    for each in choices:
        values.append(IntVar())
        button = Checkbutton(labelframe1, text=each, variable=values[-1])
        button.pack(anchor=W)

    def button1_click():
        if (entry1.get() in self.user) or (entry1.get() in self.group) or (entry1.get() == '*Add a group...'):
            label3_string.set('This name has already been taken.')
            return
        if entry1.get() == '':
            label3_string.set('Please enter the group name.')
            return
        chosen = []
        for i in range(len(values)):
            if values[i].get() == 1:
                chosen.append(choices[i])
        if chosen == []:
            label3_string.set('Please at least make a choice.')
            return
        chosen.append(self.name)
        msg = json.dumps({"action": "create_group", "from": self.name, 'member': chosen, 'name': entry1.get()})
        chat_utils.mysend(self.socket, msg)
        window.destroy()

    button1 = Button(window, text='Create_group', width=10, command=button1_click)
    button1.pack(pady=10)

    label3_string = StringVar()
    label3 = Label(window, textvariable=label3_string)
    label3.pack()

    label4 = Label(window)  # only to take up position
    label4.pack()

    window.mainloop()
    msg = json.dumps({"action": "refresh_list", "from": self.name})
    chat_utils.mysend(self.socket, msg)



if __name__ == '__main__':
    main(0)
