import torch
import torch.nn as nn
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# 12 признаков. Ответ: 1 = да, 0 = нет
# [0]  Открытый мир?
# [1]  Прокачка (RPG)?
# [2]  Мультиплеер?
# [3]  Реалистичная графика?
# [4]  Фэнтези?
# [5]  Научная фантастика?
# [6]  Герой — человек?
# [7]  Бой в реальном времени?
# [8]  Хоррор?
# [9]  JRPG?
# [10] Крафт/сбор ресурсов?
# [11] Одиночная игра?

nier_automata = [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1]
final_fantasy_7 = [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1]
zelda_botw = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1]
monster_hunter_world = [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1]
resident_evil_2 = [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1]

games_data = [
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],  # Nier Automata
    [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1],  # Final Fantasy VII
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],  # Zelda BotW
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1],  # Monster Hunter World
   [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1],  # Resident Evil 2
]

games_name = [
 
    "Nier Automata",
    "Final Fantasy VII",
    "Zelda Breath of the Wild",
    "Monster Hunter World",
    "Resident Evil 2",

]

#X - признаки игр
X = torch.tensor(games_data, dtype=torch.float32)

#y - метки классов: 0 - Nier | 1 - FF7 | 2 - Zelda | 3 - MHW | 4 - RE2 |
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

epochs = 500

for epoch in range(epochs):
     outputs = model(X)
     loss = criterion(outputs, y)
     optimizer.zero_grad()
     loss.backward()
     optimizer.step()
     if (epoch + 1) % 100 == 0:
          print(f"Эпоха {epoch+1}/{epochs}, ошибка: {loss.item():.4f}")


G = nx.DiGraph()

games = ["Nier Automata", "Final Fantasy VII", "Zelda Breath of the Wild", "Monster Hunter World", "Resident Evil 2"]
G.add_nodes_from(games)

G.add_edge("Nier Automata", "Action RPG", relation="жанр")
G.add_edge("Final Fantasy VII", "JRPG", relation="жанр")
G.add_edge("Zelda Breath of the Wild", "Action-Adventure", relation="жанр")
G.add_edge("Monster Hunter World", "Action RPG", relation="жанр")
G.add_edge("Resident Evil 2", "Survival Horror", relation="жанр")

G.add_edge("Nier Automata", "Platinum games", relation="разработчик")
G.add_edge("Final Fantasy VII", "Square Enix", relation="разработчик")
G.add_edge("Zelda Breath of the Wild", "Nintendo", relation="разработчик")
G.add_edge("Monster Hunter World", "Capcom", relation="разработчик")
G.add_edge("Resident Evil 2", "Capcom", relation="разработчик")

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
G.add_edge("Resident Evil 2", "Nintendo switch", relation="платформа")
G.add_edge("Resident Evil 2", "PC", relation="платформа")

G.add_edge("Nier Automata", "2017", relation="год")
G.add_edge("Final Fantasy VII", "1997", relation="год")
G.add_edge("Zelda Breath of the Wild", "2017", relation="год")
G.add_edge("Monster Hunter World", "2018", relation="год")
G.add_edge("Resident Evil 2", "2019", relation="год")

G.add_edge("Nier Automata", "Nier", relation="серия")
G.add_edge("Nier Automata", "Drakengard", relation="серия")
G.add_edge("Nier Automata", "Drag-on Dragoon", relation="серия")

G.add_edge("Final Fantasy VII", "Final Fantasy", relation="серия")
G.add_edge("Zelda Breath of the Wild", "The Legend of Zelda", relation="серия")
G.add_edge("Monster Hunter World", "Monster Hunter", relation="серия")

G.add_edge("Resident Evil 2", "Resident Evil", relation="серия")
G.add_edge("Resident Evil 2", "Biohazard", relation="серия")

G.add_edge("Nier Automata", "Square Enix", relation="издатель")
G.add_edge("Final Fantasy VII", "Square Enix", relation="издатель")
G.add_edge("Zelda Breath of the Wild", "Nintendo", relation="издатель")
G.add_edge("Monster Hunter World", "Capcom", relation="издатель")
G.add_edge("Resident Evil 2", "Capcom", relation="издатель")

G.add_edge("Nier Automata", "Platinum Engine", relation="движок")
G.add_edge("Final Fantasy VII", "Square Engine", relation="движок")
G.add_edge("Zelda Breath of the Wild", "Havok", relation="движок")
G.add_edge("Monster Hunter World", "MT Framework", relation="движок")
G.add_edge("Resident Evil 2", "RE Engine", relation="движок")


plt.figure(figsize=(14, 12))
pos = nx.spring_layout(G, k=3, seed=42)
import math

# Игры в центр
for i, game in enumerate(games):
    angle = 2 * math.pi * i / len(games)
    pos[game] = (1.5 * math.cos(angle), 1.5 * math.sin(angle))

# Остальные узлы по кругу
other_nodes = [n for n in G.nodes() if n not in games]
for i, node in enumerate(other_nodes):
    angle = 2 * math.pi * i / len(other_nodes)
    pos[node] = (5 * math.cos(angle), 5 * math.sin(angle))

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=7)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=10)
edge_labels = {(u, v): d['relation'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)
plt.title("Семантическая сеть игр")
plt.axis('off')
plt.show()


