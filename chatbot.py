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

    #Жанр

    for game in games:
        if game.lower() in question and "жанр" in question:
            for _, target, data in G.edges(game, data=True):
                if data ['relation'] == 'жанр':
                    return f"Жанр {game}: {target}"
                
    #Разработчик

    for game in games:
        if game.lower() in question and "разработчик" in question:
            for _, target, data in G.edges(game, data=True):
                if data ['relation'] == 'разработчик':
                    return f"{game} разработала: {target}"
                
    #Платформа

    for game in games:
        if game.lower() in question and "платформа" in question:
            platforms = []
            for _, target, data in G.edges(game, data=True):
                if data ['relation'] == 'платформа':
                    platforms.append(target)
            if platforms:
                    return f"{game} на: {', '.join(platforms)}"
                

    return "Не понял. Спроси про жанр, разработчика или платформы"

def ask():
    question = entry.get().lower()
    entry.delete(0, tk.END)
    chat.insert(tk.END, f"Ты: {question}\n")
    answer = get_answer(question)
    chat.insert(tk.END, f"Бот: {answer}\n\n")
    chat.see(tk.END)

btn.config(command=ask)

window.mainloop()



