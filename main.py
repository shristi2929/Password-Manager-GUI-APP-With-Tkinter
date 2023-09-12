import tkinter
import secrets
import string
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import csv
import os.path

import pandas as pd


def checkIfEnteysIsNotEmpty(website, username, password):
    if website == "":
        tkinter.messagebox.showerror(title="Website is empty", message="Website is empty \n please try again.")
        return False
    if username == "":
        tkinter.messagebox.showerror(title="Username is empty", message="Username/Email is empty \n please try again.")
        return False
    if password == "":
        tkinter.messagebox.showerror(title="Password is empty", message="Password is empty \n please try again.")
        return False
    return True


def readAllTheWebsiteAndThePasswordFromFile():
    fileName = "Password_Manager_Data.csv"
    if os.path.isfile(fileName):
        df = pd.read_csv(fileName)
        return df["Website:"].values.tolist(), df["Password:"].values.tolist()
    return None, None


def changePasswordIfWebsiteExist():
    website = entryWebsite.get()
    username = entryUsername.get()
    password = entryPassword.get()

    if checkIfEnteysIsNotEmpty(website, username, password):
        websiteLst, passwordLst = readAllTheWebsiteAndThePasswordFromFile()
        if websiteLst is None:
            save(website, username, password)
        elif website in websiteLst:
            is_ok = tkinter.messagebox.askokcancel(title="Change password to save",
                                                   message=f"Do you want to change the {website} Password ?\n\n"
                                                           f"These are the details entered:\n\nWebsite: {website}\n"
                                                           f"User Name: {username}\n"
                                                           f"Password:{password} \n\nIs it ok to save?")
            if is_ok:
                # reading the csv file
                df = pd.read_csv("Password_Manager_Data.csv")
                # updating the column value/data
                df.loc[websiteLst.index(website), 'Password:'] = password
                df.loc[websiteLst.index(website), 'Username:'] = username
                # writing into the file
                df.to_csv("Password_Manager_Data.csv", index=False)


        else:
            save(website, username, password)


def showCsv():
    root = Tk()
    root.title("Passwords")
    width = 600
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Website", "Username", "Password"), height=400, selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Website', text="Website:", anchor=W)
    tree.heading('Username', text="Username:", anchor=W)
    tree.heading('Password', text="Password:", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.pack()
    if os.path.isfile("Password_Manager_Data.csv"):
        with open('Password_Manager_Data.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                firstname = row["Website:"]
                lastname = row["Username:"]
                address = row['Password:']
                tree.insert("", 0, values=(firstname, lastname, address))


def generatePassword():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(18))
    entryPassword.delete(0, 'end')
    entryPassword.insert(0, password)


def save(website, username, password):
    is_ok = tkinter.messagebox.askokcancel(title="New password to save",
                                           message=
                                           f"These are the details entered:\n\n"
                                           f"Website: {website}\n"
                                           f"User Name: {username}\n"
                                           f"Password:{password} \n\nIs it ok to save?")
    if is_ok:
        if not os.path.isfile("Password_Manager_Data.csv"):
            header = ['Website:', 'Username:', 'Password:']
            with open('Password_Manager_Data.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(header)
                data = [
                    [website, username, password],
                ]
                writer.writerows(data)
        else:
            with open('Password_Manager_Data.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                data = [
                    [website, username, password],
                ]
                writer.writerows(data)


window = Tk()
window.geometry('450x350')
window.title("Password Manager")

img = Image.open('logo.png')
resized = img.resize((130, 130), Image.Resampling.LANCZOS)
new_pic = ImageTk.PhotoImage(resized)

panel = Label(window, image=new_pic)
panel.pack()

labelWebsite = Label(window, text="Website:", width=20, font=("bold", 10))
labelWebsite.place(x=56, y=130)

entryWebsite = Entry(window)
entryWebsite.place(x=240, y=130, width=150)
entryWebsite.focus()

labelUsername = Label(window, text="Email/Username:", width=20, font=("bold", 10))
labelUsername.place(x=80, y=170)

entryUsername = Entry(window)
entryUsername.insert(0, "savizronen@gmail.com")
entryUsername.place(x=240, y=170, width=150)

labelPassword = Label(window, text="Password:", width=20, font=("bold", 10))
labelPassword.place(x=60, y=210)

entryPassword = Entry(window)
entryPassword.place(x=240, y=210, width=150)
Button(window, text='Generate Password', width=20, bg='black', fg='white', command=generatePassword).place(x=240, y=235)

Button(window, text='Open passwords page', width=20, bg='black', fg='white', command=showCsv).place(x=155, y=270)

Button(window, text='Add', width=20, bg='brown', fg='white', command=changePasswordIfWebsiteExist).place(x=155, y=300)
# it is use for display the registration form on the window
window.mainloop()

print("Password Manager form  seccussfully created...")
