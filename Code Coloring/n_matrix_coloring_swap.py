# Import necessary libraries
import random  # To generate random integers for initializing the matrix
import copy  # To create deep copies of data structures
from coloring_gui import draw  # Imports draw function, used for visualization



# Helper function to get the third element in a list or tuple
def return_second(elem):
    return elem[2]



# Helper function to print each row of the matrix
def print_data(data):
    for k in data:
        print(k)



# Function to check for adjacent identical elements in rows and columns
# Returns the first position of adjacent identical elements if found, else returns 1
def check(data):
    for m in range(len(data)):
        for n in range(len(data) - 1):
            if data[m][n] == data[m][n + 1]:  # Check for identical elements in rows
                return (m, n)
            if data[n][m] == data[n + 1][m]:  # Check for identical elements in columns
                return (n, m)
    return 1  # Return 1 if no adjacent identical elements are found



# Function to find all positions where there are adjacent identical elements
# Returns a list of positions where collisions are found
def get_collissions(array):
    collissions = []

    for m in range(len(array) - 1):
        for n in range(len(array)):
            # Check for vertical collisions
            if (array[m][n] == array[m + 1][n]):
                if (m, n) not in collissions:
                    collissions.append((m, n))
                if (m + 1, n) not in collissions:
                    collissions.append((m + 1, n))
            # Check for horizontal collisions
            if (array[n][m] == array[n][m + 1]):
                if (n, m) not in collissions:
                    collissions.append((n, m))
                if (n, m + 1) not in collissions:
                    collissions.append((n, m + 1))
    return collissions  # List of positions with adjacent identical elements



# Counts the total number of "collisions" or adjacent identical elements in the matrix
def count_collisions(array):
    return len(get_collissions(array))



# Returns a list of values excluding the given value, used to find alternative values for replacement
def get_possibilities(value):
    val = [0, 1, 2, 3]  # Possible values in the matrix
    val.remove(value)  # Remove the current value to get possible alternatives
    return val



# Returns a list of adjacent positions for a given cell, ensuring positions are within bounds
def get_possibilities_2(input_array, pos):
    possibilities = []
    n = pos[0]
    m = pos[1]
    size = len(input_array[0]) - 1  # Matrix bounds
    for i in [-1, 1]:  # Check left and right neighbors
        if (m + i) >= 0 and m + i <= size:
            possibilities.append((m + i, n))
    for j in [-1, 1]:  # Check up and down neighbors
        if (n + j) >= 0 and n + j <= size:
            possibilities.append((m, n + j))
    return possibilities



# Generates an n x n matrix filled with random values between 0 and 3
def generate_matrix(number_of_rows):
    data = []
    for i in range(number_of_rows):
        temp = []
        for j in range(number_of_rows):
            temp.append(random.randint(0, 3))  # Random value in range [0, 3]
        data.append(temp)
    return data



# Function called when the matrix is "solved" (no collisions)
# Prints the result and visualizes it
def done(original, data):
    print("\n**Done**")
    print_data(data[0])
    print("Cost: " + str(data[1]))  # Display the cost (steps taken)
    draw(original, data[0])  # Visualize the solved matrix
    exit(0)  # Exit the program



# Main code execution
original_array = generate_matrix(int(input("\nEnter n: ")))  # Create an n x n matrix

print_data(original_array)  # Display the initial matrix

count = 0  # Step counter
queue = []  # Queue to store states to explore
extended_list = []  # List to track explored states
queue.append([original_array, 0, count_collisions(original_array)])  # Initial state with cost 0



# User input for search type
usr_input = int(input("\n1. BFS\n2. DFS\n3. Greedy Best First Search\n"))
if usr_input > 3 or usr_input < 1:  # Validate input
    print("Invalid Input!")
    exit(0)



# Search algorithm loop
while queue:
    popped_array = queue.pop(0)  # Remove the first element for processing
    count += 1
    extended_list.append(popped_array[0])  # Mark the current state as explored

    checked_pos = check(popped_array[0])  # Check for collisions
    if checked_pos == 1:  # If no collisions, solution is found
        done(original_array, popped_array)
    else:
        collisions = get_collissions(popped_array[0])  # Get collision positions

        for col in collisions:
            possibilities = get_possibilities_2(popped_array[0], col)  # Get neighboring positions to swap
            m, n = col

            # Attempt to resolve each collision by swapping values
            for z in possibilities:
                temp_data = copy.deepcopy(popped_array[0])  # Deep copy to preserve the current state
                swap_element = temp_data[m][n]  # Swap values to try a new state
                temp_data[m][n] = temp_data[z[0]][z[1]]
                temp_data[z[0]][z[1]] = swap_element

                collissions = count_collisions(temp_data)  # Count collisions in the new state
                insert_data = [temp_data, popped_array[1] + 1, collissions]  # New state data

                # Only add new state if it hasn't been explored
                if temp_data not in extended_list:
                    if usr_input == 1:  # BFS: add to end of queue
                        queue.append(insert_data)
                    elif usr_input == 2:  # DFS: add to front of queue
                        queue.insert(0, insert_data)
                    elif usr_input == 3:  # Greedy Best First: add, then sort by collisions
                        queue.append(insert_data)
                        queue.sort(key=return_second)

                # Print status of queue, extended list, cost, and collisions
                print("Queue: " + str(len(queue)) + " Extended: " + str(len(extended_list)) +
                      " Cost: " + str(popped_array[1] + 1) + " Collissions: " + str(collissions))

                # Check if the new state is solved
                if check(temp_data) == 1:
                    done(original_array, [temp_data, popped_array[1] + 1])



# If no solution is found after exploring all possibilities
print("\n**No possible Permutation found**")


