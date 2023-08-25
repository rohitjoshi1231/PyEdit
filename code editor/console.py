import subprocess
import tkinter as tk
from tkinter import filedialog
import threading


class Console:
    dynamic_title = "Untitled*"
    bold = False
    italic = False
    isdarkmode = False

    def __init__(self, main):
        self.path = ""
        self.text = None
        self.shell = None
        self.root = main
        self.root.geometry("500x600")
        self.root.title(self.dynamic_title)
        self.create_menu(bg="white", fg="black")
        self.text = tk.Text(self.root, height=20, width=50, font="Serif 12")
        self.text.pack()
        self.output_label = tk.Label(
            text="Output", font="Serif 10 roman", relief="raised")
        self.output_label.pack(pady=10, anchor="center")
        self.shell = tk.Text(self.root, height=8, width=50,
                             font="Serif 12", pady=10)
        self.shell.config(state=tk.NORMAL)
        self.shell.bind("<KeyPress>", lambda e: "break")
        self.shell.pack(side='bottom')

        # creating menubar
    def create_menu(self, bg, fg):
        menubar = tk.Menu(root, bg=bg, fg=fg)
        # Adding File Menu and commands
        file = tk.Menu(menubar, tearoff=0, bg="#303030", fg="white", activebackground="#004f98",
                       activeforeground="white")
        menubar.add_cascade(label='File', font="Serif 10 roman", menu=file)
        file.add_command(label='New File',
                         font="Serif 10 roman", command=self.new_file)
        file.add_command(label='Open...', font="Serif 10 roman",
                         command=self.open_file)
        file.add_command(label='Save as', font="Serif 10 roman",
                         command=self.save_note)
        file.add_separator()
        file.add_command(label='Exit', font="Serif 10 roman",
                         command=root.destroy)

        # Adding Edit Menu and commands
        edit = tk.Menu(menubar, tearoff=0, bg="#303030", fg="white", activebackground="#004f98",
                       activeforeground="white")
        menubar.add_cascade(label='Edit', menu=edit, font="Serif 10 roman", )
        edit.add_command(label='Cut', font="Serif 10 roman", command=self.cut)
        edit.add_command(label='Copy', font="Serif 10 roman",
                         command=self.copy)
        edit.add_command(label='Paste', font="Serif 10 roman",
                         command=self.paste)
        edit.add_command(label='Select All',
                         font="Serif 10 roman", command=self.select_all)

        # Adding Style Menu and commands
        style = tk.Menu(menubar, tearoff=0, bg="#303030", fg="white", activebackground="#004f98",
                        activeforeground="white")
        menubar.add_cascade(label='Style', font="Serif 10 roman", menu=style)
        style.add_checkbutton(
            label='Bold', font="Serif 10 roman", command=self.toggle_bold)
        style.add_checkbutton(
            label='Italic', font="Serif 10 roman", command=self.toggle_italic)
        style.add_separator()
        style.add_command(label='Dark Mode',
                          font="Serif 10 roman", command=self.toggle_dark_mode)
        style.add_command(label='Text Color',
                          font="Serif 10 roman", command=self.select_color)

        run = tk.Menu(menubar, tearoff=0, bg="#303030", fg="white", activebackground="#004f98",
                      activeforeground="white")
        menubar.add_cascade(label='Run', menu=run, font="Serif 10 roman")
        run.add_command(label="Run File", command=self.run_file,
                        font="Serif 10 roman", hidemargin=True)
        root.config(menu=menubar)

    def apply_font_style(self):
        font_style = "Serif"
        font_size = 12

        if Console.bold:
            self.text.tag_configure("bold", font=(
                font_style, font_size, "bold"))
        else:
            self.text.tag_configure("bold", font=(font_style, font_size))

        if Console.italic:
            self.text.tag_configure("italic", font=(
                font_style, font_size, "italic"))
        else:
            self.text.tag_configure("italic", font=(font_style, font_size))

        # Apply initial font style
        self.text.tag_remove("bold", "1.0", tk.END)
        self.text.tag_remove("italic", "1.0", tk.END)
        self.apply_selection_font_style()

    def apply_selection_font_style(self):
        if Console.bold:
            self.text.tag_add("bold", "sel.first", "sel.last")

        if Console.italic:
            self.text.tag_add("italic", "sel.first", "sel.last")

    def select_color(self):
        """
        Selects a color from a list of colors.
        """
        win = tk.Tk()
        win.title("Select Color")
        colours = ["black", "white", "red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan",
                   "magenta", "indigo", "teal", "olive", "maroon", "navy", "aqua", "turquoise", "lime", "fuchsia",
                   "gold", "silver", "gray", "coral", "maize", "sienna", "tan", "wheat", "olivedrab"]

        self.listbox = tk.Listbox(win, height=10,
                                  width=15,
                                  bg="grey",
                                  activestyle='dotbox',
                                  font="Helvetica",
                                  fg="yellow")
        for idx, color in enumerate(colours, start=1):
            self.listbox.insert(int(idx), color)

        def on_select(event):
            u = self.listbox.get(event.widget.curselection()[0])
            self.text.config(fg=u)
            self.shell.config(fg=u)
            win.destroy()

        self.listbox.bind("<ButtonRelease-1>", on_select)

        self.listbox.pack()
        win.mainloop()

    def save_note(self):
        note_text = self.text.get("1.0", "end-1c")
        path = filedialog.asksaveasfile(title="Save as", filetypes=[
                                        ("python", ".py"), ("All Files", ".*")])
        if path:
            path.write(note_text)
            n = path.name.split("/")
            Console.dynamic_title = n[-1]
            self.root.title(Console.dynamic_title)
            self.path = path.name

    def open_file(self):
        file = filedialog.askopenfilename(title="Select a directory",
                                          filetypes=[("python", ".py"), ("All Files", ".*")])
        if file:
            with open(file, mode="r+") as new_file:
                content = new_file.read()
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, content)
                self.shell.delete("1.0", tk.END)
                self.shell.insert(tk.END, file)
                n = file.split("/")
                Console.dynamic_title = n[-1]
                self.root.title(Console.dynamic_title)
                self.path = file

    def new_file(self):
        note_text = self.text.get("1.0", "end-1c")
        path = filedialog.asksaveasfile(title="Create New File", filetypes=[
                                        ("python", ".py"), ("All Files", ".*")])
        if path:
            path.write(note_text)
            n = path.name.split("/")
            Console.dynamic_title = n[-1]
            self.root.title(Console.dynamic_title)
            self.path = path.name

    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def select_all(self):
        self.text.tag_add("sel", "1.0", tk.END)

    def toggle_bold(self):
        Console.bold = not Console.bold
        self.apply_font_style()

    def toggle_italic(self):
        Console.italic = not Console.italic
        self.apply_font_style()

    def run_file(self):
        if self.path:
            output_thread = threading.Thread(
                target=self.run_and_capture_output)
            output_thread.start()

    def run_and_capture_output(self):
        result = subprocess.Popen(
            ["python", self.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = result.communicate()
        out_str = output.decode('utf-8')
        err_str = errors.decode('utf-8')
        self.update_shell(out_str + err_str)

    def update_shell(self, output):
        self.shell.config(state=tk.NORMAL)
        self.shell.delete("1.0", tk.END)
        self.shell.insert(tk.END, output)
        self.shell.config(state=tk.DISABLED)

    def toggle_dark_mode(self):
        Console.isdarkmode = not Console.isdarkmode
        bg_color = "#303030" if Console.isdarkmode else "white"
        fg_color = "white" if Console.isdarkmode else "black"
        self.text.config(bg=bg_color, fg=fg_color)
        self.shell.config(bg=bg_color, fg=fg_color)
        self.root.config(bg=bg_color)
        self.create_menu(bg=bg_color, fg=fg_color)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    app = Console(root)
    root.mainloop()
