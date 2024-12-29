# Take a 2d random square matrix and generating it from this to reach the final matrix where sum of each rows to a particular 
# number X and sum of diagonal should be a particular number Y. 

import numpy as np
import random

# Problem Parameters
matrix_size = 4  # Size of the square matrix (NxN)
target_row_sum = 10  # Desired sum of each row (X)
target_diag_sum = 20  # Desired sum of diagonal (Y)
population_size = 20  # Number of matrices in each generation
generations = 100  # Number of generations
# mutation_rate = 0.1  # Probability of mutation
local_search_iterations = 10


# Initialize a random matrix as a chromosome
def create_random_matrix(size):
    return np.random.randint(1, 10, (size, size))


# Fitness function: Measures how close a matrix is to the target row and diagonal sums
def fitness(matrix):
    row_sums = np.sum(matrix, axis=1)
    diagonal_sum = np.trace(matrix)
    row_difference = np.sum(np.abs(row_sums - target_row_sum))
    diag_difference = abs(diagonal_sum - target_diag_sum)
    return row_difference + diag_difference


# Perform selection: Pick two parents based on fitness (lower is better)
def select_parents(population):
    sorted_population = sorted(population, key=lambda x: fitness(x))
    return sorted_population[0], sorted_population[1]  # Return top two fittest


# Perform crossover between two parent matrices
def crossover(parent1, parent2):
    size = parent1.shape[0]
    cross_point = random.randint(0, size - 1)
    child1 = np.vstack((parent1[:cross_point, :], parent2[cross_point:, :]))
    child2 = np.vstack((parent2[:cross_point, :], parent1[cross_point:, :]))
    return child1, child2


def mutate(matrix):
    size = matrix.shape[0]
    row, col = random.randint(0, size - 1), random.randint(0, size - 1)
    matrix[row, col] += random.choice([-1, 1])
    return matrix


def local_search(matrix):
    """Perform local optimization by tweaking matrix to improve fitness."""
    best_matrix = matrix.copy()
    best_fitness = fitness(best_matrix)
    for _ in range(local_search_iterations):
        temp_matrix = mutate(matrix.copy())
        temp_fitness = fitness(temp_matrix)
        if temp_fitness < best_fitness:
            best_matrix = temp_matrix
            best_fitness = temp_fitness
    return best_matrix


def genetic_algorithm(population):
    """Solve the matrix problem using Genetic Algorithm."""
    for generation in range(generations):
        # Step 2: Evaluate fitness of population
        population = sorted(population, key=fitness)
        best_matrix = population[0]
        best_fitness = fitness(best_matrix)
        
        # Step 3: Termination check
        if best_fitness == 0:  # Perfect solution found
            print(f"Genetic Algorithm: Solution found at generation {generation}!")
            return best_matrix
        
        # Step 4: Create next generation
        new_population = []
        
        # Always keep the best two (elitism)
        new_population.extend(population[:2])
        
        # Generate offspring
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
        
        # Update population
        population = new_population[:population_size]
    
    print("Genetic Algorithm: No perfect solution found.")
    return population[0]


def memetic_algorithm(population):
    """Solve the matrix problem using Memetic Algorithm."""
    for generation in range(generations):
        # Step 2: Evaluate fitness of population
        population = sorted(population, key=fitness)
        best_matrix = population[0]
        best_fitness = fitness(best_matrix)
        
        # Step 3: Termination check
        if best_fitness == 0:  # Perfect solution found
            print(f"Memetic Algorithm: Solution found at generation {generation}!")
            return best_matrix
        
        # Step 4: Create next generation
        new_population = []
        
        # Always keep the best two (elitism)
        new_population.extend(population[:2])
        
        # Generate offspring
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            
            # Apply local search
            child1 = local_search(child1)
            child2 = local_search(child2)
            
            new_population.extend([child1, child2])
        
        # Update population
        population = new_population[:population_size]
    
    print("Memetic Algorithm: No perfect solution found.")
    return population[0]


if __name__ == "__main__":
    # Initialize a shared population
    initial_population = [create_random_matrix(matrix_size) for _ in range(population_size)]
    
    print("Solving with Genetic Algorithm...")
    genetic_result = genetic_algorithm(initial_population.copy())
    print("Best solution (Genetic Algorithm):")
    print(genetic_result)
    print("Fitness:", fitness(genetic_result))
    print("Row Sums:", np.sum(genetic_result, axis=1))
    print("Diagonal Sum:", np.trace(genetic_result))
    

    print("\nSolving with Memetic Algorithm...")
    memetic_result = memetic_algorithm(initial_population.copy())
    print("Best solution (Memetic Algorithm):")
    print(memetic_result)
    print("Row Sum:", np.sum(memetic_result,axis = 1))
    print("Diagonal Sums:", np.trace(memetic_result))
    print("Fitness:", fitness(memetic_result))

















'''

Algorithm Explanation: 

Start with a randomly generated 2D square matrix.
Goal: Transform this matrix so:
----The sum of each row equals X.
----The sum of the diagonal equals Y.


Genetic Algorithm Components:

-- Chromosome Representation: Each matrix is treated as a chromosome.
-- Population Initialization: Create an initial population of random matrices.
-- Fitness Function: Measure how close a matrix is to the desired row sums and diagonal sum.
-- Selection: Select the fittest matrices for crossover.
-- Crossover: Combine two parent matrices to create offspring.
-- Mutation: Introduce small changes to a matrix to maintain diversity.
-- Termination: Stop when a solution meets the conditions or after a maximum number of iterations.


Fitness Function:

Calculate deviations of row sums from X and the diagonal sum from Y:

Fitness = sum of absolute deviations from X
                  +
          absolute deviation from Y

Fitness = sum of absolute deviations from X + absolute deviation from Y

'''