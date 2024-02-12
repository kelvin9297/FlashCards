from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
french_dict = {}

# import csv data
try:
    french_df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_dict = original_data.to_dict(orient="records")
else:
    french_dict = french_df.to_dict(orient="records")


# functions
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def remove_card():
    french_dict.remove(current_card)
    data = pandas.DataFrame(french_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# flip card mechanism
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


# UI Setup
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# canvas and texts
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, columnspan=2, row=0)

# buttons
cross_image = PhotoImage(file="images/wrong.png")
check_image = PhotoImage(file="images/right.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=next_card)
cross_button.grid(column=0, row=1)
check_button = Button(image=check_image, highlightthickness=0, command=remove_card)
check_button.grid(column=1, row=1)

next_card()
window.mainloop()
