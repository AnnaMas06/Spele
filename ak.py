import tkinter as tk
from tkinter import messagebox
import random
import json
import requests


HAND_EMOJIS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️"
}
HAND_CHOICES = list(HAND_EMOJIS.keys())
RANKINGS_FILE = "rankings.json"


def load_rankings():
    try:
        with open(RANKINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_rankings(rankings):
    with open(RANKINGS_FILE, "w") as f:
        json.dump(rankings, f, indent=2)

def update_rankings(winner):
    rankings = load_rankings()
    rankings[winner] = rankings.get(winner, 0) + 1
    save_rankings(rankings)


class RPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.mode = None
        self.names = ["", ""]
        self.choices = [None, None]
        self.current_player = 0

        self.build_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Rock Paper Scissors", font=("Arial", 20)).pack(pady=10)
        tk.Button(self.root, text="1 Player Game", command=lambda: self.start_setup(1)).pack(pady=5)
        tk.Button(self.root, text="2 Player Game", command=lambda: self.start_setup(2)).pack(pady=5)

    def start_setup(self, mode):
        self.mode = mode
        self.clear_screen()

        tk.Label(self.root, text="Enter Player Names").pack()
        self.name1_entry = tk.Entry(self.root)
        self.name1_entry.pack(pady=2)

        if mode == 2:
            self.name2_entry = tk.Entry(self.root)
            self.name2_entry.pack(pady=2)
        else:
            self.name2_entry = None

        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=10)
        tk.Button(self.root, text="Show Rules", command=self.show_rules).pack(pady=2)
        tk.Button(self.root, text="Ranking", command=self.show_rankings).pack(pady=2)

    def show_rules(self):
        rules = "Rock beats Scissors\nScissors beats Paper\nPaper beats Rock"
        messagebox.showinfo("Rules", rules)

    def show_rankings(self):
        rankings = load_rankings()
        ranking_text = "\n".join([f'{name}: {wins} wins' for name, wins in sorted(rankings.items(), key=lambda x: x[1], reverse=True)])
        messagebox.showinfo("Rankings", ranking_text or "No rankings yet.")

    def start_game(self):
        self.names[0] = self.name1_entry.get()
        self.names[1] = self.name2_entry.get() if self.name2_entry else "Computer"
        self.choices = [None, None]
        self.current_player = 0
        self.show_hand_choice()

    def show_hand_choice(self):
        self.clear_screen()
        prompt = f"{self.names[self.current_player]}'s turn. Choose your hand:"
        tk.Label(self.root, text=prompt).pack(pady=10)

        for hand in HAND_CHOICES:
            tk.Button(self.root, text=f'{HAND_EMOJIS[hand]} {hand.capitalize()}', width=20,
                      command=lambda h=hand: self.record_choice(h)).pack(pady=2)

    def record_choice(self, hand):
        self.choices[self.current_player] = hand

        if self.mode == 1:
            self.choices[1] = random.choice(HAND_CHOICES)
            self.show_result()
        elif self.current_player == 0:
            self.current_player = 1
            self.show_hand_choice()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()
        p1, p2 = self.choices
        outcome = f"{self.names[0]} chose {HAND_EMOJIS[p1]}, {self.names[1]} chose {HAND_EMOJIS[p2]}\n\n"

        if p1 == p2:
            outcome += "It's a draw!"
        elif (p1 == "rock" and p2 == "scissors") or (p1 == "scissors" and p2 == "paper") or (p1 == "paper" and p2 == "rock"):
            outcome += f"{self.names[0]} wins!"
            update_rankings(self.names[0])
        else:
            outcome += f"{self.names[1]} wins!"
            update_rankings(self.names[1])

        tk.Label(self.root, text=outcome, font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Play Again", command=self.start_setup_again).pack(pady=5)
        tk.Button(self.root, text="Main Menu", command=self.build_main_menu).pack(pady=5)
        tk.Button(self.root, text="Get a Joke", command=self.show_joke).pack(pady=5)

    def start_setup_again(self):
        self.choices = [None, None]
        self.current_player = 0
        self.show_hand_choice()

    def show_joke(self):
        try:
            res = requests.get("https://official-joke-api.appspot.com/random_joke").json()
            joke = f"{res['setup']}\n{res['punchline']}"
            messagebox.showinfo("Joke", joke)
        except:
            messagebox.showwarning("Oops!", "Couldn't fetch a joke right now.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RPSApp(root)
    root.mainloop()
