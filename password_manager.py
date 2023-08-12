import os.path
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# --------------------------- global variable -----------------------------
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)

# file path global variable
user_home = os.path.expanduser("~")
file_path = os.path.join(user_home, "data.json")


# ##################### Functionality ####################################

# ----------------------- SAVE PASSWORD ------------------
def save():
    website_save_to_file = website_input.get().lower()
    email_save_to_file = email_input.get()
    password_save_to_file = password_input.get()
    new_data = {website_save_to_file: {"email": email_save_to_file, "password": password_save_to_file}}

    if website_save_to_file == '' or password_save_to_file == '':
        messagebox.showerror(title='Oops', message='You left some fields empty')
        return

    answer = messagebox.askyesno(message=f"Are all the details correct?\nEmail: {email_save_to_file}"
                                         f"\nWebsite: {website_save_to_file}", icon='question', title='save')
    if answer:
        data = {}
        try:
            with open(file_path, "r") as data_file:
                try:
                    # first load the old data
                    data = json.load(data_file)
                except json.JSONDecodeError as decode_error:
                    print(decode_error)
                    # messagebox.showerror(message=f"error loading the file: {decode_error}")
        except FileNotFoundError as e:
            print(f"file not found: {e}")
            # open file
            with open(file_path, "w") as data_file:
                try:
                    json.dump(new_data, data_file, indent=4)
                except json.JSONDecodeError as decode_error:
                    print(decode_error)
                    messagebox.showerror(message=f"error dumping into the file: {decode_error}")
        else:
            # check if the website is already in the data
            try:
                data[website_save_to_file]['password'] = password_save_to_file
                print(data)
            except KeyError as key_error:
                print(f"Key doesn't exist: {key_error}")
                # update the old data with the new data
                data.update(new_data)
            with open(file_path, "w") as data_file:
                try:
                    # write the new data into the file
                    json.dump(data, data_file, indent=4)
                    # remove all inputs
                    messagebox.showinfo(message="Your information was saved")
                except json.JSONDecodeError as decode_error:
                    print(decode_error)
                    messagebox.showerror(message=f"error dumping into the file: {decode_error}")
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- GENERATE PASSWORD --------------------------------
def generate_password():
    password_input.delete(0, END)
    password_list = [random.choice(letters) for i in range(nr_letters)]
    password_list += [random.choice(symbols) for i in range(nr_symbols)]
    password_list += [random.choice(numbers) for i in range(nr_numbers)]

    random.shuffle(password_list)
    final_password = "".join(password_list)
    password_input.insert(0, final_password)
    pyperclip.copy(final_password)


# ------------------------------- FIND PASSWORD ---------------------------------------
def search_website():
    curr_website = website_input.get().lower()
    if curr_website == '':
        messagebox.showinfo(title="Empty Search", message="Oops, you didn't add a website to search")
        return
    try:
        with open(file_path, "r") as data_file:
            password_data = json.load(data_file)
    except FileNotFoundError as e:
        print(f"No such file exists: {e}")
    else:
        try:
            curr_email = password_data[curr_website]['email']
            curr_password = password_data[curr_website]['password']
            messagebox.showinfo(title="Website Info", message=f"Website: {curr_website}\n"
                                                              f"Email: {curr_email}\n"
                                                              f"Password: {curr_password}")
        except KeyError as key_error:
            messagebox.showinfo(title="No such website",
                                message=f"you do not have information for this website: {curr_website}")


# ------------------------- UI --------------------------
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# canvas
canvas = Canvas(height=300, width=300)
logo_img = PhotoImage(file=r"C:\Users\arieh\PycharmProjects\day-27\lock-png.png")
canvas.create_image(150, 150, image=logo_img)
canvas.grid(row=0, column=1, columnspan=2)

# website label
website = Label(text="Website:")
website.grid(row=1, column=0, sticky=E)

# website input
website_input = Entry(width=20)
website_input.grid(row=1, column=1)
website_input.focus()

# email/username
email = Label(text="Email/Username:")
email.grid(row=2, column=0, sticky=E)
email_input = Entry(width=44)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "arieh.norton@gmail.com")

# Password frame
password = Label(text="Password:")
password.grid(row=3, column=0, sticky=E)

password_input = Entry(width=20)
password_input.grid(row=3, column=1)

password_button = Button(text="Generate Password", width=14, command=generate_password)
password_button.grid(row=3, column=2)

# add
add_button = Button(text="Add", width=37, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# search button
search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(row=1, column=2)

window.mainloop()
input("Press Enter to exit...")
