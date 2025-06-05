import itertools

# Prior probabilities
P_DT = {'true': 0.3, 'false': 0.7}
P_EM = {'true': 0.3, 'false': 0.7}
P_FTL = {'true': 0.2, 'false': 0.8}

# CPTs
P_V_given_DT = {
    'true': {'true': 0.7, 'false': 0.3},
    'false': {'true': 0.1, 'false': 0.9}
}

P_SMS_given_DT_EM = {
    ('true', 'true'): {'true': 0.05, 'false': 0.95},
    ('true', 'false'): {'true': 0.6, 'false': 0.4},
    ('false', 'true'): {'true': 0.3, 'false': 0.7},
    ('false', 'false'): {'true': 0.7, 'false': 0.3}
}

P_HC_given_DT_FTL_EM = {
    ('true', 'true', 'true'): {'true': 0.9, 'false': 0.1},
    ('true', 'true', 'false'): {'true': 0.8, 'false': 0.2},
    ('true', 'false', 'true'): {'true': 0.3, 'false': 0.7},
    ('true', 'false', 'false'): {'true': 0.2, 'false': 0.8},
    ('false', 'true', 'true'): {'true': 0.6, 'false': 0.4},
    ('false', 'true', 'false'): {'true': 0.5, 'false': 0.5},
    ('false', 'false', 'true'): {'true': 0.1, 'false': 0.9},
    ('false', 'false', 'false'): {'true': 0.01, 'false': 0.99}
}

# Evidence
evidence = {
    'V': 'true',       # Vibrations
    'SMS': 'true',     # Slow Max Speed
    'HC': 'false'      # High Consumption
}

# Variable name map
variable_names = {
    'DT': 'Damaged Tire',
    'EM': 'Electronics Malfunctioning',
    'FTL': 'Fuel Tank Leaking',
    'V': 'Vibrations',
    'SMS': 'Slow Max Speed',
    'HC': 'High Consumption'
}


def joint_probability(DT_val, EM_val, FTL_val, evidence):
    p = 1.0
    p *= P_DT[DT_val]
    p *= P_EM[EM_val]
    p *= P_FTL[FTL_val]
    p *= P_V_given_DT[DT_val][evidence['V']]
    p *= P_SMS_given_DT_EM[(DT_val, EM_val)][evidence['SMS']]
    p *= P_HC_given_DT_FTL_EM[(DT_val, FTL_val, EM_val)][evidence['HC']]
    return p


def compute_posterior(query_var):
    posterior = {}
    total = 0.0

    for query_val in ['true', 'false']:
        prob = 0.0
        for DT_val, EM_val, FTL_val in itertools.product(['true', 'false'], repeat=3):
            if query_var == 'DT' and DT_val != query_val:
                continue
            if query_var == 'EM' and EM_val != query_val:
                continue
            if query_var == 'FTL' and FTL_val != query_val:
                continue
            prob += joint_probability(DT_val, EM_val, FTL_val, evidence)

        posterior[query_val] = prob
        total += prob

    for k in posterior:
        posterior[k] /= total

    return posterior


def main():
    print("Posterior probabilities given the following evidence:\n")
    for ev_key in evidence:
        full_name = variable_names[ev_key]
        print(f"  {full_name}: {evidence[ev_key].capitalize()}")
    print()

    posteriors = {}
    for var in ['DT', 'EM', 'FTL']:
        full_name = variable_names[var]
        posterior = compute_posterior(var)
        posteriors[var] = posterior['true']
        print(f"P({full_name} | evidence):")
        print(f"  Yes: {posterior['true']:.5f}")
        print(f"  No:  {posterior['false']:.5f}\n")

    # --- Conclusion ---
    print("Conclusion:")
    likely_causes = {variable_names[k]: v for k, v in posteriors.items() if v > 0.5}
    if likely_causes:
        sorted_causes = sorted(likely_causes.items(), key=lambda item: item[1], reverse=True)
        print("  Based on the evidence, the most likely cause(s) of the malfunction are:")
        for name, prob in sorted_causes:
            print(f"    - {name} (P = {prob:.4f})")
    else:
        print("  No likely mechanical fault identified with >50% probability based on current evidence.")


if __name__ == '__main__':
    main()
