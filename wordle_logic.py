from typing import List, Tuple
import random
import os

DEFAULT_WORDS: List[str] = []

class WordleLogic:
    def __init__(self, word_list: List[str] = None, target: str = None, max_attempts: int = 6):
        if word_list is None:
            try:
                with open("words.txt", "r") as f:
                    word_list = [w.strip().lower() for w in f if len(w.strip()) == 5 and w.strip().isalpha()]
            except FileNotFoundError:
                raise FileNotFoundError("words.txt not found. Please add a file with 5-letter words.")
        self.word_list = [w.lower() for w in word_list if len(w) == 5]
        if not self.word_list:
            raise ValueError("word_list must contain some 5-letter words")
        self.max_attempts = max_attempts
        self._target_override = target.lower() if target else None
        self.valid_guesses = None
        if os.path.exists("guesses.txt"):
            try:
                with open("guesses.txt", "r") as gf:
                    self.valid_guesses = set(w.strip().lower() for w in gf if len(w.strip()) == 5 and w.strip().isalpha())
            except Exception:
                self.valid_guesses = None
        self.reset()

    def reset(self):
        self.target = self._target_override or random.choice(self.word_list)
        self.attempts = []
        self.finished = False
        self.won = False

    def _validate_guess(self, guess: str) -> Tuple[bool, str]:
        if len(guess) != 5:
            return False, "Guess must be 5 letters"
        if not guess.isalpha():
            return False, "Guess must contain only letters"
        if self.valid_guesses is not None and guess.lower() not in self.valid_guesses:
            return False, "Guess not in valid guesses list"
        return True, "ok"

    def guess(self, guess_word: str) -> Tuple[List[str], bool, str]:
        if self.finished:
            return [], True, "Game already finished"
        guess_word = guess_word.lower()
        valid, msg = self._validate_guess(guess_word)
        if not valid:
            return [], False, msg
        target = list(self.target)
        guess = list(guess_word)
        feedback = [None] * 5
        target_taken = [False] * 5
        for i in range(5):
            if guess[i] == target[i]:
                feedback[i] = "correct"
                target_taken[i] = True
        for i in range(5):
            if feedback[i] is None:
                found = False
                for j in range(5):
                    if not target_taken[j] and guess[i] == target[j]:
                        found = True
                        target_taken[j] = True
                        break
                feedback[i] = "present" if found else "absent"
        self.attempts.append((guess_word, feedback))
        if guess_word == self.target:
            self.finished = True
            self.won = True
            return feedback, True, "Correct! You won."
        if len(self.attempts) >= self.max_attempts:
            self.finished = True
            return feedback, True, f"Out of attempts. The word was '{self.target}'."
        return feedback, False, "Try again"
