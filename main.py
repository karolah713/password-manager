from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letter_result = [random.choice(letters) for _ in range(nr_letters)]
    symbol_result = [random.choice(symbols) for _ in range(nr_symbols)]
    number_result = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = letter_result+symbol_result+number_result
    random.shuffle(password_list)

    password_generated = "".join(password_list)

    password_entry.insert(END, string=f"{password_generated}")
    pyperclip.copy(f"{password_generated}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        empty_field = messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # reading old data
                date = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, fp=data_file, indent=4)
        else:
            # updating old data
            date.update(new_data)
            with open("data.json", mode="w") as data_file:
                # saving updated data
                json.dump(date, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    user_entry = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            # reading data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if user_entry in data:
            email = data[user_entry]["email"]
            password = data[user_entry]["password"]
            data_pop_up = messagebox.showinfo(title=f"{user_entry}", message=f"Email: {email}\nPassword: {password}")
        else:
            empty_field = messagebox.showinfo(title="Error", message=f"No Details for the {user_entry} exist.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Lable
website_title = Label(text="Website:")
website_title.grid(column=0, row=1)

username_title = Label(text="Email/Username:")
username_title.grid(column=0, row=2)

password_title = Label(text="Password:")
password_title.grid(column=0, row=3)

# Entry
website_entry = Entry(width=33)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = Entry(width=52)
username_entry.insert(END, string="karola713@o2.pl")
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

#Buttons

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=find_password, width=14)
search_button.grid(column=2, row=1)



window.mainloop()