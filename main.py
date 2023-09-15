
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
import tempfile

class CppCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C++ Compiler")

        self.text_input = tk.Text(root, height=10, width=40)
        self.text_input.pack()
        self.text_input.bind("<KeyRelease>", self.compile_cpp)

        self.output_text = tk.Text(root, height=10, width=40, state=tk.DISABLED)
        self.output_text.pack()

        self.compiler_label = tk.Label(root, text="Select Compiler:")
        self.compiler_label.pack()

        self.compiler_var = tk.StringVar()
        self.compiler_var.set("g++")  # Default to g++
        self.compiler_option = tk.OptionMenu(root, self.compiler_var, "g++", "clang++")
        self.compiler_option.pack()

        self.optimization_label = tk.Label(root, text="Select Optimization Level:")
        self.optimization_label.pack()

        self.optimization_var = tk.StringVar()
        self.optimization_var.set("-O2")  # Default to -O2
        self.optimization_option = tk.OptionMenu(
            root, self.optimization_var, "-O0", "-O1", "-O2", "-O3"
        )
        self.optimization_option.pack()

    def compile_cpp(self, event=None):
        code = self.text_input.get("1.0", tk.END)
        with open("temp.cpp", "w") as f:
            f.write(code)

        compiler = self.compiler_var.get()
        optimization = self.optimization_var.get()

        # Create a temporary file to store assembly output
        with tempfile.NamedTemporaryFile(mode="w", delete=False, text=True) as asm_file:
            try:
                cmd = [compiler, "-S", "temp.cpp", "-o", "temp", optimization]
                subprocess.run(cmd, stdout=asm_file, stderr=subprocess.STDOUT, text=True, check=True)
            except subprocess.CalledProcessError as e:
                asm_file.write(e.output)

        # Read and display the content of the assembly file
        with open(asm_file.name, "r") as asm_file:
            assembly_code = asm_file.read()

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, assembly_code)
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CppCompilerApp(root)
    root.mainloop()

