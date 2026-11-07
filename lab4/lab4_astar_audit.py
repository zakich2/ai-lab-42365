# lab4_astar_audit.py - A*, UCS (h = 0) and heuristic audit on the campus graph
# Run: python lab4_astar_audit.py
# Heuristic values are ABSTRACT TIME ESTIMATES (same units as edge travel time), not measured distances.
import heapq

GRAPH = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
H = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

def astar(graph, h, start, goal, verbose=False):
    """A* following the supplied implementation. Expansion = successors examined;
    goal processing is logged but NOT counted; stale queue entries are ignored."""
    pq = [(h[start], 0, start, [start])]; best = {start: 0}
    processed, expansions = [], 0
    if verbose: print("  step | processed (g,h,f) | frontier after step [(node,g,h,f)]")
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if g != best[node]:
            continue                                         # stale entry
        processed.append(node)
        if node == goal:
            if verbose: print(f"  GOAL {node} (g={g},h={h[node]},f={f}) selected -> stop")
            return g, path, processed, expansions
        expansions += 1
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))
        if verbose:
            fr = sorted((e[0], e[1], e[2]) for e in pq)
            fr = [(n, gg, h[n], ff) for ff, gg, n in fr if gg == best[n]]
            print(f"  {expansions} | {node} (g={g},h={h[node]},f={f}) | {fr}")
    return None, None, processed, expansions

def path_cost(graph, path):                                   # independent sum of edge weights
    return sum(dict(graph[u])[v] for u, v in zip(path, path[1:]))

def true_remaining(graph, goal):
    """Exact remaining cost to goal for every node (Bellman-Ford style relaxation)."""
    inf = float("inf"); d = {n: inf for n in graph}; d[goal] = 0
    for _ in range(len(graph)):
        for u, edges in graph.items():
            for v, w in edges:
                d[u] = min(d[u], w + d[v])
    return d

def audit(graph, h, goal):
    true = true_remaining(graph, goal)
    print("Node | h(n) | true remaining | admissible (h <= true)")
    for n in graph:
        print(f"{n} | {h[n]} | {true[n]} | {h[n] <= true[n]}")
    print("Edge | h(u) | cost + h(v) | consistent (h(u) <= cost + h(v))")
    for u, edges in graph.items():
        for v, w in edges:
            print(f"{u}->{v} | {h[u]} | {w}+{h[v]}={w + h[v]} | {h[u] <= w + h[v]}")

def report(title, h):
    print(f"\n=== {title} ===")
    g, path, processed, exp = astar(GRAPH, h, "S", "G", verbose=True)
    print(f"  path={path} returned_cost={g} independent_sum={path_cost(GRAPH, path)}")
    print(f"  processed order={processed} expansions(excl. goal)={exp}")
    return g, path, processed, exp

if __name__ == "__main__":
    print("--- Heuristic audit (supplied h) ---")
    audit(GRAPH, H, "G")
    print("\nHand-check of first three expansions: S (0,5,5), A (1,4,5), C (3,2,5); then G (6,0,6) vs B (4,4,8)")
    a = report("A* with supplied heuristic", H)
    u = report("UCS control (all h = 0)", {n: 0 for n in H})
    h_bad = dict(H); h_bad["C"] = 10
    print(f"\nOverestimate experiment: h(C) changed from {H['C']} to {h_bad['C']} (true remaining cost of C = 3)")
    b = report("A* with h(C) = 10", h_bad)
    print("\nSUMMARY TABLE")
    print("run | path | cost | expansions")
    for name, r in [("A* supplied h", a), ("UCS h=0", u), ("A* h(C)=10", b)]:
        print(name, "->".join(r[1]), r[0], r[3], sep=" | ")
