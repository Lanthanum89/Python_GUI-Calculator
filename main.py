import tkinter as tk
from tkinter import messagebox
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter GUI Calculator")
        self.geometry("480x420")  # Wider for history panel
        self.resizable(True, True)
        # Theme colors
        self.themes = {
            'light': {
                'bg': '#f8c9e1',
                'input_bg': '#ffb6c1',
                'input_fg': 'white',
                'btn_bg': '#f785be',
                'btn_fg': 'white',
                'btn_active_bg': '#ffb6c1',
                'btn_active_fg': 'white',
                'history_bg': '#ffe3f0',
                'history_fg': '#a14d7f',
                'listbox_bg': '#fff0fa',
                'listbox_fg': '#a14d7f',
            },
            'dark': {
                'bg': '#7a3161',
                'input_bg': '#a14d7f',
                'input_fg': 'white',
                'btn_bg': '#c85a9e',
                'btn_fg': 'white',
                'btn_active_bg': '#a14d7f',
                'btn_active_fg': 'white',
                'history_bg': '#4a2040',
                'history_fg': '#ffe3f0',
                'listbox_bg': '#a14d7f',
                'listbox_fg': '#ffe3f0',
            }
        }
        self.theme = 'light'
        self.history = []
        self._create_widgets()
        self.bind_all('<Key>', self._on_key_press)

    def _on_key_press(self, event):
        key = event.keysym
        char = event.char
        # Allow numbers, operators, parentheses, dot
        if char in '0123456789+-*/().':
            self._on_button_click(char)
        elif key == 'Return':
            self._on_button_click('=')
        elif key == 'BackSpace':
            self._on_button_click('<-')
        elif key == 'Escape':
            self._on_button_click('C')

    def _create_widgets(self):
        self.expression = ""
        self.input_text = tk.StringVar()
        colors = self.themes[self.theme]

        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill="both", expand=True)

        # Calculator area (left)
        calc_frame = tk.Frame(main_frame, width=312, height=420, bg=colors['bg'])
        calc_frame.pack(side=tk.LEFT, fill="both", expand=False)

        # Theme toggle button
        theme_btn = tk.Button(calc_frame, text="Toggle Theme", font=("Arial", 10, "bold"),
                                bg=colors['btn_bg'], fg=colors['btn_fg'],
                                activebackground=colors['btn_active_bg'], activeforeground=colors['btn_active_fg'],
                                command=self._toggle_theme)
        theme_btn.pack(side=tk.TOP, anchor="ne", padx=8, pady=8)

        input_frame = tk.Frame(calc_frame, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg=colors['bg'])
        input_frame.pack(side=tk.TOP)

        self.input_field = tk.Entry(input_frame, font=('Helvetica', 24, 'bold'), textvariable=self.input_text, width=50, bg=colors['input_bg'], fg=colors['input_fg'], bd=0, justify=tk.RIGHT, insertbackground=colors['input_fg'])
        self.input_field.grid(row=0, column=0)
        self.input_field.pack(ipady=15)

        # Bind copy/paste keyboard shortcuts
        self.input_field.bind('<Control-c>', self._copy_result)
        self.input_field.bind('<Control-C>', self._copy_result)
        self.input_field.bind('<Control-v>', self._paste_clipboard)
        self.input_field.bind('<Control-V>', self._paste_clipboard)

        # Add right-click context menu for copy/paste
        self.menu = tk.Menu(self.input_field, tearoff=0)
        self.menu.add_command(label="Copy", command=self._copy_result)
        self.menu.add_command(label="Paste", command=self._paste_clipboard)
        self.input_field.bind('<Button-3>', self._show_context_menu)
    def _copy_result(self, event=None):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.input_text.get())
        except Exception:
            pass
        return 'break'

    def _paste_clipboard(self, event=None):
        try:
            paste = self.clipboard_get()
            # Only allow numbers, operators, and functions
            allowed = '0123456789+-*/().^'
            for func in ['sin', 'cos', 'tan', 'log', 'sqrt']:
                paste = paste.replace(func, '')
            if all(c in allowed or c.isspace() for c in paste):
                self.expression += paste.strip()
                self.input_text.set(self.expression)
        except Exception:
            pass
        return 'break'

    def _show_context_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    # --- The following code was previously outside the method, now properly indented ---
    def _create_widgets_continued(self, main_frame, calc_frame, colors):
        btns_frame = tk.Frame(calc_frame, width=312, height=272.5, bg=colors['bg'])
        btns_frame.pack(expand=True, fill="both")

        buttons = [
            ["sin", "cos", "tan", "log"],
            ["sqrt", "^", "(", ")"],
            ["C", "/", "*", "<-"]
            , ["7", "8", "9", "-"]
            , ["4", "5", "6", "+"]
            , ["1", "2", "3", "="]
            , ["0", ".", "", ""]
        ]

        # Configure grid weights for even resizing
        for i in range(len(buttons)):
            btns_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btns_frame.columnconfigure(j, weight=1)

        self.button_refs = []
        for i, row in enumerate(buttons):
            btn_row = []
            for j, btn_text in enumerate(row):
                if btn_text:
                    btn = tk.Button(
                        btns_frame, text=btn_text, fg=colors['btn_fg'], bd=0, bg=colors['btn_bg'],
                        font=('Arial', 20, 'bold'),
                        activebackground=colors['btn_active_bg'], activeforeground=colors['btn_active_fg'],
                        cursor="hand2", command=lambda x=btn_text: self._on_button_click(x)
                    )
                    btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                    btn_row.append(btn)
                else:
                    btn_row.append(None)
            self.button_refs.append(btn_row)

        # History area (right)
        history_frame = tk.Frame(main_frame, width=160, bg=colors['history_bg'], bd=2, relief=tk.GROOVE)
        history_frame.pack(side=tk.RIGHT, fill="y")
        history_label = tk.Label(history_frame, text="History", font=("Helvetica", 14, "bold"), bg=colors['history_bg'], fg=colors['history_fg'])
        history_label.pack(pady=(10,0))
        self.history_listbox = tk.Listbox(history_frame, font=("Helvetica", 12), bg=colors['listbox_bg'], fg=colors['listbox_fg'], bd=0, highlightthickness=0)
        self.history_listbox.pack(fill="both", expand=True, padx=8, pady=8)

    # Call the continued widget creation at the end of _create_widgets
    def _create_widgets(self):
        self.expression = ""
        self.input_text = tk.StringVar()
        colors = self.themes[self.theme]

        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill="both", expand=True)

        # Calculator area (left)
        calc_frame = tk.Frame(main_frame, width=312, height=420, bg=colors['bg'])
        calc_frame.pack(side=tk.LEFT, fill="both", expand=False)

        # Theme toggle button
        theme_btn = tk.Button(calc_frame, text="Toggle Theme", font=("Arial", 10, "bold"),
                                bg=colors['btn_bg'], fg=colors['btn_fg'],
                                activebackground=colors['btn_active_bg'], activeforeground=colors['btn_active_fg'],
                                command=self._toggle_theme)
        theme_btn.pack(side=tk.TOP, anchor="ne", padx=8, pady=8)

        input_frame = tk.Frame(calc_frame, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg=colors['bg'])
        input_frame.pack(side=tk.TOP)

        self.input_field = tk.Entry(input_frame, font=('Helvetica', 24, 'bold'), textvariable=self.input_text, width=50, bg=colors['input_bg'], fg=colors['input_fg'], bd=0, justify=tk.RIGHT, insertbackground=colors['input_fg'])
        self.input_field.grid(row=0, column=0)
        self.input_field.pack(ipady=15)

        # Bind copy/paste keyboard shortcuts
        self.input_field.bind('<Control-c>', self._copy_result)
        self.input_field.bind('<Control-C>', self._copy_result)
        self.input_field.bind('<Control-v>', self._paste_clipboard)
        self.input_field.bind('<Control-V>', self._paste_clipboard)

        # Add right-click context menu for copy/paste
        self.menu = tk.Menu(self.input_field, tearoff=0)
        self.menu.add_command(label="Copy", command=self._copy_result)
        self.menu.add_command(label="Paste", command=self._paste_clipboard)
        self.input_field.bind('<Button-3>', self._show_context_menu)

        # Continue widget creation
        self._create_widgets_continued(main_frame, calc_frame, colors)
    def _toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self._update_theme()

    def _update_theme(self):
        colors = self.themes[self.theme]
        self.configure(bg=colors['bg'])
        # Update all frames and widgets
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=colors['bg'])
        # Update input field
        self.input_field.configure(bg=colors['input_bg'], fg=colors['input_fg'], insertbackground=colors['input_fg'])
        # Update buttons
        for row in self.button_refs:
            for btn in row:
                if btn:
                    btn.configure(bg=colors['btn_bg'], fg=colors['btn_fg'], activebackground=colors['btn_active_bg'], activeforeground=colors['btn_active_fg'])
        # Update history panel
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, tk.Frame):
                        subwidget.configure(bg=colors['bg'])
                    elif isinstance(subwidget, tk.Label):
                        subwidget.configure(bg=colors['history_bg'], fg=colors['history_fg'])
                    elif isinstance(subwidget, tk.Listbox):
                        subwidget.configure(bg=colors['listbox_bg'], fg=colors['listbox_fg'])

    def _on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.input_text.set("")
        elif char == "<-":
            self.expression = self.expression[:-1]
            self.input_text.set(self.expression)
        elif char == "=":
            try:
                expr = self.expression.replace('^', '**')
                expr = expr.replace('sin', 'math.sin')
                expr = expr.replace('cos', 'math.cos')
                expr = expr.replace('tan', 'math.tan')
                expr = expr.replace('log', 'math.log10')
                expr = expr.replace('sqrt', 'math.sqrt')
                result = str(eval(expr, {"math": math, "__builtins__": {}}))
                self.input_text.set(result)
                self._add_to_history(self.expression, result)
                self.expression = result
            except ZeroDivisionError:
                messagebox.showerror("Math Error", "Division by zero is not allowed.")
                self.input_text.set("")
                self.expression = ""
            except ValueError as ve:
                messagebox.showerror("Math Error", f"Math domain error: {ve}")
                self.input_text.set("")
                self.expression = ""
            except SyntaxError:
                messagebox.showerror("Input Error", "Syntax error: Please check your expression.")
                self.input_text.set("")
                self.expression = ""
            except Exception as e:
                messagebox.showerror("Error", f"Invalid Input: {e}")
                self.input_text.set("")
                self.expression = ""
        else:
            if char in ["sin", "cos", "tan", "log", "sqrt"]:
                self.expression += f"{char}("
            elif char == "^":
                self.expression += "^"
            else:
                self.expression += str(char)
            self.input_text.set(self.expression)

    def _add_to_history(self, expr, result):
        entry = f"{expr} = {result}"
        self.history.append(entry)
        self.history_listbox.insert(tk.END, entry)
        # Optionally, keep only the last 20 entries
        if len(self.history) > 20:
            self.history.pop(0)
            self.history_listbox.delete(0)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

