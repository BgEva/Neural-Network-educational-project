import tkinter as tk
from tkinter import scrolledtext
from Neuro_mamykin_1 import G, games, GameNet, games_data
import torch
import random

context = {"last_game": None}

model = GameNet()
model.load_state_dict(torch.load("game_net.pth"))
model.eval()

def predict_game(description):
    """Предсказывает игру по описанию"""
    keywords = [
        ["открытый мир", "открытый"],  # 0
        ["прокачка", "rpg", "уровни"],  # 1
        ["мультиплеер", "кооп", "онлайн"],  # 2
        ["реалистичная графика", "реализм"],  # 3
        ["фэнтези", "магия", "эльфы"],  # 4
        ["научная фантастика", "сайфай", "роботы", "будущее"],  # 5
        ["человек", "люди"],  # 6
        ["реального времени", "экшен"],  # 7
        ["хоррор", "ужасы", "страх"],  # 8
        ["jrpg", "японская"],  # 9
        ["крафт", "сбор", "ресурсы"],  # 10
        ["одиночная", "соло"],  # 11
    ]
    
    vector = []
    for words in keywords:
        if any(w in description.lower() for w in words):
            vector.append(1)
        else:
            vector.append(0)
    
    x = torch.tensor([vector], dtype=torch.float32)
    with torch.no_grad():
        output = model(x)
        pred = torch.argmax(output, dim=1).item()
    
    game_names = ["Nier Automata", "Final Fantasy VII", "Zelda Breath of the Wild", 
                  "Monster Hunter World", "Resident Evil 2"]
    return game_names[pred]

# Создаём окно
window = tk.Tk()
window.title("Game Chatbot")
window.geometry("600x550")

chat = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20)
chat.pack(pady=10)

# Фрейм для ввода
input_frame = tk.Frame(window)
input_frame.pack()

entry = tk.Entry(input_frame, width=40)
entry.pack(side=tk.LEFT, padx=5)

btn = tk.Button(input_frame, text="Отправить")
btn.pack(side=tk.LEFT, padx=2)

def get_answer(question):
    question = question.lower()
    words = question.split()

    # Small talk
    if any(g in question for g in ["привет", "здравствуй", "хай", "добрый день"]):
        return "Привет! Я геймер-бот с нейросетью. Могу рассказать о 5 играх или подобрать игру по описанию. Спроси: 'жанр Nier', 'платформы Zelda', или 'посоветуй игру фэнтези открытый мир'!"
    
    if any(g in question for g in ["пока", "до свидания", "bye"]):
        return "До новых встреч! Приходи ещё за игровыми советами."
    
    if any(g in question for g in ["спасибо", "благодарю", "спс"]):
        return random.choice(["Всегда пожалуйста!", "Рад помочь!", "Обращайся!"])
    
    if any(g in question for g in ["что ты умеешь", "что можешь", "помощь"]):
        return "Я использую нейросеть для подбора игр и базу знаний для ответов. Скажи 'посоветуй игру' и опиши что нравится, или спроси про конкретную игру: жанр, платформы, год, движок, серия."

    # Подбор игры через нейросеть
    if "подобрать" in question or "порекомендуй" in question or "посоветуй" in question:
        game = predict_game(question)
        context["last_game"] = game
        return f"🎮 Нейросеть рекомендует: {game}!\nСпроси про жанр, платформы или разработчика."

    # Запрос на подбор
    suggest_words = ["фэнтези", "фентези", "хоррор", "ужасы", "сайфай", "открытый мир", "jrpg"]
    if not any(w in question for w in ["жанр", "разработчик", "платформ", "издатель", "год", "сери", "движок", "порекомендуй", "посоветуй", "подобрать"]):
        if any(w in question for w in suggest_words):
            return "Хочешь подобрать игру? Напиши 'посоветуй игру' и описание (например: посоветуй игру фэнтези открытый мир)."


    matched_game = None
    for game in games:
        if any(word in game.lower() for word in words):
            matched_game = game
            break

    context_triggers = ["жанр", "разработчик", "платформ", "издатель", "год", "сери", "движок"]
    if not matched_game and any(w in question for w in context_triggers) and context["last_game"]:
        matched_game = context["last_game"]

    if matched_game:
        context["last_game"] = matched_game

    # Обратный поиск
    if not matched_game:
        results = []
        for game in games:
            for _, target, data in G.edges(game, data=True):
                rel = data['relation']
                target_words = target.lower().split()
                if any(tw in words for tw in target_words):
                    results.append((game, rel, target))
        seen = set()
        unique = []
        for game, rel, target in results:
            key = (game, target)
            if key not in seen:
                seen.add(key)
                unique.append(f"{game} ({rel}: {target})")
        if unique:
            return "Нашёл:\n" + "\n".join(unique)
        return "Не знаю такую игру. Можешь спросить про конкретную игру или попросить подобрать!"

    buckets = {
        'жанр': [], 'разработчик': [], 'платформа': [],
        'издатель': [], 'год': [], 'серия': [], 'движок': [],
    }

    for _, target, data in G.edges(matched_game, data=True):
        rel = data['relation']
        for key in buckets:
            if key in rel:
                buckets[key].append(target)

    templates = {
        "жанр": ["{} — это {}", "{} относится к жанру {}", "Я бы сказал, что {} это {}"],
        "разработчик": ["{} создала студия {}", "{} разработала {}", "Над {} работали {}"],
        "платформ": ["{} вышла на {}", "{} доступна на {}", "В {} можно поиграть на {}"],
        "издатель": ["{} издала {}", "Издатель {} — {}", "{} выпустила в свет {}"],
        "год": ["{} вышла в {} году", "Релиз {} состоялся в {}", "{} увидела свет в {}"],
        "серия": ["{} входит в серию {}", "{} — часть франшизы {}", "{} относится к серии игр {}"],
        "движок": ["{} работает на движке {}", "{} использует {}", "Движок {} — {}"],
    }

    for word, t_list in templates.items():
        key = "платформа" if word == "платформ" else word
        if word in question and buckets[key]:
            items = buckets[key]
            template = random.choice(t_list)
            return template.format(matched_game, ', '.join(items))

    # Если просто название игры без вопроса
    return f"🎮 {matched_game}! Что хочешь узнать? Жанр, платформы, разработчик, год, серия, движок?"

def ask():
    question = entry.get()
    entry.delete(0, tk.END)
    chat.insert(tk.END, f"Ты: {question}\n")
    answer = get_answer(question)
    chat.insert(tk.END, f"Бот: {answer}\n\n")
    chat.see(tk.END)

def recommend():
    entry.delete(0, tk.END)
    entry.insert(0, "посоветуй игру ")
    entry.focus_set()

btn.config(command=ask)

window.mainloop()