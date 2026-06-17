import torch
import torch.nn as nn
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

# 12 признаков
nier_automata = [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1]
final_fantasy_7 = [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1]
zelda_botw = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1]
monster_hunter_world = [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1]
resident_evil_2 = [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1]

games_data = [
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1],
]

games_name = ["Nier Automata", "Final Fantasy VII", "Zelda Breath of the Wild", "Monster Hunter World", "Resident Evil 2"]

X = torch.tensor(games_data, dtype=torch.float32)
y = torch.tensor([0, 1, 2, 3, 4], dtype=torch.long)

class GameNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(12, 8)
        self.fc2 = nn.Linear(8, 5)

    def forward(self, x):
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        return x

model = GameNet()
print(model)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

for epoch in range(500):
    outputs = model(X)
    loss = criterion(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 100 == 0:
        print(f"Эпоха {epoch+1}/500, ошибка: {loss.item():.4f}")

# ===== ГРАФ =====
G = nx.DiGraph()
games = ["Nier Automata", "Final Fantasy VII", "Zelda Breath of the Wild", "Monster Hunter World", "Resident Evil 2"]
G.add_nodes_from(games)

all_nodes = ["Action RPG", "JRPG", "Action-Adventure", "Survival Horror",
             "RPG", "Horror", "Adventure", "Action", "Жанр",
             "Экшен", "Японская RPG", "Ужасы", "Приключенческий экшен",
             "Platinum games", "Square Enix", "Nintendo", "Capcom", "Разработчик",
             "PC", "PlayStation", "PlayStation 4", "PlayStation 5",
             "Xbox", "Xbox One", "Xbox series X/S", "Nintendo Switch", "Wii u", "Платформа",
             "Сюжет", "Геймплей", "Саундтрек", "Система материи",
             "Открытый мир", "Система готовки", "Охота", "Крафт брони",
             "Зомби", "Убежище",
             "Персонаж 2B", "Персонаж Клауд", "Персонаж Линк", "Персонаж Леон",
             "2017", "1997", "2018", "2019",
             "Nier", "Drakengard", "Drag-on Dragoon",
             "Final Fantasy", "The Legend of Zelda", "Monster Hunter", "Resident Evil", "Biohazard",
             "Platinum Engine", "Square Engine", "Havok", "MT Framework", "RE Engine"]

G.add_nodes_from(all_nodes)

# Жанры
G.add_edge("Nier Automata", "Action RPG", relation="жанр")
G.add_edge("Final Fantasy VII", "JRPG", relation="жанр")
G.add_edge("Zelda Breath of the Wild", "Action-Adventure", relation="жанр")
G.add_edge("Monster Hunter World", "Action RPG", relation="жанр")
G.add_edge("Resident Evil 2", "Survival Horror", relation="жанр")

# AKO
G.add_edge("Action RPG", "Экшен", relation="AKO")
G.add_edge("JRPG", "Японская RPG", relation="AKO")
G.add_edge("Survival Horror", "Ужасы", relation="AKO")
G.add_edge("Action-Adventure", "Приключенческий экшен", relation="AKO")

# ISA
G.add_edge("Action RPG", "RPG", relation="ISA")
G.add_edge("JRPG", "RPG", relation="ISA")
G.add_edge("Survival Horror", "Horror", relation="ISA")
G.add_edge("Action-Adventure", "Adventure", relation="ISA")
G.add_edge("RPG", "Жанр", relation="ISA")
G.add_edge("Horror", "Жанр", relation="ISA")
G.add_edge("Adventure", "Жанр", relation="ISA")
G.add_edge("Action", "Жанр", relation="ISA")

# Разработчики
G.add_edge("Platinum games", "Разработчик", relation="ISA")
G.add_edge("Square Enix", "Разработчик", relation="ISA")
G.add_edge("Nintendo", "Разработчик", relation="ISA")
G.add_edge("Capcom", "Разработчик", relation="ISA")

# Платформы
G.add_edge("PC", "Платформа", relation="ISA")
G.add_edge("PlayStation", "Платформа", relation="ISA")
G.add_edge("PlayStation 4", "PlayStation", relation="ISA")
G.add_edge("PlayStation 5", "PlayStation", relation="ISA")
G.add_edge("Xbox One", "Xbox", relation="ISA")
G.add_edge("Xbox series X/S", "Xbox", relation="ISA")
G.add_edge("Nintendo Switch", "Nintendo", relation="ISA")
G.add_edge("Wii u", "Nintendo", relation="ISA")
G.add_edge("Xbox", "Платформа", relation="ISA")
G.add_edge("Nintendo", "Платформа", relation="ISA")

# Part-Of
G.add_edge("Сюжет", "Nier Automata", relation="Part-Of")
G.add_edge("Геймплей", "Nier Automata", relation="Part-Of")
G.add_edge("Саундтрек", "Nier Automata", relation="Part-Of")
G.add_edge("Персонаж 2B", "Nier Automata", relation="Part-Of")
G.add_edge("Сюжет", "Final Fantasy VII", relation="Part-Of")
G.add_edge("Персонаж Клауд", "Final Fantasy VII", relation="Part-Of")
G.add_edge("Система материи", "Final Fantasy VII", relation="Part-Of")
G.add_edge("Открытый мир", "Zelda Breath of the Wild", relation="Part-Of")
G.add_edge("Система готовки", "Zelda Breath of the Wild", relation="Part-Of")
G.add_edge("Персонаж Линк", "Zelda Breath of the Wild", relation="Part-Of")
G.add_edge("Охота", "Monster Hunter World", relation="Part-Of")
G.add_edge("Крафт брони", "Monster Hunter World", relation="Part-Of")
G.add_edge("Зомби", "Resident Evil 2", relation="Part-Of")
G.add_edge("Убежище", "Resident Evil 2", relation="Part-Of")
G.add_edge("Персонаж Леон", "Resident Evil 2", relation="Part-Of")

# Разработчик/издатель
G.add_edge("Final Fantasy VII", "Square Enix", relation="разработчик/издатель")
G.add_edge("Zelda Breath of the Wild", "Nintendo", relation="разработчик/издатель")
G.add_edge("Monster Hunter World", "Capcom", relation="разработчик/издатель")
G.add_edge("Resident Evil 2", "Capcom", relation="разработчик/издатель")
G.add_edge("Nier Automata", "Platinum games", relation="разработчик")
G.add_edge("Nier Automata", "Square Enix", relation="издатель")

# Платформы
G.add_edge("Nier Automata", "PC", relation="платформа")
G.add_edge("Nier Automata", "PlayStation 4", relation="платформа")
G.add_edge("Nier Automata", "Xbox One", relation="платформа")
G.add_edge("Nier Automata", "Nintendo Switch", relation="платформа")
G.add_edge("Final Fantasy VII", "PlayStation", relation="платформа")
G.add_edge("Final Fantasy VII", "PlayStation 4", relation="платформа")
G.add_edge("Final Fantasy VII", "Xbox One", relation="платформа")
G.add_edge("Final Fantasy VII", "Nintendo Switch", relation="платформа")
G.add_edge("Final Fantasy VII", "PC", relation="платформа")
G.add_edge("Zelda Breath of the Wild", "Nintendo Switch", relation="платформа")
G.add_edge("Zelda Breath of the Wild", "Wii u", relation="платформа")
G.add_edge("Monster Hunter World", "PlayStation 4", relation="платформа")
G.add_edge("Monster Hunter World", "Xbox One", relation="платформа")
G.add_edge("Monster Hunter World", "PC", relation="платформа")
G.add_edge("Resident Evil 2", "PlayStation 4", relation="платформа")
G.add_edge("Resident Evil 2", "PlayStation 5", relation="платформа")
G.add_edge("Resident Evil 2", "Xbox One", relation="платформа")
G.add_edge("Resident Evil 2", "Xbox series X/S", relation="платформа")
G.add_edge("Resident Evil 2", "Nintendo Switch", relation="платформа")
G.add_edge("Resident Evil 2", "PC", relation="платформа")

# Год
G.add_edge("Nier Automata", "2017", relation="год")
G.add_edge("Final Fantasy VII", "1997", relation="год")
G.add_edge("Zelda Breath of the Wild", "2017", relation="год")
G.add_edge("Monster Hunter World", "2018", relation="год")
G.add_edge("Resident Evil 2", "2019", relation="год")

# Серия
G.add_edge("Nier Automata", "Nier", relation="серия")
G.add_edge("Nier Automata", "Drakengard", relation="серия")
G.add_edge("Nier Automata", "Drag-on Dragoon", relation="серия")
G.add_edge("Final Fantasy VII", "Final Fantasy", relation="серия")
G.add_edge("Zelda Breath of the Wild", "The Legend of Zelda", relation="серия")
G.add_edge("Monster Hunter World", "Monster Hunter", relation="серия")
G.add_edge("Resident Evil 2", "Resident Evil", relation="серия")
G.add_edge("Resident Evil 2", "Biohazard", relation="серия")

# Движок
G.add_edge("Nier Automata", "Platinum Engine", relation="движок")
G.add_edge("Final Fantasy VII", "Square Engine", relation="движок")
G.add_edge("Zelda Breath of the Wild", "Havok", relation="движок")
G.add_edge("Monster Hunter World", "MT Framework", relation="движок")
G.add_edge("Resident Evil 2", "RE Engine", relation="движок")

# ===== ВИЗУАЛИЗАЦИЯ =====
plt.figure(figsize=(26, 20))
pos = {}

for i, game in enumerate(games):
    pos[game] = (i * 5 - 10, 12)

pos["Персонаж 2B"] = (-10, 9)
pos["Персонаж Клауд"] = (-5, 9)
pos["Персонаж Линк"] = (0, 9)
pos["Персонаж Леон"] = (10, 9)

pos["Сюжет"] = (-12, 6)
pos["Геймплей"] = (-10, 6)
pos["Саундтрек"] = (-8, 6)
pos["Система материи"] = (-5, 6)
pos["Открытый мир"] = (0, 6)
pos["Система готовки"] = (2, 6)
pos["Охота"] = (5, 6)
pos["Крафт брони"] = (8, 6)
pos["Зомби"] = (10, 6)
pos["Убежище"] = (12, 6)

pos["Action RPG"] = (-14, 12)
pos["JRPG"] = (-14, 10)
pos["Action-Adventure"] = (-14, 8)
pos["Survival Horror"] = (-14, 6)
pos["Экшен"] = (-16, 12)
pos["Японская RPG"] = (-16, 10)
pos["Приключенческий экшен"] = (-16, 8)
pos["Ужасы"] = (-16, 6)
pos["RPG"] = (-14, 4)
pos["Horror"] = (-14, 2)
pos["Adventure"] = (-14, 0)
pos["Action"] = (-14, -2)
pos["Жанр"] = (-14, -4)

pos["Platinum games"] = (14, 12)
pos["Square Enix"] = (14, 10)
pos["Nintendo"] = (14, 8)
pos["Capcom"] = (14, 6)
pos["Разработчик"] = (14, 4)

for i, p in enumerate(["PC", "PlayStation", "PlayStation 4", "PlayStation 5",
                         "Xbox One", "Xbox series X/S", "Nintendo Switch", "Wii u",
                         "Xbox", "Nintendo switch", "Платформа"]):
    pos[p] = (i * 2.5 - 14, -6)

others = ["2017", "1997", "2018", "2019",
          "Nier", "Drakengard", "Drag-on Dragoon",
          "Final Fantasy", "The Legend of Zelda", "Monster Hunter", "Resident Evil", "Biohazard",
          "Platinum Engine", "Square Engine", "Havok", "MT Framework", "RE Engine"]
for i, o in enumerate(others):
    pos[o] = (i * 1.8 - 14, -8)

color_map = []
for node in G.nodes():
    if node in games:
        color_map.append('#FF4444')  # красный - игры
    elif 'Персонаж' in node:
        color_map.append('#FF8C00')  # оранжевый - персонажи
    elif node in ['Сюжет', 'Геймплей', 'Саундтрек', 'Охота', 'Крафт брони', 'Зомби', 'Убежище', 'Открытый мир', 'Система готовки', 'Система материи']:
        color_map.append('#FFD700')  # золотой - части игр
    elif 'RPG' in node or 'Horror' in node or 'Adventure' in node or 'Action' in node or 'Жанр' in node or 'Экшен' in node or 'Ужасы' in node or 'Японская' in node or 'Приключенческий' in node:
        color_map.append('#4ECDC4')  # голубой - жанры
    elif node in ['Разработчик', 'Platinum games', 'Square Enix', 'Nintendo', 'Capcom']:
        color_map.append('#2ECC71')  # зелёный - компании
    elif node in ['Платформа', 'PC', 'PlayStation', 'PlayStation 4', 'PlayStation 5', 'Xbox', 'Xbox One', 'Xbox series X/S', 'Nintendo Switch', 'Wii u']:
        color_map.append('#3498DB')  # синий - платформы
    elif node in ['Nier', 'Drakengard', 'Drag-on Dragoon', 'Final Fantasy', 'The Legend of Zelda', 'Monster Hunter', 'Resident Evil', 'Biohazard']:
        color_map.append('#F1C40F')  # жёлтый - серии
    elif node in ['2017', '1997', '2018', '2019']:
        color_map.append('#9B59B6')  # фиолетовый - годы
    elif node in ['Platinum Engine', 'Square Engine', 'Havok', 'MT Framework', 'RE Engine']:
        color_map.append('#8B4513')  # коричневый - движки
    else:
        color_map.append('#AAAAAA')  # серый

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=color_map, edgecolors='black', linewidths=1)
nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=8, edge_color='#888888', alpha=0.5, width=1.5)
edge_labels = {(u, v): d['relation'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_color='#555555')

plt.title("Игры", fontsize=18, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig("semantic_graph.png", dpi=200, bbox_inches='tight')
plt.show()