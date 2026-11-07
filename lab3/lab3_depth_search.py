# lab3_depth_search.py - DLS (FOUND / CUTOFF / FAILURE) and IDDFS, original A-G graph
# Run: python lab3_depth_search.py
graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}

def dls(g, node, goal, limit, path=None, stats=None):
    """Depth-limited search. Root has depth 0. Cycle check is PATH-LOCAL."""
    path = path or [node]
    if stats is not None: stats["visited"] += 1
    if node == goal:
        return "FOUND", path
    succ = [n for n in g.get(node, []) if n not in path]     # path-local cycle check
    if limit == 0:
        # CUTOFF only if a deeper continuation exists; otherwise this branch is exhausted
        return ("CUTOFF", None) if succ else ("FAILURE", None)
    cutoff = False
    for n in succ:
        status, result = dls(g, n, goal, limit - 1, path + [n], stats)
        if status == "FOUND": return status, result
        if status == "CUTOFF": cutoff = True
    return ("CUTOFF", None) if cutoff else ("FAILURE", None)

def iddfs(g, start, goal, max_depth):
    """Repeat DLS with limits 0..max_depth, fresh search each time (no global visited set)."""
    attempted, total_visits = [], 0
    for limit in range(max_depth + 1):
        stats = {"visited": 0}
        status, result = dls(g, start, goal, limit, stats=stats)
        attempted.append(limit); total_visits += stats["visited"]
        if status == "FOUND":   return status, result, attempted, total_visits
        if status == "FAILURE": return status, None, attempted, total_visits  # search space exhausted
    return "CUTOFF", None, attempted, total_visits

if __name__ == "__main__":
    print("=== DLS on original graph, start A, goal G ===")
    for limit in [1, 2, 3, 4]:
        stats = {"visited": 0}
        status, path = dls(graph, "A", "G", limit, stats=stats)
        print(f"limit={limit} status={status} path={path} nodes_visited={stats['visited']}")

    print("\n=== IDDFS with maximum depths 1..4 ===")
    for md in [1, 2, 3, 4]:
        status, path, attempted, visits = iddfs(graph, "A", "G", md)
        print(f"max_depth={md} status={status} path={path} limits_attempted={attempted} total_node_visits={visits}")

    print("\n=== Edge cases ===")
    print("start == goal      :", dls(graph, "A", "A", 0))
    g2 = dict(graph); g2["Z"] = []
    print("unreachable goal Z :", iddfs(g2, "A", "Z", 6)[:3])
    cyc = {"A": ["B"], "B": ["A", "C"], "C": []}
    print("cycle graph, goal C:", iddfs(cyc, "A", "C", 5)[:3])
    print("cycle graph, goal X:", iddfs(dict(cyc, X=[]), "A", "X", 5)[:3])
