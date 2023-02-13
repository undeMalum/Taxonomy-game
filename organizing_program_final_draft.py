from math import ceil
from tkinter import *


# used to round time, avoiding long numbers
def round_up(value, decimals=0):
    multiplier = 10 ** decimals
    return ceil(value * multiplier) / multiplier


# put all function connected with answer in one place
class Answer(Entry):
    def insert_text(self, event):
        if event.widget == self:
            self.delete(0, END)
            self.config(bg="white")

    def answer_check(self, ans, dir_f, info):
        mistake_f = False
        if ans == f"{dir_f}":
            self.config(bg="green")
            self.delete(0, END)
            self.insert(0, f"Correct answer! {info}")
        else:
            self.config(bg="red")
            self.delete(0, END)
            self.insert(0, f"Wrong. Correct: {dir_f}. {info}")
            mistake_f = True
        return mistake_f

    def set_default(self):
        self.config(state=NORMAL, bg="white")
        self.delete(0, END)
        self.insert(0, "What phylum/class is it?")
        self.bind("<FocusIn>", self.insert_text)
