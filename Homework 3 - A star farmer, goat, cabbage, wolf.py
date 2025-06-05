import sys

class Node:
    def __init__(self, state, heuristic=6, weight=0, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.WEIGHT = weight
        self.HEURISTIC = heuristic
        self.fn = heuristic + weight

    def path(self):
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:
            current_node = current_node.PARENT_NODE
            path.append(current_node)
        return list(reversed(path))

    def display(self):
        print(self)

    def __repr__(self):
        return f"State: {self.STATE} - f(n): {self.fn} - Depth: {self.DEPTH}"


def TREE_SEARCH(algo: str, alpha: int):
    fringe = []
    initial_node = Node(INITIAL_STATE, heuristic=HEURISTICS[INITIAL_STATE] * alpha)
    fringe = INSERT(initial_node, fringe)
    while fringe:
        if algo == 'bfs':
            node = REMOVE_FIRST(fringe)
        elif algo == 'a*':
            node = REMOVE_OPTIMAL(fringe)
        elif algo == 'gbf':
            node = REMOVE_CHEAP(fringe)
        else:
            print(f"Unknown algorithm: {algo}")
            return []

        if node.STATE == GOAL_STATE:
            return node.path()

        children = EXPAND(node, alpha)
        fringe = INSERT_ALL(children, fringe)
        print("Fringe:", fringe)


def EXPAND(node, alpha):
    successors = []
    children = successor_fn(node.STATE)
    for child_state, weight in children:
        heuristic = HEURISTICS[child_state] * alpha
        total_weight = weight + node.WEIGHT
        child_node = Node(
            state=child_state,
            heuristic=heuristic,
            weight=total_weight,
            parent=node,
            depth=node.DEPTH + 1
        )
        successors = INSERT(child_node, successors)
    return successors


def INSERT(node, queue):
    queue.append(node)
    return queue


def INSERT_ALL(nodes, queue):
    queue.extend(nodes)
    return queue


def REMOVE_FIRST(queue):
    return queue.pop(0)


def REMOVE_CHEAP(queue):
    cheapest = min(queue, key=lambda n: n.HEURISTIC)
    queue.remove(cheapest)
    return cheapest


def REMOVE_OPTIMAL(queue):
    best = min(queue, key=lambda n: n.fn)
    queue.remove(best)
    return best


def successor_fn(state):
    return STATE_SPACE[state]


def run(config: str, alpha: int):
    print(f"\nRunning tree search with algorithm = {config}, alpha = {alpha}")
    path = TREE_SEARCH(config, alpha)
    print('\nSolution path:')
    for node in path:
        node.display()


def print_help():
    print("=== SEARCH AGENT ===")
    print("Choose search algorithm and heuristic weight.")
    print("\nOptions:")
    print("  algorithm : 'bfs', 'a*', or 'gbf'")
    print("  alpha     : integer weight for heuristic (default is 1)")
    print("\nExamples:")
    print("  Algorithm: a*")
    print("  Alpha: 1\n")


# ------------------ CONFIG ------------------
INITIAL_STATE = 'A'
GOAL_STATE = 'L'
STATE_SPACE = {
    'A': [('B', 1), ('C', 2), ('D', 4)],
    'B': [('F', 5), ('E', 4)],
    'C': [('E', 1)],
    'D': [('H', 1), ('I', 4), ('J', 2)],
    'E': [('G', 2), ('H', 3)],
    'F': [('G', 1)],
    'G': [('K', 6)],
    'H': [('K', 6), ('L', 5)],
    'I': [('L', 3)],
    'J': [],
    'K': [],
    'L': []
}
HEURISTICS = {
    'A': 6, 'B': 5, 'C': 5, 'D': 2, 'E': 4,
    'F': 5, 'G': 4, 'H': 1, 'I': 2, 'J': 1,
    'K': 0, 'L': 0
}

# --------------- ENTRY POINT ----------------
if __name__ == '__main__':
    print_help()

    # Ask user input if not provided via arguments
    config = input("Enter algorithm (bfs / a* / gbf): ").strip().lower()
    if config not in ['bfs', 'a*', 'gbf']:
        print("Invalid algorithm. Exiting.")
        sys.exit(1)

    alpha_input = input("Enter alpha (integer): ").strip()
    try:
        alpha = int(alpha_input)
    except ValueError:
        print("Invalid alpha. Must be an integer.")
        sys.exit(1)

    run(config, alpha)
