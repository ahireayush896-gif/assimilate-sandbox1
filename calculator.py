import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Assimilate Calculator")
        self.root.geometry("360x480")
        self.root.config(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.equation = ""
        self.display_var = tk.StringVar()

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Display Frame
        display_frame = tk.Frame(self.root, bg="#1e1e1e", height=100)
        display_frame.pack(expand=False, fill="both", padx=15, pady=20)

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 28, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            anchor="e",
            padx=15,
            relief="flat"
        )
        self.display_label.pack(expand=True, fill="both")

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(expand=True, fill="both", padx=15, pady=(0, 20))

        buttons = [
            ('C', 0, 0, '#d9534f', '#ffffff'), ('(', 0, 1, '#333333', '#ffffff'), (')', 0, 2, '#333333', '#ffffff'), ('/', 0, 3, '#f0ad4e', '#ffffff'),
            ('7', 1, 0, '#2d2d2d', '#ffffff'), ('8', 1, 1, '#2d2d2d', '#ffffff'), ('9', 1, 2, '#2d2d2d', '#ffffff'), ('*', 1, 3, '#f0ad4e', '#ffffff'),
            ('4', 2, 0, '#2d2d2d', '#ffffff'), ('5', 2, 1, '#2d2d2d', '#ffffff'), ('6', 2, 2, '#2d2d2d', '#ffffff'), ('-', 2, 3, '#f0ad4e', '#ffffff'),
            ('1', 3, 0, '#2d2d2d', '#ffffff'), ('2', 3, 1, '#2d2d2d', '#ffffff'), ('3', 3, 2, '#2d2d2d', '#ffffff'), ('+', 3, 3, '#f0ad4e', '#ffffff'),
            ('0', 4, 0, '#2d2d2d', '#ffffff', 1), ('.', 4, 1, '#2d2d2d', '#ffffff', 1), ('=', 4, 2, '#5cb85c', '#ffffff', 2)
        ]

        for btn_info in buttons:
            text = btn_info[0]
            row = btn_info[1]
            col = btn_info[2]
            bg_color = btn_info[3]
            fg_color = btn_info[4]
            colspan = btn_info[5] if len(btn_info) > 5 else 1

            if colspan > 1:
                btn = tk.Button(
                    btn_frame,
                    text=text,
                    font=("Arial", 18, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    activebackground=bg_color,
                    activeforeground=fg_color,
                    bd=0,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)
            else:
                btn = tk.Button(
                    btn_frame,
                    text=text,
                    font=("Arial", 18, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    activebackground=bg_color,
                    activeforeground=fg_color,
                    bd=0,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        # Configure grid weights for responsive resizing
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.equation = ""
            self.display_var.set("")
        elif char == '=':
            try:
                # Sanitize / evaluate safely
                result = str(eval(self.equation))
                if result.endswith('.0'):
                    result = result[:-2]
                self.display_var.set(result)
                self.equation = result
            except ZeroDivisionError:
                messagebox.showerror("Error", "Division by zero is not allowed.")
                self.equation = ""
                self.display_var.set("")
            except Exception as e:
                messagebox.showerror("Error", "Invalid Expression")
                self.equation = ""
                self.display_var.set("")
        else:
            self.equation += str(char)
            self.display_var.set(self.equation)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
