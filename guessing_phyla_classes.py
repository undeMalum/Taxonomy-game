from choosing_random_photo_final_draft import random_photos
from organizing_program_final_draft import round_up, Answer
from photos_db import select_many, select_unusual, display_phyla
from time import time
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from PIL import ImageTk, Image, ImageFile

# keeping track for truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# creating main window and setting default values
root = Tk()
root.title("Taxonomy game")
root.geometry("350x450")


# intermediary between Enter key and function "confirm_action" (getting rid of an event argument)
def call_confirm_action(event=None):
    confirm_action()


# function for a button and Enter key, depending on user's preferences
def confirm_action():
    global n, best_time, timer, end, answer, mistakes
    # saving answer from a widget "answer" as it later gets destroyed
    from_answer = answer.get().lower()
    # if the time for an answer didn't expire 'coz user provided the answer, we need to stop counting this time
    root.after_cancel(timer)
    if n == len(files) - 1:
        # it is last screen; with correct answer for last question, time spent on answering and button to come back
        end = time()
        overall_time = round_up(end - start, 2)
        mistake = answer.answer_check(from_answer, directories[n], f"Time: {overall_time}")
        if mistake:
            mistakes += 1
        confirm.config(text="Done")
        answer.config(state=DISABLED)
        n += 1
    elif n == len(files):
        # it returns to the main screen; providing the number of mistakes and new best time if needed
        overall_time = round_up(end - start, 2)
        if best_time < 0:
            time_mistakes.config(text=f"Best time: {overall_time}. Mistakes: {mistakes}")
        elif overall_time < best_time:
            best_time = overall_time
            time_mistakes.config(text=f"Best time: {best_time}. Mistakes: {mistakes}")
        game_frame.pack_forget()
        main_frame.pack()
    else:
        # it is a window for providing the question, place for answer, and answer for the previous question
        answer.destroy()
        answer = Answer(game_frame, width=35)
        answer.bind("<FocusIn>", answer.insert_text)
        answer.grid(column=0, row=1, sticky=E)

        mistake = answer.answer_check(from_answer, directories[n], "(Click)")
        if mistake:
            mistakes += 1

        # new picture
        n += 1
        img_temp = Image.open(files[n])
        img_temp.thumbnail(seize)
        img = ImageTk.PhotoImage(img_temp)
        img_label.config(image=img)
        img_label.image = img

        # start timer and set defaults for answer
        timer = root.after(time_answer, confirm_action)
        answer.bind("<Return>", call_confirm_action)


# there are two frames; main window and game frame
# here is the game frame
game_frame = Frame(root, height=300, width=320)

# creating widget in the game frame
answer = Answer(game_frame, width=35)
answer.insert(0, "What phylum/class is it?")
answer.bind("<FocusIn>", answer.insert_text)
confirm = Button(game_frame, text="Confirm")
img_label = Label(game_frame)
# placing widgets in the game frame
img_label.grid(column=0, row=0, columnspan=2)
answer.grid(column=0, row=1, sticky=E)
confirm.grid(column=1, row=1, sticky=W)


# function for initializing each game
def initialize(game_option_init):
    global current_choices
    # checking if user chose at least two phyla or classes
    if len(choices.curselection()) <= 1 and len(current_choices) <= 1 and game_option_init != 1:
        messagebox.showinfo("Error", "Choose at least two phyla!")
    elif game_option_init == 1 and len(choices.curselection()) == 0 and len(current_choices) == 0:
        messagebox.showinfo("Error", "Choose at least one phylum!")
    else:
        global start, timer, n, directories, files, time_answer, mistakes, answer
        # if it is a second game or other, this returns to the initial values
        if str(answer["state"]) == "disabled":
            confirm.config(text="Confirm")
            answer.destroy()
            answer = Answer(game_frame, width=30)
            answer.grid(column=0, row=1, sticky=E)
            answer.set_default()

        # setting time for answers according to the user's choice
        choice_dif = difficulty.get()
        if choice_dif == "easy":
            time_answer = 20000
        elif choice_dif == "moderate":
            time_answer = 15000
        else:
            time_answer = 10000

        # changing game options to folders
        if game_option_init == 1:
            species_characteristics_init = "classes"
        elif game_option_init == 2:
            species_characteristics_init = "phyla"
        else:
            species_characteristics_init = "characteristics"

        # determining whether user firstly clicked level of difficulty or chose phyla/classes
        if len(choices.curselection()) > 0:
            selected_now = [choices.get(idx) for idx in choices.curselection()]
        else:
            selected_now = [choices.get(idx) for idx in current_choices]

        # fetching photos with answers (corresponding classes or phyla)
        number_of_photos = 10
        directories, files = random_photos(number_of_photos, selected_now, species_characteristics_init)

        # setting values to initialize the game
        mistakes = 0
        n = 0
        img_temp = Image.open(files[n])
        img_temp.thumbnail(seize)
        img = ImageTk.PhotoImage(img_temp)
        img_label.config(image=img)
        img_label.image = img
        confirm.config(command=confirm_action)
        start = time()
        main_frame.pack_forget()
        game_frame.pack()
        timer = root.after(time_answer, confirm_action)
        answer.bind("<Return>", call_confirm_action)


# function to avoid the problem with the disappearing focus on Combobox
def remember_choices(selection, event=None):
    global current_choices
    if len(current_choices) <= 1:
        current_choices = selection


# creating flexible listbox
def determined_list(cla_phyla_char):
    choices.delete(0, END)
    global options, current_choices
    current_choices = ()
    if cla_phyla_char == 1:
        game_mode = 0
        choices.config(selectmode="single")
    elif cla_phyla_char == 2:
        game_mode = 1
        choices.config(selectmode="multiple")
    else:
        game_mode = 2
        choices.config(selectmode="multiple")
    for each_item in options[game_mode]:
        choices.insert(END, each_item)


# Initial values
n = -1  # determines the number of answer in the sequence
start = 0  # starts counting for a game
end = 0  # ends counting for a game
seize = 400, 200  # sets maximum value of pictures
best_time = -1
directories, files = [], []
timer = 0  # keeps the id of a widget to be canceled
mistakes = 0
time_answer = 0  # in milliseconds
current_choices = ()

# here is main frame
main_frame = Frame(root, height=300, width=350)

# creating widgets in main frame
main_img = ImageTk.PhotoImage(Image.open("main_photo.png"))
main_img_label = Label(main_frame, image=main_img)
classes_phyla_char = IntVar(main_frame, 1)
classes = Radiobutton(main_frame, variable=classes_phyla_char, value=1, text="Classes",
                      command=lambda: determined_list(classes_phyla_char.get()))
phyla = Radiobutton(main_frame, variable=classes_phyla_char, value=2, text="Phyla",
                    command=lambda: determined_list(classes_phyla_char.get()))
characteristics = Radiobutton(main_frame, variable=classes_phyla_char, value=3, text="Characteristics",
                              command=lambda: determined_list(classes_phyla_char.get()))
start_game = Button(main_frame, text="Start", command=lambda: initialize(classes_phyla_char.get()))
info_difficulty = Label(main_frame, text="Choose the the level of difficulty:")
difficulty = Combobox(main_frame, width=20, state="readonly")
yscrollbar = Scrollbar(main_frame, width=20)
choices = Listbox(main_frame, selectmode="single",
                  yscrollcommand=yscrollbar.set, height=5, width=20)
yscrollbar.config(command=choices.yview)
time_mistakes = Label(main_frame, text="Best time: -")
# additional parameters for difficulty
difficulty.bind("<Button-1>", lambda event: remember_choices(selection=choices.curselection()))
difficulty["values"] = ("easy", "moderate", "hard")
difficulty.current(0)


# managing listbox
# options variable will store available phyla for each mode of the game ([0]: classes, [1]: phyla,
# [2]: characteristics)
options = [[], [], []]

# filling the first inner array (classes)
prompt = f"""select phylum_id from classes"""
range_temp = select_unusual(prompt, None, None)
options[0] = display_phyla(range_temp)

# filling the second inner array (phyla)
range_temp = select_many("phyla_and_characteristics", "phylum_id", "phyla_characteristics_id", 2)
options[1] = display_phyla(range_temp)

# filling the third inner array (characteristics)
range_temp = select_many("phyla_and_characteristics", "phylum_id", "phyla_characteristics_id", 1)
options[2] = display_phyla(range_temp)

# filling, initially, the listbox
for each_item in options[0]:
    choices.insert(END, each_item)

# putting menu on screen
main_frame.pack()
# organizing stuff inside menu
main_img_label.grid(column=0, row=0, columnspan=3)
classes.grid(column=0, row=1)
phyla.grid(column=1, row=1)
characteristics.grid(column=2, row=1)
info_difficulty.grid(column=0, row=3, columnspan=2)
difficulty.grid(column=2, row=3)
time_mistakes.grid(column=0, row=4, columnspan=2)
start_game.grid(column=2, row=4)
# connecting the listbox and scrollbar
choices.grid(column=0, row=2, columnspan=2, sticky=E)
yscrollbar.grid(column=2, row=2, sticky=W)

root.mainloop()
