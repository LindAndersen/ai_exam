from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.recursive_backtracking(assignment)
                if result != False:
                    return result
                    
        return False

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_australia_csp():
    wa, q, t, v, sa, nt, nsw = 'WA', 'Q', 'T', 'V', 'SA', 'NT', 'NSW'
    values = ['Red', 'Green', 'Blue']
    variables = [wa, q, t, v, sa, nt, nsw]
    domains = {
        wa: values[:],
        q: values[:],
        t: values[:],
        v: values[:],
        sa: values[:],
        nt: values[:],
        nsw: values[:],
    }
    neighbours = {
        wa: [sa, nt],
        q: [sa, nt, nsw],
        t: [],
        v: [sa, nsw],
        sa: [wa, nt, q, nsw, v],
        nt: [sa, wa, q],
        nsw: [sa, q, v],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        wa: constraint_function,
        q: constraint_function,
        t: constraint_function,
        v: constraint_function,
        sa: constraint_function,
        nt: constraint_function,
        nsw: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)

def create_southamerica_csp():
    cr, pan, col, vene, ecu, peru, guy, sur, guyfr, bra, bol, chile, para, arg, uru = 'CR', 'PAN', 'COL', 'VENE', 'ECU', 'PERU', 'GUY', 'SUR', 'GUYFR', 'BRA', 'BOL', 'CHILE', 'PARA', 'ARG', 'URU'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [cr, pan, col, vene, ecu, peru, guy, sur, guyfr, bra, bol, chile, para, arg, uru]
    domains = {
        cr: values[:],
        pan: values[:],
        col: values[:],
        vene: values[:],
        ecu: values[:],
        peru: values[:],
        guy: values[:],
        sur: values[:],
        guyfr: values[:],
        bra: values[:],
        bol: values[:],
        chile: values[:],
        para: values[:],
        arg: values[:],
        uru: values[:],
    }
    neighbours = {
        cr: [pan],
        pan: [col],
        col: [vene, ecu, peru, bra, pan],
        vene: [col, bra, guy],
        ecu: [col, peru],
        peru: [ecu, col, bra, bol, chile],
        guy: [vene, bra, sur],
        sur: [guy, guyfr, bra],
        guyfr: [sur, bra],
        bra: [guyfr, sur, guy, vene, col, peru, bol, para, uru, arg],
        bol: [peru, bra, para, arg, chile],
        chile: [bol, peru, arg],
        para: [bol, bra, arg],
        arg: [bol, para, chile, uru, bra],
        uru: [arg, bra],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        cr: constraint_function,
        pan: constraint_function,
        col: constraint_function,
        vene: constraint_function,
        ecu: constraint_function,
        peru: constraint_function,
        guy: constraint_function,
        sur: constraint_function,
        guyfr: constraint_function,
        bra: constraint_function,
        bol: constraint_function,
        chile: constraint_function,
        para: constraint_function,
        arg: constraint_function,
        uru: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    continent = create_australia_csp()
    continent = create_southamerica_csp()
    result = continent.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
