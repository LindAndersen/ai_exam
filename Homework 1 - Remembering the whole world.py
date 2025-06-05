A = 'A'
B = 'B'
C = 'C'
D = 'D'
state = {}
action = None
model = {A: None, B: None, C: None, D: None}  # Initially ignorant

RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'NoOp',
    5: 'Up',
    6: 'Down'
}

rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 5,
    (C, 'Clean'): 3,
    (D, 'Clean'): 6,
    (A,B,C,D, 'Clean'): 4
}
# Ex. rule (if location == A && Dirty then rule 1)

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Clean',
    D: 'Dirty',
    'Current': A
}


def INTERPRET_INPUT(input):  # No interpretation
    return input


def RULE_MATCH(state, rules):  # Match rule for a given state
    rule = rules.get(tuple(state))
    return rule


def UPDATE_STATE(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == 'Clean':
        state = (A, B, C, D, 'Clean')
        # Model consulted only for A and B Clean
    model[location] = status  # Update the model state
    return state


def REFLEX_AGENT_WITH_STATE(percept):
    global state, action
    state = UPDATE_STATE(state, action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


def Sensors():  # Sense Environment
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):  # Modify Environment
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right':
        if location == A:
            Environment['Current'] = B
        elif location == D:
            Environment['Current'] = C
    elif action == 'Left':
        if location == B:
            Environment['Current'] = A
        elif location == C:
            Environment['Current'] = D
    elif action == 'Up':
        if location == B:
            Environment['Current'] = C
        elif location == A:
            Environment['Current'] = D
    elif action == 'Down':
        if location == D:
            Environment['Current'] = A
        if location == C:
            Environment['Current'] = B


def run(n):  # run the agent through n steps
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = Sensors()  # Sense Environment before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_AGENT_WITH_STATE(Sensors())
        Actuators(action)
        (location, status) = Sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20)
