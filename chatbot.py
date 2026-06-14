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

   # Разработчик
    if "разработчик" in question:
        for _, target, data in G.edges(matched_game, data=True):
            rel = data.get('relation', '')
            if 'разработчик' in rel:
                return f"{matched_game} разработала: {target}"

    # Жанр
    if "жанр" in question:
        for _, target, data in G.edges(matched_game, data=True):
            if data['relation'] == 'жанр':
                return f"Жанр {matched_game}: {target}"

    # Платформы
    if "платформ" in question:
        platforms = []
        for _, target, data in G.edges(matched_game, data=True):
            if data['relation'] == 'платформа':
                platforms.append(target)
        if platforms:
            return f"{matched_game} на: {', '.join(platforms)}"
        

    # Издатель
    if "издатель" in question:
        for _, target, data in G.edges(matched_game, data=True):
            rel = data.get('relation', '')
            if 'издатель' in rel:
                return f"{matched_game} издала: {target}"
            
    # год
    if "год" in question:
        for _, target, data in G.edges(matched_game, data=True):
            if data['relation'] == 'год':
                return f"{matched_game} вышла в {target} году"
            
    # Серия
    if "серия" in question:
        series = []
        for _, target, data in G.edges(matched_game, data=True):
            if data['relation'] == 'серия':
                series.append(target)
        if series:
            return f"{matched_game} относится к серии: {', '.join(series)}"
        
    # Движок
    if "движок" in question:
        for _, target, data in G.edges(matched_game, data=True):
            if data['relation'] == 'движок':
                return f"{matched_game} была разработана на движке {target}"



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



