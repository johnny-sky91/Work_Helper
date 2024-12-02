import os, pyperclip, traceback
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
from helper_scripts.get_all_diffrences import All_diffrences


load_dotenv()

paths, passwords = {}, {}
for key, value in os.environ.items():
    if key.startswith("PATH_"):
        paths[key] = value
    elif key.startswith("PASSWORD_"):
        passwords[value.split(", ")[0]] = value.split(", ")[1]


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Work_Helper")
        self.call("source", "used_theme/azure.tcl")
        self.call("set_theme", "dark")

        self.entries = {}
        self.check_vars = {}

        self.labels_widgets()
        self.select_widgets()
        self.entry_widgets()
        self.reports_widgets()
        self.others_widgets()
        self.passwords_widgets()

    def labels_widgets(self):
        labels_list = ["Select", "Files", "Reports", "Others", "Passwords"]
        for index, label in enumerate(labels_list):
            label_widget = tk.Label(self, text=label, font=("bold", 14))
            label_widget.grid(row=0, column=index, padx=5, pady=5)

    def select_widgets(self):
        select_data = {
            "Stock_old": lambda path_name="stock_old": self.select_path(path_name),
            "Stoc_new": lambda path_name="stock_new": self.select_path(path_name),
            "PO_old": lambda path_name="po_old": self.select_path(path_name),
            "PO_new": lambda path_name="po_new": self.select_path(path_name),
        }
        for index, (key, value) in enumerate(select_data.items()):
            bt = tk.Button(self, text=key, command=value, width=20)
            bt.grid(row=index + 1, column=0, padx=5, pady=5)

    def entry_widgets(self):
        entries_list = ["stock_old", "stock_new", "po_old", "po_new"]
        for index, entry_name in enumerate(entries_list):
            entry = tk.Entry(self, name=entry_name, width=40)
            entry.grid(row=index + 1, column=1, padx=5, pady=5)
            self.entries[entry_name] = entry

    def reports_widgets(self):
        reports_data = {
            "All diffrences": self.run_with_error_handling(
                lambda: All_diffrences(
                    old_po=self.entries["po_old"].get(),
                    new_po=self.entries["po_new"].get(),
                    old_stock=self.entries["stock_old"].get(),
                    new_stock=self.entries["stock_new"].get(),
                    report_path=paths["PATH_MAIN_FOLDER"],
                )
            ),
        }
        for index, (key, value) in enumerate(reports_data.items()):
            bt = tk.Button(self, text=key, command=value, width=20)
            bt.grid(row=index + 1, column=2, padx=5, pady=5)

    def others_widgets(self):
        others_data = {}
        for index, (key, value) in enumerate(others_data.items()):
            bt = tk.Button(self, text=key, command=value, width=20)
            bt.grid(row=index + 1, column=3, padx=5, pady=5)

    def passwords_widgets(self):
        for index, (key, value) in enumerate(passwords.items()):
            pass_bt = tk.Button(
                self,
                text=key,
                width=20,
                command=lambda pssw=value: pyperclip.copy(pssw),
            )
            pass_bt.grid(row=index + 1, column=4, padx=5, pady=5)

    def select_path(self, path_name):
        path = filedialog.askopenfilename()
        entry = self.nametowidget(path_name)
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.xview_moveto(1)

    def run_with_error_handling(self, func):
        def wrapper():
            try:
                func()
            except Exception:
                error_trace = traceback.format_exc()
                messagebox.showerror("Error", error_trace)

        return wrapper


if __name__ == "__main__":
    app = Application()
    app.mainloop()
