# Implementation of (MU, LAMBDA) Evolution Strategy
import random
import math

X_MIN = -2.0 # minimum x allowed
X_MAX = 2.0 # maximum x allowed
MU = 5 # number of parents selected
LAMBDA = 20 # number of children generated by the parents
P_MUTATION = 0.1 # probability of mutation
P_CROSSOVER = 0.1 # probability of crossover
CHROMOSOME_SIZE = 8 # define the length of binary string

# function f(x) ****TEST FUNCTION HERE****
def f(t_num, chromosome):
    x = inContext(X_MIN, X_MAX, toDecimal(chromosome))
    if t_num == 0:
        return (6*x-2)**2 * math.sin(12*x-4)
    elif t_num == 1:
        return -2*(x**3) * math.sin(x**5+4)
    elif t_num == 2:
        return 3*(x**3) * math.cos(3*(x**3)+3)

# generate initial population
def initial_population(n_population):
    population = []
    for p_index in range(n_population):
        chromosome = ""
        for c_index in range(CHROMOSOME_SIZE):
            chromosome += random.choice(["0", "1"])
        population.append(chromosome)
    return population

# generaet initial chromosome based on number of variables
def initial_chromosome(n_var):
    chromosome = ""
    for index in range(CHROMOSOME_SIZE * n_var):
        chromosome += "x"
    return chromosome

# loop stops when the condition is not met
def loop_condition_is_met(t, timeCounter):
    timeLimit = 1000
    return timeCounter < timeLimit

# convert the binary into decimal
def toDecimal(binaryString):
    decimalNumber = 0
    length = len(binaryString)
    for index, digit in enumerate(binaryString):
        if digit == "1":
            decimalNumber += 2**(length - index - 1)
    return decimalNumber

# convert the decimal number into real value in context
def inContext(x_min, x_max, decimal):
    r_min = 0.0
    r_max = 2**CHROMOSOME_SIZE-1
    precision = (x_max - x_min) / (r_max - r_min)
    return x_min + decimal * precision

# return top {MU} individuals
def truncation_selection(fitnessList, mu):
    indices = []
    # copy of the fitness list
    tempList = fitnessList
    for counter in range(mu):
        bestIndex = 0 # initially set the best as 0
        bestFitness = tempList[0] # initially set the best as index 0
        for index, fitness in enumerate(tempList):
            if tempList[index] > bestFitness:
                bestIndex = index
        indices.append(bestIndex) # add the best index to indices
        tempList.remove(tempList[bestIndex]) # remove the best from the list
    # return the indices of the top scored individuals
    return indices

# mutate each index of a chromosome with a chance of P_MUTATION
def mutated(chromosome):
    mutatedChromosome = ""
    for index in range(CHROMOSOME_SIZE):
        if random.uniform(0.0, 1.0) < P_MUTATION:
            if chromosome[index] == "0":
                mutatedChromosome += "1"
            elif chromosome[index] == "1":
                mutatedChromosome += "0"
        else:
            mutatedChromosome += chromosome[index]
    return mutatedChromosome

# (MU, LAMBDA) Evolution Strategy main function
def mu_lambda_evoulution_strategy(t=0, n_var=1):
    population = initial_population(LAMBDA)
    bestGene = initial_chromosome(n_var)
    timeCounter = 0
    while loop_condition_is_met(t, timeCounter):
        # list that stores fitness of chromosomes with the same indices
        fitness = []
        for chromosome in population:
            # assess fitness
            fitness.append(f(t,chromosome))
            # determine the best gene
            if bestGene[0] == "X" or f(t,chromosome) < f(t,bestGene):
                bestGene = chromosome
        # the MU individuals in P whose fitness are greatest
        survivors = []
        truncated_indices = truncation_selection(fitness, MU)
        for index in truncated_indices:
            survivors.append(population[index])
        # join by replacing P with LAMBDA/MU * MU (=LAMBDA) children
        population = []
        for individual in survivors:
            for copy in range(LAMBDA/MU):
                population.append(mutated(individual))
        # increment time counter
        timeCounter += 1
    # print the result
    print "(MU, LAMBDA) Evolution Strategy: " +\
            str((bestGene, round(f(t,bestGene), 3)))
    # return the result
    return (bestGene, round(f(t,bestGene), 3))

# execute
mu_lambda_evoulution_strategy()
