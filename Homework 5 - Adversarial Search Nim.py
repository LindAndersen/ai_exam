import copy

minimax_cache = {}


# Check if a pile can be split into two unequal, non-empty piles
def valid_splits(pile):
    splits = []
    for i in range(1, pile):
        j = pile - i
        if i != j and i < j:  # ensure non-equal, and no reversed duplicates
            splits.append((i, j))
    return splits

# Generate all possible successor states from a given game state
def successors(state):
    next_states = set()
    for i, pile in enumerate(state):
        splits = valid_splits(pile)
        for a, b in splits:
            new_state = state[:i] + state[i+1:] + [a, b]
            new_state.sort()
            next_states.add(tuple(new_state))
    return list(next_states)

# Terminal state = no piles can be split
def is_terminal(state):
    for pile in state:
        splits = valid_splits(pile)
        if splits:
            return False  # At least one valid move exists
    return True  # No moves possible


# Utility value for terminal states
def utility(state, is_max_turn):
    if is_terminal(state):
        return -1 if is_max_turn else 1  # the player who cannot move loses
    return 0

# Minimax algorithm
def minimax(state, is_max_turn):
    key = (tuple(state), is_max_turn)
    if key in minimax_cache:
        return minimax_cache[key]

    if is_terminal(state):
        result = (utility(state, is_max_turn), None)
        minimax_cache[key] = result
        return result

    best_value = float('-inf') if is_max_turn else float('inf')
    best_move = None

    for succ in successors(state):
        val, _ = minimax(list(succ), not is_max_turn)
        if is_max_turn:
            if val > best_value:
                best_value = val
                best_move = succ
        else:
            if val < best_value:
                best_value = val
                best_move = succ

    result = (best_value, list(best_move))
    minimax_cache[key] = result
    return result


# Play game between MIN and MAX using minimax
def play_nim(starting_pile):
    state = [starting_pile]
    is_max_turn = False  # MIN starts

    print("Starting Nim game with pile:", state)
    turn = 0
    while not is_terminal(state):
        print(f"\nTurn {turn}: {'MAX' if is_max_turn else 'MIN'} to play")
        _, next_state = minimax(state, is_max_turn)
        print("Current state:", state)
        print("Next move:    ", next_state)
        state = next_state
        is_max_turn = not is_max_turn
        turn += 1

    print(f"\nGame over! Winner: {'MAX' if not is_max_turn else 'MIN'}")


if __name__ == '__main__':
    play_nim(20)
