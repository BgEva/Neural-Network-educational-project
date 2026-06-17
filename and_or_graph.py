import matplotlib.pyplot as plt
import networkx as nx


"""
И/ИЛИ-граф для подбора видеоигры
Входы: 12 признаков (e1-e12)
Выходы: 10 игр (r1-r10)
"""

# Коэффициенты влияния [k1, k2, ...]
coefficients = {
    # r1 = Nier Automata
    "r1": {
        "and": [("e6", 0.9), ("e10", 0.8), ("e12", 0.7)],
        "or": [("e9", 0.6)],
        "k": 0.85
    },
    # r2 = Final Fantasy VII
    "r2": {
        "and": [("e9", 0.95), ("e2", 0.85), ("e12", 0.9)],
        "or": [("e5", 0.7)],
        "k": 0.85
    },
    # r3 = Zelda BotW
    "r3": {
        "and": [("e1", 0.95), ("e5", 0.9), ("e12", 0.9)],
        "or": [("e11", 0.7), ("e10", 0.6)],
        "k": 0.9
    },
    # r4 = Monster Hunter World
    "r4": {
        "and": [("e2", 0.9), ("e11", 0.9)],
        "or": [("e10", 0.7), ("e7", 0.6), ("e3", 0.8)],
        "k": 0.85
    },
    # r5 = Resident Evil 2
    "r5": {
        "and": [("e8", 0.95), ("e4", 0.85), ("e12", 0.7)],
        "or": [],
        "k": 0.9
    },
    # r6 = Dark Souls
    "r6": {
        "and": [("e7", 0.95), ("e12", 0.9)],
        "or": [("e5", 0.85), ("e2", 0.9), ("e10", 0.8)],
        "k": 0.95
    },
    # r7 = Metal Gear Rising
    "r7": {
        "and": [("e10", 0.95), ("e7", 0.75)],
        "or": [("e6", 0.7)],
        "k": 0.85
    },
    # r8 = Persona 5
    "r8": {
        "and": [("e9", 0.95), ("e12", 0.9), ("e2", 0.85)],
        "or": [("e5", 0.3)],
        "k": 0.8
    },
    # r9 = Devil May Cry 5
    "r9": {
        "and": [("e10", 0.95), ("e7", 0.8)],
        "or": [("e5", 0.5)],
        "k": 0.9
    },
    # r10 = Silent Hill 2
    "r10": {
        "and": [("e8", 0.95), ("e12", 0.8)],
        "or": [("e7", 0.5)],
        "k": 0.9
    },
}

# Названия
input_names = {
    "e1": "Открытый мир", "e2": "Прокачка/RPG", "e3": "Мультиплеер/кооп",
    "e4": "Реалистичная графика", "e5": "Фэнтези", "e6": "Сайфай",
    "e7": "Хардкор/сложность", "e8": "Хоррор", "e9": "JRPG/аниме",
    "e10": "Экшен/Hack and Slash", "e11": "Крафт", "e12": "Одиночная игра"
}

output_names = {
    "r1": "Nier Automata", "r2": "Final Fantasy VII", "r3": "Zelda BotW",
    "r4": "Monster Hunter World", "r5": "Resident Evil 2", "r6": "Dark Souls",
    "r7": "Metal Gear Rising", "r8": "Persona 5", "r9": "Devil May Cry 5",
    "r10": "Silent Hill 2"
}

def calc_and(inputs, pairs, k):
    """Связка И: p = k * min(ki * p(ei))"""
    values = []
    for ei, ki in pairs:
        if ei in inputs:
            values.append(ki * inputs[ei])
    if not values:
        return 0
    return k * min(values)

def calc_or(inputs, pairs):
    """Связка ИЛИ: p = k1*p1 + k2*p2 - k1*p1*k2*p2"""
    if not pairs:
        return 0
    result = 0
    for ei, ki in pairs:
        if ei in inputs:
            pi = ki * inputs[ei]
            result = result + pi - result * pi
    return result

def calc_output(inputs, rule):
    """Расчёт вероятности выходного события"""
    p_and = calc_and(inputs, rule["and"], rule["k"])
    p_or = calc_or(inputs, rule["or"])
    if rule["or"]:
        # Бонус от ИЛИ не больше 30% от остатка
        return p_and + 0.3 * p_or * (1 - p_and)
    return p_and

def run_scenario(inputs, name):
    """Запуск сценария и вывод результатов"""
    print(f"\n{'='*50}")
    print(f"Сценарий: {name}")
    print(f"{'='*50}")
    print("Входные вероятности:")
    for ei, val in inputs.items():
        print(f"  {ei} ({input_names[ei]}): {val}")
    
    results = {}
    for ri, rule in coefficients.items():
        results[ri] = calc_output(inputs, rule)
    
    print("\nРезультаты (вероятности):")
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for ri, prob in sorted_results:
        bar = "█" * int(prob * 20)
        print(f"  {ri} {output_names[ri]:25s}: {prob:.4f} {bar}")
    
    print(f"\n>>> Рекомендация: {output_names[sorted_results[0][0]]}")
    return results


def visualize_graph():
    G = nx.DiGraph()
    
    for ei, name in input_names.items():
        G.add_node(ei, label=name, color='#AED6F1')
    for ri, name in output_names.items():
        G.add_node(ri, label=name, color='#A9DFBF')
    
    for ri, rule in coefficients.items():
        for ei, ki in rule["and"]:
            G.add_edge(ei, ri, style='solid')
        for ei, ki in rule["or"]:
            G.add_edge(ei, ri, style='dashed')
    
    plt.figure(figsize=(20, 14))
    
    # Входы слева, выходы справа
    pos = {}
    for i, ei in enumerate(input_names):
        pos[ei] = (0, i * 1.5 - 8)
    for i, ri in enumerate(output_names):
        pos[ri] = (6, i * 1.5 - 7)
    
    node_colors = ['#AED6F1' if n.startswith('e') else '#A9DFBF' for n in G.nodes()]
    labels = {n: G.nodes[n]['label'] for n in G.nodes()}
    
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, edgecolors='black', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    solid = [(u, v) for u, v, d in G.edges(data=True) if d['style'] == 'solid']
    dashed = [(u, v) for u, v, d in G.edges(data=True) if d['style'] == 'dashed']
    
    nx.draw_networkx_edges(G, pos, edgelist=solid, edge_color='#2980B9', arrows=True, arrowsize=15, width=2)
    nx.draw_networkx_edges(G, pos, edgelist=dashed, edge_color='#E74C3C', style='dashed', arrows=True, arrowsize=15, width=2)
    
    plt.title("И/ИЛИ-граф подбора видеоигры\nГолубые = Входы | Зелёные = Выходы | Синие = И | Красные пунктир = ИЛИ", fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("and_or_graph.png", dpi=150, bbox_inches='tight')
    print("Граф сохранён в and_or_graph.png")
    plt.show()


# ===== СЦЕНАРИИ =====
if __name__ == "__main__":
    # Сценарий 1: любитель фэнтези и открытого мира
    scenario1 = {
        "e1": 0.95, "e2": 0.5, "e3": 0.1, "e4": 0.3,
        "e5": 0.9, "e6": 0.2, "e7": 0.3, "e8": 0.1,
        "e9": 0.4, "e10": 0.6, "e11": 0.3, "e12": 0.9
    }
    
    # Сценарий 2: хардкорный геймер
    scenario2 = {
        "e1": 0.4, "e2": 0.9, "e3": 0.2, "e4": 0.5,
        "e5": 0.7, "e6": 0.3, "e7": 0.95, "e8": 0.6,
        "e9": 0.5, "e10": 0.9, "e11": 0.2, "e12": 0.95
    }
    
    # Сценарий 3: любитель хорроров
    scenario3 = {
        "e1": 0.2, "e2": 0.3, "e3": 0.1, "e4": 0.9,
        "e5": 0.2, "e6": 0.1, "e7": 0.3, "e8": 0.95,
        "e9": 0.1, "e10": 0.4, "e11": 0.1, "e12": 0.9
    }
    
    run_scenario(scenario1, "Любитель фэнтези и открытого мира")
    run_scenario(scenario2, "Хардкорный геймер")
    run_scenario(scenario3, "Любитель хорроров")
    visualize_graph()