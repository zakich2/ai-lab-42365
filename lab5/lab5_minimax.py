# lab5_minimax.py - Minimax vs Alpha-Beta with leaf counters and branch re-ordering
# Run: python lab5_minimax.py
import math

# ---------------- Minimax (supplied logic + leaf counter) ----------------
def minimax(depth, idx, max_turn, scores, target, counter):
    if depth == target:
        counter[0] += 1                      # leaf evaluated
        return scores[idx]
    vals = [minimax(depth + 1, idx * 2 + i, not max_turn, scores, target, counter) for i in range(2)]
    return max(vals) if max_turn else min(vals)

# ---------------- Alpha-Beta (supplied logic + leaf counter) ----------------
def alphabeta(depth, idx, max_turn, scores, target, alpha, beta, counter):
    if depth == target:
        counter[0] += 1                      # leaf evaluated
        return scores[idx]
    if max_turn:
        value = float("-inf")
        for i in range(2):
            value = max(value, alphabeta(depth + 1, idx * 2 + i, False, scores, target, alpha, beta, counter))
            alpha = max(alpha, value)
            if alpha >= beta:
                break                        # prune remaining child
        return value
    value = float("inf")
    for i in range(2):
        value = min(value, alphabeta(depth + 1, idx * 2 + i, True, scores, target, alpha, beta, counter))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value

def pad(scores):
    d = math.ceil(math.log2(len(scores)))
    return scores + [0] * (2 ** d - len(scores)), d

def run_both(scores):
    scores, d = pad(list(scores))
    c1, c2 = [0], [0]
    v1 = minimax(0, 0, True, scores, d, c1)
    v2 = alphabeta(0, 0, True, scores, d, float("-inf"), float("inf"), c2)
    return v1, c1[0], v2, c2[0]

def root_action(scores):
    """Which root move (0 = left, 1 = right) does MAX choose?"""
    scores, d = pad(list(scores))
    vals = [minimax(1, i, False, scores, d, [0]) for i in range(2)]
    return ("LEFT" if vals[0] >= vals[1] else "RIGHT"), vals

# ---------------- branch re-ordering (swap children at internal nodes) ----------------
def nest(leaves):
    if len(leaves) == 1: return leaves[0]
    m = len(leaves) // 2
    return (nest(leaves[:m]), nest(leaves[m:]))

def flat(t):
    return [t] if not isinstance(t, tuple) else flat(t[0]) + flat(t[1])

def orderings(t):
    if not isinstance(t, tuple): return [t]
    out = []
    for a in orderings(t[0]):
        for b in orderings(t[1]):
            out.append((a, b)); out.append((b, a))
    return out

if __name__ == "__main__":
    print("=== Task 1: supplied Minimax tree ===")
    base = [3, 5, 2, 9, 0, 7]
    padded, d = pad(list(base))
    print("scores (padded):", padded, "| tree depth:", d)
    print("MAX-level pairs : max(3,5)=5, max(2,9)=9, max(0,7)=7, max(0,0)=0")
    print("MIN-level pairs : min(5,9)=5, min(7,0)=0")
    print("Root (MAX)      : max(5,0)=5")
    print("Root action:", root_action(base))

    print("\n=== Task 2: both algorithms with leaf counters ===")
    for name, sc in [("minimax tree [3,5,2,9,0,7]", base),
                     ("alpha-beta tree [3,5,2,9,3,5,2,9]", [3, 5, 2, 9, 3, 5, 2, 9])]:
        v1, n1, v2, n2 = run_both(sc)
        print(f"{name}: minimax value={v1} leaves={n1} | alpha-beta value={v2} leaves={n2} | same value: {v1 == v2}")

    print("\n=== Task 3: re-ordering branches (same tree, children swapped) ===")
    manual = {
        "original order": [3, 5, 2, 9, 0, 7, 0, 0],
        "root children swapped": [0, 7, 0, 0, 3, 5, 2, 9],
        "leaf pairs reversed": [5, 3, 9, 2, 7, 0, 0, 0],
        "fully reversed": [0, 0, 7, 0, 9, 2, 5, 3],
    }
    print("ordering | leaves (as list) | root value | minimax leaves | alpha-beta leaves")
    for name, sc in manual.items():
        v1, n1, v2, n2 = run_both(sc)
        assert v1 == v2
        print(name, sc, v2, n1, n2, sep=" | ")

    print("\nAll 2^7 = 128 sibling orderings of the tree [3,5,2,9,0,7,0,0]:")
    results = []
    for t in orderings(nest([3, 5, 2, 9, 0, 7, 0, 0])):
        v1, n1, v2, n2 = run_both(flat(t))
        assert v1 == v2 == 5
        results.append(n2)
    print("root value in every ordering: 5")
    print("alpha-beta leaves: min =", min(results), "max =", max(results), "(minimax always evaluates 8)")
