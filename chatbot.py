import tkinter as tk
from tkinter import scrolledtext
from Neuro_mamykin_1 import G, games
import random

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

    templates = {
        "жанр": [
            "{} — это {}", 
            "{} относится к жанру {}", 
            "Я бы сказал, что {} это {}"
        ],
        "разработчик": [
            "{} создала студия {}",
            "{} разработала {}",
            "Над {} работали {}"
        ],
        "платформ": [
            "{} вышла на {}",
            "{} доступна на {}",
            "В {} можно поиграть на {}"
        ],
        "издатель": [
            "{} издала {}",
            "Издатель {} — {}",
            "{} выпустила в свет {}"
        ],
        "год": [
            "{} вышла в {} году",
            "Релиз {} состоялся в {}",
            "{} увидела свет в {}"
        ],
        "сери": [
            "{} входит в серию {}",
            "{} — часть франшизы {}",
            "{} относится к серии игр {}"
        ],
        "движок": [
            "{} работает на движке {}",
            "{} использует {}",
            "Движок {} — {}"
        ],
    }

    for word, t_list in templates.items():
        if word in question and buckets[word if word != "платформ" else "платформа"]:
            items = buckets[word if word != "платформ" else "платформа"]
            template = random.choice(t_list)
            return template.format(matched_game, ', '.join(items))

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



