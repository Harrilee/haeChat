from tkinter import *
import threading


def main(self):
    window = Toplevel()  ############################## Remember to change this back
    window.iconbitmap('logo.ico')
    window.title('Game Menu')

    def snake():
        import snakeS

    def virus():
        import shooter
        shooter.main()

    def blackjack():
        import window_blackjack
        window_blackjack.main(self)


    def play():
        if choice_val.get() == 0:
            label2_string.set('Please choose a game.')
        else:
            window.destroy()
            if choice_val.get() == 1:
                input_thread = threading.Thread(target=snake)
                input_thread.daemon = True
                input_thread.start()
            elif choice_val.get() == 2:
                input_thread = threading.Thread(target=virus)
                input_thread.daemon = True
                input_thread.start()
            elif choice_val.get() == 3:
                input_thread = threading.Thread(target=blackjack)
                input_thread.daemon = True
                input_thread.start()

    label00 = Label(window)
    label00.pack(padx=10)

    label0 = Label(window, text="Choose a Game", padx=10, pady=10, font=('verdana', 16))
    label0.pack(padx=10)

    frame0 = Frame(window)
    frame0.pack(padx=60, pady=10)

    choice_val = IntVar()
    choice_val.set(0)

    labelframe1 = LabelFrame(frame0, text='Single Player')
    labelframe1.pack(fill=X, padx=10, pady=10, anchor=W)

    radiobutton1 = Radiobutton(labelframe1, text='Gluttonous Snake', value=1, variable=choice_val)
    radiobutton1.pack(anchor=W)
    radiobutton2 = Radiobutton(labelframe1, text='Virus Shooter', value=2, variable=choice_val)
    radiobutton2.pack(anchor=W)

    labelframe2 = LabelFrame(frame0, text='Double Player')
    labelframe2.pack(fill=X, padx=10, pady=10, anchor=W)

    radiobutton2 = Radiobutton(labelframe2, text='BlackJack', value=3, variable=choice_val)
    radiobutton2.pack(anchor=W)

    button1 = Button(frame0, text='Play', command=play, width=15)
    button1.pack(pady=10)

    label2_string = StringVar()
    label2 = Label(window, textvariable=label2_string)
    label2.pack(padx=10, pady=10)

    mainloop()


if __name__ == '__main__':
    main(0)
