import tkinter as tk
from tkinter import messagebox
from wordle_logic import WordleLogic

class WordleGUI(tk.Tk):
    def __init__(self, logic: WordleLogic):
        super().__init__()
        self.logic = logic
        self.title("Wordle")
        self.resizable(False, False)
        self.current_row = 0
        self.current_col = 0
        self.guess_chars = [""] * 5
        self._create_widgets()
        self.bind_all("<Key>", self._on_key)

    def _create_widgets(self):
        pad = 6
        self.grid_frame = tk.Frame(self, padx=pad, pady=pad)
        self.grid_frame.pack()
        self.cells = []
        for r in range(6):
            row = []
            for c in range(5):
                lbl = tk.Label(self.grid_frame, text=" ", width=4, height=2, relief="solid", font=("Helvetica", 18), bg="white")
                lbl.grid(row=r, column=c, padx=3, pady=3)
                row.append(lbl)
            self.cells.append(row)
        self.info_label = tk.Label(self, text="Type letters, Enter to submit, Backspace to delete")
        self.info_label.pack(pady=(0,8))
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=(0,8))
        tk.Button(btn_frame, text="New Game", command=self._new_game).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Show Answer", command=self._show_answer).pack(side="left", padx=4)

    def _on_key(self, event):
        if self.logic.finished:
            return
        key = event.keysym
        if key == "Return":
            self._submit_guess()
        elif key == "BackSpace":
            self._delete_letter()
        elif len(event.char) == 1 and event.char.isalpha():
            self._add_letter(event.char)

    def _add_letter(self, ch):
        if self.current_col >= 5 or self.current_row >= 6:
            return
        ch = ch.lower()
        self.guess_chars[self.current_col] = ch
        self.cells[self.current_row][self.current_col]["text"] = ch.upper()
        self.current_col += 1

    def _delete_letter(self):
        if self.current_col <= 0:
            return
        self.current_col -= 1
        self.guess_chars[self.current_col] = ""
        self.cells[self.current_row][self.current_col]["text"] = " "

    def _submit_guess(self):
        if self.current_col != 5:
            self._flash_message("Not enough letters")
            return
        guess = "".join(self.guess_chars)
        feedback, finished, msg = self.logic.guess(guess)
        if not feedback:
            self._flash_message(msg)
            return
        for i, status in enumerate(feedback):
            lbl = self.cells[self.current_row][i]
            if status == "correct":
                lbl["bg"] = "#6aaa64"
                lbl["fg"] = "white"
            elif status == "present":
                lbl["bg"] = "#c9b458"
                lbl["fg"] = "white"
            else:
                lbl["bg"] = "#787c7e"
                lbl["fg"] = "white"
        if finished:
            if self.logic.won:
                messagebox.showinfo("Wordle", f"You won! The word was {self.logic.target.upper()}")
            else:
                messagebox.showinfo("Wordle", f"Game over. The word was {self.logic.target.upper()}")
            return
        self.current_row += 1
        self.current_col = 0
        self.guess_chars = [""] * 5

    def _new_game(self):
        self.logic.reset()
        self.current_row = 0
        self.current_col = 0
        self.guess_chars = [""] * 5
        for r in range(6):
            for c in range(5):
                self.cells[r][c]["text"] = " "
                self.cells[r][c]["bg"] = "white"
                self.cells[r][c]["fg"] = "black"

    def _show_answer(self):
        messagebox.showinfo("Answer", f"The word is: {self.logic.target.upper()}")

    def _flash_message(self, msg: str):
        old = self.info_label["text"]
        self.info_label["text"] = msg
        self.after(1200, lambda: self.info_label.config(text=old))

if __name__ == "__main__":
    logic = WordleLogic()
    app = WordleGUI(logic)
    app.mainloop()
