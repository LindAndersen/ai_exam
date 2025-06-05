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

    # Emission matrix: rows = state, cols = observation (1-indexed)
    emissions = np.array([
        [0.2, 0.5, 0.3],  # hot: P(1)=0.2, P(2)=0.4, P(3)=0.4
        [0.4, 0.3, 0.3],  # cold: P(1)=0.5, P(2)=0.4, P(3)=0.1
    ])

    # Initial probabilities from start state
    start_probs = np.array([0.6, 0.4])  # P(start → hot), P(start → cold)

    print("Observations:", ' '.join(map(str, obs_sequence)))
    prob = compute_forward(start_probs, transitions, emissions, obs_sequence)
    print("Observation Sequence Probability (Forward):", prob)

    path = compute_viterbi_log(start_probs, transitions, emissions, obs_sequence, states)
    print("Most Likely State Sequence (Viterbi):", ' '.join(path))


def compute_forward(start_probs, transitions, emissions, observations):
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

    return np.sum(forward[:, -1])


def compute_viterbi_log(start_probs, transitions, emissions, observations, state_names):
    n_states = transitions.shape[0]
    T = len(observations)

    log = np.log
    viterbi = np.full((n_states, T), -np.inf)
    backpointer = np.zeros((n_states, T), dtype=int)

    # Convert to log-space
    log_start = log(start_probs + 1e-12)
    log_trans = log(transitions + 1e-12)
    log_emit = log(emissions + 1e-12)

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

    # Backtrace
    last_state = np.argmax(viterbi[:, -1])
    path_indices = [last_state]
    for t in range(T - 1, 0, -1):
        last_state = backpointer[last_state][t]
        path_indices.insert(0, last_state)

    return [state_names[i] for i in path_indices]


if __name__ == '__main__':
    main()
