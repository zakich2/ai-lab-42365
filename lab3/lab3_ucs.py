# lab3_ucs.py - Uniform-Cost Search on the weighted extension of the A-G graph
# Run: python lab3_ucs.py
# Original corridors + ONE ADDED corridor C -> G (documented extension, not the original trace graph).
# All weights are SYNTHETIC non-negative travel-cost units chosen for this lab.
import heapq
from collections import deque

W = {
    "A": [("B", 1), ("C", 5)],
    "B": [("D", 1), ("E", 1)],
    "C": [("F", 2), ("G", 7)],     # C -> G is the ADDED corridor
    "D": [],
    "E": [("G", 1)],
    "F": [],
    "G": [],
}

def ucs(graph, start, goal):
    counter = 0                                   # insertion order = tie-breaker
    pq = [(0, counter, start, [start])]; best = {start: 0}; order = []
    while pq:
        g, _, node, path = heapq.heappop(pq)
        if g > best[node]: continue               # stale entry
        order.append((node, g))
        if node == goal: return g, path, order
        for nxt, w in graph[node]:
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng; counter += 1
                heapq.heappush(pq, (ng, counter, nxt, path + [nxt]))
    return None, None, order

def bfs_weighted_topology(graph, start, goal):
    """BFS ignores weights: it minimises number of edges."""
    q = deque([(start, [start])]); seen = {start}; order = []
    while q:
        node, path = q.popleft(); order.append(node)
        if node == goal: return path, order
        for nxt, _ in graph[node]:
            if nxt not in seen:
                seen.add(nxt); q.append((nxt, path + [nxt]))
    return None, order

def path_cost(graph, path):
    """Independent sum of edge weights along a path."""
    total = 0
    for u, v in zip(path, path[1:]):
        total += dict(graph[u])[v]
    return total

if __name__ == "__main__":
    print("Weighted graph (edge: weight):")
    for u, edges in W.items():
        for v, w in edges:
            print(f"  {u} -> {v}: {w}" + ("   <- added corridor" if (u, v) == ("C", "G") else ""))
    cost, path, order = ucs(W, "A", "G")
    print("\nUCS  path:", path, "| returned cost:", cost,
          "| independent sum:", path_cost(W, path), "| edges:", len(path) - 1)
    print("UCS  processing order (node, g):", order)
    bpath, border = bfs_weighted_topology(W, "A", "G")
    print("\nBFS  path:", bpath, "| independent cost:", path_cost(W, bpath), "| edges:", len(bpath) - 1)
    print("BFS  processing order:", border)
    print("\nConclusion: BFS has fewer edges (%d vs %d) but higher cost (%d vs %d)."
          % (len(bpath) - 1, len(path) - 1, path_cost(W, bpath), path_cost(W, path)))
