
# hello world
#from tkinter import *
#from tkinter import ttk
#root = Tk()
#frm = ttk.Frame(root, padding=10)
#frm.grid()
#ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#root.mainloop()


import tkinter as tk
import subprocess


class CppCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C++ Compiler")

        self.text_input = tk.Text(self.root, height=10, width=40)
        self.text_input.pack()
        self.text_input.bind("<KeyRelease>", self.compile_cpp)

        self.output_text = tk.Text(self.root, height=10, width=40, state=tk.DISABLED)
        self.output_text.pack()

    def compile_cpp(self, event=None):
        code = self.text_input.get("1.0", tk.END)
        with open("temp.cpp", "w") as f:
            f.write(code)

        try:
            result = subprocess.check_output(["g++", "temp.cpp", "-o", "temp"])
            output = result.decode("utf-8")
        except subprocess.CalledProcessError as e:
            output = e.output.decode("utf-8")

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = CppCompilerApp(root)
    root.mainloop()
