import json
import tkinter
from tkinter import ttk
from dataclasses import dataclass
from strongbox.locker.io import IO
from strongbox.app.utils import _sha256, get_accounts
from cryptography.fernet import InvalidToken
from strongbox.gui.utils import UserCache, cache_user, get_user_cache


@dataclass
class UserData(IO):
    profile: str
    password: str


class EntryWithPlaceholder(ttk.Entry):
    def __init__(self, master=None, placeholder: str = "placeholder", color: str = "grey"):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["foreground"]

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["foreground"] = self.placeholder_color

    def foc_in(self, *args):
        if str(self["foreground"]) == self.placeholder_color:
            self.delete(0, tkinter.END)
            self['foreground'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class LoginPage:
    def __init__(self, root: tkinter.Tk):
        def on_done(event: tkinter.Event):
            try:
                profile = profile_entry.get()
                password = _sha256(password_entry.get())
                get_accounts(profile, password)
                cache_user(UserCache(profile))
                mainframe.destroy()
                MainPage(root, UserData(profile, password))
            except InvalidToken:
                error = ttk.Label(mainframe, text="Wrong password!")
                error.grid(row=3, column=2)
                error.config(foreground="red")
                password_entry.delete(0, tkinter.END)

        root.title("StrongBox")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        profile_entry = EntryWithPlaceholder(mainframe, "profile")
        profile_entry.grid(row=2, column=2)

        password_entry = EntryWithPlaceholder(mainframe, "password")
        password_entry.grid(row=3, column=2)
        password_entry.bind("<KeyRelease-Return>", on_done)


class LoginPasswordOnlyPage:
    def __init__(self, root: tkinter.Tk, profile: str):
        def on_done(event: tkinter.Event):
            try:
                password = _sha256(entry.get())
                get_accounts(profile, password)
                mainframe.destroy()
                MainPage(root, UserData(profile, password))
            except InvalidToken:
                error = ttk.Label(mainframe, text="Wrong password!")
                error.grid(row=3, column=2)
                error.config(foreground="red")
                entry.delete(0, tkinter.END)

        root.title("StrongBox")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        entry = EntryWithPlaceholder(mainframe, "password")
        entry.grid(row=2, column=2)
        entry.focus()
        entry.bind("<KeyRelease-Return>", on_done)


class MainPage:
    def __init__(self, root: tkinter.Tk, user: UserData):
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        accounts = get_accounts(user.profile, user.password)
        accounts = [account.to_dict() for account in accounts]
        label = ttk.Label(mainframe, text=json.dumps(accounts))
        label.grid(row=2, column=2)

        root.update()


class GUI:
    def __init__(self, root: tkinter.Tk):
        cache = get_user_cache()
        if not cache:
            LoginPage(root)
        else:
            LoginPasswordOnlyPage(root, cache.profile)


root = tkinter.Tk()
GUI(root)
root.mainloop()
