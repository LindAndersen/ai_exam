import numpy as np

def main():
    np.set_printoptions(suppress=True)

    states = np.array(["hot", "cold"])
    obs_sequence = [2, 1, 3, 1]  # observations: 2 1 3 1

    # Transition matrix: rows = from, cols = to (hot=0, cold=1)
    transitions = np.array([
        [0.3, 0.5],  # from hot
        [0.2, 0.6],  # from cold
    ])

    # Transition probabilities to END state
    end_probs = np.array([0.2, 0.2])  # from hot, cold

    # Emission matrix: rows = state, cols = observation (1-indexed)
    emissions = np.array([
        [0.2, 0.5, 0.3],  # hot
        [0.4, 0.3, 0.3],  # cold
    ])

    # Initial probabilities from start state
    start_probs = np.array([0.6, 0.4])  # Start → HOT, Start → COLD

    print("Observations:", ' '.join(map(str, obs_sequence)))

    prob = compute_forward(start_probs, transitions, emissions, obs_sequence, end_probs)
    print("Observation Sequence Probability (Forward):", prob)

    path = compute_viterbi_log(start_probs, transitions, emissions, obs_sequence, end_probs, states)
    print("Most Likely State Sequence (Viterbi):", ' '.join(path))


def compute_forward(start_probs, transitions, emissions, observations, end_probs):
    n_states = transitions.shape[0]
    T = len(observations)
    forward = np.zeros((n_states, T))

    # Initialization
    for s in range(n_states):
        forward[s][0] = start_probs[s] * emissions[s][observations[0] - 1]

    # Recursion
    for t in range(1, T):
        for s in range(n_states):
            forward[s][t] = sum(
                forward[sp][t - 1] * transitions[sp][s]
                for sp in range(n_states)
            ) * emissions[s][observations[t] - 1]

    # Termination (account for transition to END)
    prob = sum(forward[s][T - 1] * end_probs[s] for s in range(n_states))
    return prob


def compute_viterbi_log(start_probs, transitions, emissions, observations, end_probs, state_names):
    n_states = transitions.shape[0]
    T = len(observations)

    log = np.log
    viterbi = np.full((n_states, T), -np.inf)
    backpointer = np.zeros((n_states, T), dtype=int)

    # Convert to log-space
    log_start = log(start_probs + 1e-12)
    log_trans = log(transitions + 1e-12)
    log_emit = log(emissions + 1e-12)
    log_end = log(end_probs + 1e-12)

    # Initialization
    for s in range(n_states):
        viterbi[s][0] = log_start[s] + log_emit[s][observations[0] - 1]

    # Recursion
    for t in range(1, T):
        for s in range(n_states):
            log_probs = [viterbi[sp][t - 1] + log_trans[sp][s] for sp in range(n_states)]
            best_prev = np.argmax(log_probs)
            viterbi[s][t] = log_probs[best_prev] + log_emit[s][observations[t] - 1]
            backpointer[s][t] = best_prev

    # Termination: Add transition to END state
    final_probs = [viterbi[s][T - 1] + log_end[s] for s in range(n_states)]
    last_state = np.argmax(final_probs)

    # Backtrace
    path_indices = [last_state]
    for t in range(T - 1, 0, -1):
        last_state = backpointer[last_state][t]
        path_indices.insert(0, last_state)

    return [state_names[i] for i in path_indices]


if __name__ == '__main__':
    main()
