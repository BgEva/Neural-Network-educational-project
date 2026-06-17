from Neuro_mamykin_1 import G
import networkx as nx

def search_by_relation(graph, node, relation_type):
    results = []
    for u, v, data in graph.edges(data=True):
        if data.get('relation') == relation_type:
            if u == node:
                results.append(v)
            elif v == node:
                results.append(u)
    return results

def get_isa_parents(graph, node):
    parents = []
    for u, v, data in graph.edges(data=True):
        if data.get('relation') == 'ISA' and u == node:
            parents.append(v)
    return parents

def get_isa_children(graph, node):
    children = []
    for u, v, data in graph.edges(data=True):
        if data.get('relation') == 'ISA' and v == node:
            children.append(u)
    return children

def find_path(graph, start, end):
    try:
        path = nx.shortest_path(graph, start, end)
        return path
    except nx.NetworkXNoPath:
        return None

def explain_path(graph, start, end):
    path = find_path(graph, start, end)
    if not path:
        return "Путь не найден"
    steps = []
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        data = graph.get_edge_data(u, v)
        if data:
            rel = list(data.values())[0] if isinstance(list(data.values())[0], str) else list(data.values())[0].get('relation', 'связан с')
        else:
            data = graph.get_edge_data(v, u)
            if data:
                rel = list(data.values())[0] if isinstance(list(data.values())[0], str) else list(data.values())[0].get('relation', 'связан с')
            else:
                rel = 'связан с'
        steps.append(f"{u} --[{rel}]--> {v}")
    return "\n".join(steps)


def classify_by_properties(graph, properties):
    results = []
    for node in graph.nodes():
        node_props = set()
        for u, v, data in graph.edges(data=True):
            if v == node:
                rel = list(data.values())[0] if isinstance(list(data.values())[0], str) else data.get('relation', '')
                node_props.add(rel)
        if properties.issubset(node_props) or properties & node_props:
            results.append(node)
    return results

# Меню
while True:
    print("\n=== СЕМАНТИЧЕСКИЙ ПОИСК ===")
    print("1. Поиск по отношению")
    print("2. Предки по ISA")
    print("3. Потомки по ISA")
    print("4. Путь между узлами")
    print("5. Объяснение пути")
    print("6. Классификация по свойствам")
    print("7. Выход")
    choice = input("Выбор: ")

    if choice == "1":
        node = input("Узел: ")
        rel = input("Тип связи (ISA/AKO/Part-Of/жанр/...): ")
        results = search_by_relation(G, node, rel)
        print(f"Результаты: {results}")

    elif choice == "2":
        node = input("Узел: ")
        parents = get_isa_parents(G, node)
        print(f"Предки {node}: {parents}")

    elif choice == "3":
        node = input("Узел: ")
        children = get_isa_children(G, node)
        print(f"Потомки {node}: {children}")

    elif choice == "4":
        start = input("От: ")
        end = input("До: ")
        path = find_path(G, start, end)
        if path:
            print(" → ".join(path))
        else:
            print("Путь не найден")

    elif choice == "5":
        start = input("От: ")
        end = input("До: ")
        print(explain_path(G, start, end))

    elif choice == "6":
        props = input("Свойства через запятую: ").split(",")
        props = set(p.strip() for p in props)
        results = classify_by_properties(G, props)
        print(f"Подходящие объекты: {results}")
        

    elif choice == "7":
        break