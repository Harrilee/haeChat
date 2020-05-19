# -*- coding: UTF-8 -*-


from tkinter import *
from tkinter import Toplevel
import window_chat


def main(text2):

    emoji_dict = {
        "GRINNING_FACE": '\ud83d\ude00',
        "GRINNING_FACE_WITH_SMILING_EYES": '\ud83d\ude04',
        "BEAMING_FACE_WITH_SMILING_EYES": '\ud83d\ude01',
        "GRINNING_SQUINTING_FACE": '\ud83d\ude06',
        "GRINNING_FACE_WITH_SWEAT": '\ud83d\ude05',
        "LAUGHING_ON_THE_FLOOR": '\ud83e\udd23',
        "TEARS_OF_JOY": '\ud83d\ude02',
        "SMILING_FACE_SLIGHTLY": '\ud83d\ude42',
        "UPSIDE-DOWN_FACE": '\ud83d\ude43',
        "WINKING_FACE": '\ud83d\ude09',
        "SMILING_FACE_WITH_HEART-SHAPED_EYES": '\uD83D\uDE0D',
        "FACE_THROWING_A_KISS": '\uD83D\uDE18',
        "FACE_SAVOURING_DELICIOUS_FOOD": '\uD83D\uDE0B',
        "FACE_WITH_STUCK-OUT_TONGUE_AND_TIGHTLY-CLOSED_EYES": '\uD83D\uDE1D',
        "THINKING_FACE": '\uD83E\uDD14',
        "DIZZY_FACE": '\uD83D\uDE35',
        "SMILING_FACE_WITH_SUNGLASSES": '\uD83D\uDE0E',
        "CRYING_FACE": '\uD83D\uDE22',
        "ANGRY_FACE": '\uD83D\uDE20',
        "OK_HAND_SIGN": '\uD83D\uDC4C',
        "THUMBS_UP_SIGN": '\uD83D\uDC4D',
        "THUMBS_DOWN_SIGN": '\uD83D\uDC4E',
        "SMILING_FACE_WITH_HORNS": '\uD83D\uDE08',
        "HEART": "\u2764"
    }


        
#searching for emoji, works when testing
    
    def search(text):
        for widget in emoji_frame.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()

        emoji_name_list = list(emoji_dict.keys())
        emoji_name_list.sort()
        if text == "" or text == " ":
            creates_emojis()
        else:
            x = 10
            y = 0
            for emoji_name in emoji_name_list:
                if emoji_name.startswith(text):
                    emoji_code = emoji_dict[emoji_name]
                    emoji_button = Button(emoji_frame, text=emoji_code, borderwidth=0, font=("Courier New", 14))
                    emoji_button.place(x=x, y=y)

                    if x <= 150:
                        x += 30
                    else:
                        x = 10
                        y += 30
            emoji_frame.configure(width=200, height=y+60)
        
    
    def creates_emojis():
        x = 10
        y = 0
        for emoji_name in emoji_dict:
            emoji_code = emoji_dict[emoji_name]
            emoji_button = Button(emoji_frame, text=emoji_code, borderwidth=0, font=("Courier New", 14))
            emoji_button.place(x=x, y=y)
            emoji_button.bind("<Button-1>", lambda event, emoji=emoji_code: text2.insert(END, emoji)) 


            if x <= 150:
                x += 30
            else:
                x = 10
                y += 30
                
        emoji_frame.configure(width=200, height=y+30)
    
    window = Toplevel()
    window.iconbitmap('logo.ico')
    window.title('Emojis')

    window.tk.call('encoding', 'system', 'utf-8')

    window.configure(width=220, height=220)
        
    emoji_frame = LabelFrame(window, text="emojis")
    emoji_frame.place(x=10, y=60)

    search_var = StringVar()
    search_entry = Entry(window, textvariable=search_var)
    search_entry.place(x=10, y=10)
            
    search_button = Button(window, text="search", command=lambda: search(search_var.get().upper()))
    search_button.place(x=10, y=30)
    
    display_all_button = Button(window, text="display all", command=lambda: creates_emojis())
    display_all_button.place(x=60, y=30)

    creates_emojis()
    
    window.mainloop()

if __name__ == '__main__':
    main(0)
