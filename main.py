import tkinter as tk
from tkinter import messagebox
import math

class CasioFX991ESClone:
    def __init__(self, root):
        self.root = root
        self.root.title("Casio fx-991ES Simulator")
        self.root.geometry("380x550")
        self.root.configure(bg="#3A3A3A") # Casio dark grey body
        self.root.resizable(False, False)

        self.expression = ""

        # --- Calculator Display ---
        self.display_frame = tk.Frame(self.root, bg="#A0B2A6", bd=5, relief=tk.SUNKEN)
        self.display_frame.pack(pady=15, padx=15, fill="both")

        self.screen = tk.Label(
            self.display_frame, 
            text="0", 
            anchor="e", 
            font=("Consolas", 24), 
            bg="#A0B2A6", 
            fg="#000000", 
            height=2,
            padx=10
        )
        self.screen.pack(fill="both")

        # --- Key Layout Configuration ---
        # Matrix representing the layout matching Casio's functional positions
        self.buttons = [
            ['Shift', 'Alpha', 'Abs', 'M+', 'Mode'],
            ['sin', 'cos', 'tan', 'ln', 'log'],
            ['x²', 'x³', 'xⁿ', '√', '1/x'],
            ['7', '8', '9', 'DEL', 'AC'],
            ['4', '5', '6', '×', '÷'],
            ['1', '2', '3', '+', '-'],
            ['0', '.', 'Ans', 'Exp', '=']
        ]
        
        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#3A3A3A")
        button_frame.pack(padx=10, pady=5, fill="both", expand=True)

        for row_idx, row in enumerate(self.buttons):
            for col_idx, text in enumerate(row):
                # Styling adjustments based on Casio button types
                if text in ['AC', 'DEL']:
                    bg_color, fg_color = "#D96B27", "#FFFFFF" # Orange/amber function keys
                elif text in ['Shift', 'Alpha', 'Mode', 'sin', 'cos', 'tan', 'ln', 'log', 'x²', 'x³', 'xⁿ', '√', '1/x', 'Abs', 'M+']:
                    bg_color, fg_color = "#555555", "#FFFFFF" # Darker functional keys
                elif text == '=':
                    bg_color, fg_color = "#EEEEEE", "#000000"
                else:
                    bg_color, fg_color = "#FFFFFF", "#000000" # Standard number pad

                btn = tk.Button(
                    button_frame, 
                    text=text, 
                    font=("Arial", 11, "bold"),
                    bg=bg_color, 
                    fg=fg_color,
                    activebackground="#888888",
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=3, pady=3)
                
        # Configure equal grid weights
        for i in range(7):
            button_frame.rowconfigure(i, weight=1)
        for j in range(5):
            button_frame.columnconfigure(j, weight=1)

    def on_button_click(self, char):
        if char == "AC":
            self.expression = ""
            self.update_display("0")
        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.update_display(self.expression if self.expression else "0")
        elif char == "=":
            self.calculate_result()
        elif char in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
            # Append as a clear readable function string
            self.expression += f"{char}("
            self.update_display(self.expression)
        elif char == "×":
            self.expression += "*"
            self.update_display(self.expression)
        elif char == "÷":
            self.expression += "/"
            self.update_display(self.expression)
        elif char == "x²":
            self.expression += "**2"
            self.update_display(self.expression)
        elif char == "x³":
            self.expression += "**3"
            self.update_display(self.expression)
        elif char == "xⁿ":
            self.expression += "**"
            self.update_display(self.expression)
        else:
            self.expression += str(char)
            self.update_display(self.expression)

    def update_display(self, text):
        # Format string to look closer to a genuine scientific syntax on screen
        display_text = text.replace('*', '×').replace('/', '÷')
        if len(display_text) > 18:  # Prevents clipping
            display_text = display_text[-18:]
        self.screen.config(text=display_text)

    def calculate_result(self):
        try:
            # Safely inject mathematical equivalents into python's eval scope
            safe_dict = {
                "sin": lambda x: math.sin(math.radians(float(x))),
                "cos": lambda x: math.cos(math.radians(float(x))),
                "tan": lambda x: math.tan(math.radians(float(x))),
                "log": lambda x: math.log10(float(x)),
                "ln": lambda x: math.log(float(x)),
                "√": lambda x: math.sqrt(float(x)),
                "Abs": lambda x: abs(float(x)),
                "math": math
            }
            
            # Formatting structural adjustments for functional string brackets syntax helper
            eval_expr = self.expression
            
            # Simple fallback safety evaluation parser step
            result = eval(eval_expr, {"__builtins__": None}, safe_dict)
            
            # Format outputs elegantly
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 8)

            self.update_display(str(result))
            self.expression = str(result) # Carry over answer implicitly

        except Exception as e:
            messagebox.showerror("Math Error", "Invalid Syntax / Calculation Error")
            self.expression = ""
            self.update_display("0")

if __name__ == "__main__":
    root = tk.Tk()
    app = CasioFX991ESClone(root)
    root.mainloop()
              
