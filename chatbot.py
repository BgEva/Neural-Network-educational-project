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

    # Найти игру
    matched_game = None
    for game in games:
        if any(word in game.lower() for word in words):
            matched_game = game
            break

    if not matched_game:
        return "Не знаю такую игру."

    # Один проход по всем связям
    genres = []
    developers = []
    platforms = []
    publishers = []
    years = []
    series_list = []
    engines = []

    for _, target, data in G.edges(matched_game, data=True):
        rel = data['relation']
        if rel == 'жанр':
            genres.append(target)
        if 'разработчик' in rel:
            developers.append(target)
        if rel == 'платформа':
            platforms.append(target)
        if 'издатель' in rel:
            publishers.append(target)
        if rel == 'год':
            years.append(target)
        if rel == 'серия':
            series_list.append(target)
        if rel == 'движок':
            engines.append(target)

    if "разработчик" in question and developers:
        return f"{matched_game} разработала: {', '.join(developers)}"
    if "жанр" in question and genres:
        return f"Жанр {matched_game}: {', '.join(genres)}"
    if "платформ" in question and platforms:
        return f"{matched_game} на: {', '.join(platforms)}"
    if "издатель" in question and publishers:
        return f"Издатель {matched_game}: {', '.join(publishers)}"
    if "год" in question and years:
        return f"{matched_game} вышла в {', '.join(years)} году"
    if "сери" in question and series_list:
        return f"{matched_game} относится к серии: {', '.join(series_list)}"
    if "движок" in question and engines:
        return f"{matched_game} на движке: {', '.join(engines)}"

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



