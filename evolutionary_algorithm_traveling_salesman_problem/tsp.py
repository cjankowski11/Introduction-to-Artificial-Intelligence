import random

SIZE_OF_THE_POPULATION = 300
P_MUTATION = 4/10
P_CROSSBREEDING = 4/5
T_MAX = 500
PENALTY_CONST = 1e9

TOWNS = {"A": (0, 0),
         "B": (1, 3),
         "C": (2, 1),
         "D": (4, 6),
         "E": (5, 2),
         "F": (6, 5),
         "G": (8, 7),
         "H": (9, 4),
         "I": (10, 8),
         "J": (12, 3)}


def calculate_distance(town1, town2):
    return ((TOWNS[town1][0]-TOWNS[town2][0])**2 + (TOWNS[town1][1]-TOWNS[town2][1])**2)**(1/2)


def total_cost(starting_point, x):
    cost = calculate_distance(starting_point, x[0])
    for i in range(len(x)-1):
        cost += calculate_distance(x[i], x[i+1])
    cost += calculate_distance(x[-1], starting_point)
    for town in x:
        if x.count(town) > 1:
            penalty = x.count(town)**2*PENALTY_CONST
            cost += penalty
    return cost


def generate_individual(townsnames, n_towns):
    individual = []
    for _ in range(n_towns):
        town = random.choice(townsnames)
        individual.append(town)
        townsnames.remove(town)
    return individual


def generate_first_population(size_of_the_population):
    towns_names = [key for key, item in TOWNS.items()]
    starting_point = random.choice(towns_names)
    # starting_point = "A"
    towns_names.remove(starting_point)
    population = []
    for _ in range(size_of_the_population):
        population.append(generate_individual(towns_names.copy(), len(towns_names)))
    return population, starting_point


def find_best_individual(starting_point, population):
    best_ind = population[0]
    best_cost = total_cost(starting_point, population[0])

    for individual in population:
        cost = total_cost(starting_point, individual)
        if cost < best_cost:
            best_ind, best_cost = individual, cost
    return best_ind, best_cost

# generate_individual("a")


def roulette_selection(starting_point, population):
    new_population = []
    denominator = sum(total_cost(starting_point, i) for i in population)
    roulette = []
    sum_cost = 0
    for individual in population:
        sum_cost += round(denominator/total_cost(starting_point, individual)*100)
        roulette.append(sum_cost)

    # print(roulette)
    for _ in range(len(population)):
        random_n = random.randint(0, roulette[-1])
        i = 0
        while random_n > roulette[i]:
            i += 1
        new_population.append(population[i])
    #     print(random_n)
    # print(new_population,"\n")        
    return new_population


def crossbreeding_and_mutation(reproduction, crossb_probability, mutation_probability):
    new_population = []
    for _ in range(len(reproduction)//2):
        male = random.choice(reproduction)
        reproduction.remove(male)
        female = random.choice(reproduction)
        reproduction.remove(female)
        if random.random() < crossb_probability:
            male, female = crossbreeding(male, female) 

        if random.random() < mutation_probability:
            male = mutation(male)
        if random.random() < mutation_probability:
            female = mutation(female)
        new_population.append(male)
        new_population.append(female)
    return new_population


def crossbreeding(male, female):
    r_number = random.randint(1, len(male)-1)
    return male[:r_number] + female[r_number:], female[:r_number] + male[r_number:]


def mutation(individual):
    random_n = random.randint(0,len(individual)-1)
    random_destination = random.randint(0, len(individual)-1)
    while random_n == random_destination:
        random_destination = random.randint(0, len(individual)-1)
    letter = individual.pop(random_n)
    individual.insert(random_destination, letter)
    return individual


def how_many_unique(population):
    unique = []
    for i in population:
        if i not in unique:
            unique.append(i)
    return len(unique)


if __name__ == "__main__":
    population, starting_town = generate_first_population(SIZE_OF_THE_POPULATION)

    t = 0
    best_individual, best_cost = find_best_individual(starting_town, population)

    while t < T_MAX:
        reproduction = roulette_selection(starting_town, population)
        m = crossbreeding_and_mutation(reproduction, P_CROSSBREEDING, P_MUTATION)

        c_p_best_individual, c_p_best_cost = find_best_individual(starting_town, m)
        if c_p_best_cost < best_cost:
            best_individual, best_cost = c_p_best_individual, c_p_best_cost
        population = m
        
        t += 1
    print([starting_town]+best_individual+[starting_town], best_cost)
    # print(crossbreeding(["A","B","C"],["D","E","F"]))
    # print(mutation(["A","B","C"]))
    
