
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
from tkinter import ttk
from subprocess import check_output, CalledProcessError



class CppAssemblyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("C++ to assembly Compiler")
        self.geometry("800x600")

        self.init_ui()

    def init_ui(self):
        input_frame = ttk.Frame(self)
        input_frame.pack(fill=tk.BOTH, expand=True)

        input_label=ttk.Label(input_frame, text="C++ Program:")
        input_label.pack(anchor=tk.W)

        self.input_text = tk.Text(input_frame, wrap=tk.NONE)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        output_frame=ttk.Frame(self)
        output_frame.pack(fill=tk.BOTH, expand=True)

        output_label=ttk.Label(output_frame, text="Assembly output")
        output_label.pack(anchor=tk.W)

        self.output_text=tk.Text(output_frame, wrap=tk.NONE, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        config_frame=ttk.Frame(self)
        config_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.compiler_var=tk.StringVar()
        self.compiler_var.set("g++")

        compiler_label=ttk.Label(config_frame,text="Compiler")
        compiler_label.pack(side=tk.LEFT,padx=(0,5))
        complier_dropdown=ttk.OptionMenu(config_frame, self.compiler_var,"g++",)
        complier_dropdown.pack(side=tk.LEFT)

        self.optimization_var=tk.StringVar()
        self.optimization_var.set("O1")

        optimization_label=ttk.Label(config_frame, text="Optimization:")
        optimization_label.pack(side=tk.LEFT, padx=(10,5))
        optimization_dropdown=ttk.OptionMenu(config_frame, self.optimization_var,)
        optimization_dropdown.pack(side=tk.LEFT)

        self.input_text.bind("<KeyRelease>",self.update_assembly)


    def on_compiler_change(self,_):
        self.update_assembly()

    def on_optimization_change(self,_):
        self.update_assembly()

    def update_assembly(self,_):
        try:
            cpp_code=self.input_text.get(1.0,tk.END)
            compiler=self.compiler_var.get()
            optimization_level=self.optimization_var.get()

            with open("temp_cpp_code.cpp","w") as f:
                f.write(cpp_code)

            assembly_output=check_output([compiler,"-S", "-o-", f.name, f"-{optimization_level}","-masm=intel"])

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0",tk.END)
            self.output_text.insert(tk.END,assembly_output)
            self.output_text.config(state=tk.DISABLED)


        except CalledProcessError as e:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0",tk.END)
            self.output_text.insert(tk.END,f"Error: {e}")
            self.output_text.config(state=tk.DISABLED)



if __name__ == "__main__":
    app = CppAssemblyGUI()
    app.mainloop()
