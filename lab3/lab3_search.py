# lab3_search.py - BFS and DFS on the original A-G graph (supplied code + traced versions)
# Run: python lab3_search.py
from collections import deque

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}

# ---------- supplied implementations (unchanged) ----------
def bfs(start, goal):
    q = deque([(start, [start])]); seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal: return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))

def dfs(start, goal):
    stack = [(start, [start])]; seen = set()
    while stack:
        node, path = stack.pop()
        if node == goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n, path + [n]))

# ---------- traced versions: print queue/stack after every step ----------
def bfs_trace(start, goal):
    q = deque([(start, [start])]); seen = {start}; order = []
    print("BFS trace (frontier = queue, front on the left)")
    print("step | processed | path | frontier after step")
    step = 0
    while q:
        node, path = q.popleft(); step += 1; order.append(node)
        if node == goal:
            print(step, node, "->".join(path), [n for n, _ in q], "GOAL", sep=" | ")
            return path, order
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
        print(step, node, "->".join(path), [n for n, _ in q], sep=" | ")

def dfs_trace(start, goal):
    stack = [(start, [start])]; seen = set(); order = []
    print("DFS trace (frontier = stack, TOP is the right-most item)")
    print("step | processed | path | frontier after step")
    step = 0
    while stack:
        node, path = stack.pop()
        if node in seen: continue
        step += 1; seen.add(node); order.append(node)
        if node == goal:
            print(step, node, "->".join(path), [n for n, _ in stack], "GOAL", sep=" | ")
            return path, order
        for n in reversed(graph[node]): stack.append((n, path + [n]))
        print(step, node, "->".join(path), [n for n, _ in stack], sep=" | ")

if __name__ == "__main__":
    print("Supplied code  BFS:", bfs("A", "G"))
    print("Supplied code  DFS:", dfs("A", "G"))
    print()
    p, o = bfs_trace("A", "G"); print("BFS final path:", p); print("BFS visit order:", o); print()
    p, o = dfs_trace("A", "G"); print("DFS final path:", p); print("DFS visit order:", o)
