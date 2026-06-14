import tkinter as tk
from tkinter import scrolledtext
from Neuro_mamykin_1 import G, games

# Создаём окно
window = tk.Tk()
window.title("Game Chatbot")
window.geometry("600x500")

# Поле чата
chat = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20)
chat.pack(pady=10)

# Поле ввода
entry = tk.Entry(window, width=50)
entry.pack(side=tk.LEFT, padx=5)

# Кнопка
btn = tk.Button(window, text="Отправить")
btn.pack(side=tk.LEFT)

def get_answer(question):
    question = question.lower()
    words = question.split()

    matched_game = None
    for game in games:
        if any(word in game.lower() for word in words):
            matched_game = game
            break

    if not matched_game:
        return "Не знаю такую игру."

    buckets = {
        'жанр': [],
        'разработчик': [],
        'платформа': [],
        'издатель': [],
        'год': [],
        'серия': [],
        'движок': [],
    }

    for _, target, data in G.edges(matched_game, data=True):
        rel = data['relation']
        for key in buckets:
            if key in rel:
                buckets[key].append(target)

    labels = {
        "жанр": ("жанр", buckets['жанр']),
        "разработчик": ("разработала", buckets['разработчик']),
        "платформ": ("на", buckets['платформа']),
        "издатель": ("издатель", buckets['издатель']),
        "год": ("вышла в", buckets['год']),
        "сери": ("серия", buckets['серия']),
        "движок": ("движок", buckets['движок']),
    }

    for word, (label, items) in labels.items():
        if word in question and items:
            return f"{matched_game} {label}: {', '.join(items)}"

    return "Не понял."

def ask():
    question = entry.get().lower()
    entry.delete(0, tk.END)
    chat.insert(tk.END, f"Ты: {question}\n")
    answer = get_answer(question)
    chat.insert(tk.END, f"Бот: {answer}\n\n")
    chat.see(tk.END)

btn.config(command=ask)

window.mainloop()



