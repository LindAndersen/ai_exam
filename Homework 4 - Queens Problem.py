import random

p_mutation = 0.2
num_of_generations = 4000
max_population = 10
dict_conflicts = {}


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        #print_population(population, fitness_fn)

        new_population = set()
        
        ordered_population, probabilities = prep_generation_calculations(population, fitness_fn)
        
        if len(population) > max_population:
            population = set(random.choices(ordered_population, weights=probabilities, k=max_population))

        for i in range(len(population)):
            mother, father = random_selection(ordered_population, probabilities)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break



    #print("Final generation {}:".format(generation))
    #print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother:tuple, father:tuple):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    crossover_point = random.randint(1,len(mother)-1)
    
    child = mother[:crossover_point] + father[crossover_point:]

    return child


def mutate(individual:tuple):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    
    mutation = list(individual).copy()
    mutation[random.randint(0,7)] = random.randint(1,8)
    

    return tuple(mutation)

def prep_generation_calculations(population, fitness_fn):
    ordered_population = list(population)
    total_fitness = sum([fitness_fn(n) for n in population])

    min_fitness = min(fitness_fn(n) for n in population)
    shifted_fitness = [(fitness_fn(n) - min_fitness+1) for n in ordered_population]
    total_fitness = sum(shifted_fitness)
    probabilities = [f / total_fitness for f in shifted_fitness]
    
    return ordered_population, probabilities


def random_selection(ordered_population, probabilities):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """
    
    selected = random.choices(ordered_population, weights=probabilities, k=2)

    return tuple(selected)


def fitness_function(individual):
    '''
    Compute the number of conflicting pairs, negated.
    For a solution with 5 conflicting pairs the return value is -5, so it can
    be maximized to 0.
    '''
    
    if individual in dict_conflicts:
        return dict_conflicts[individual]

    n = len(individual)
    fitness = 0
    for column, row in enumerate(individual):
        contribution = 0

        # Horizontal
        for other_column in range(column + 1, n):
            if individual[other_column] == row:
                contribution += 1

        # Diagonals
        for other_column in range(column + 1, n):
            row_a = row + (column - other_column)
            row_b = row - (column - other_column)
            if 0 <= row_a < n and individual[other_column] == row_a:
                contribution += 1
            if 0 <= row_b < n and individual[other_column] == row_b:
                contribution += 1

        fitness += contribution
    
    dict_conflicts[individual] = -fitness

    return - fitness

def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(1, 8) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 0
    run_count = 0

    while True:
        run_count += 1
        print(f"Starting run {run_count}...\n")

        initial_population = get_initial_population(8, 2)
        fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)

        if fitness_function(fittest) == minimal_fitness:
            print(f"\nSolution found in {run_count} runs!")
            print(f"Fittest Individual: {fittest}")
            break


if __name__ == '__main__':
    main()
