import os
import sys
import time
import random
from random import seed
from random import randint

def main(num_inputs):
    input_file_path = "data/master_file.txt"
    output_file_dir = "inputs"
    os.makedirs(output_file_dir, exist_ok=True)
    output_file_name = "inputs.txt"
    output_file_path = os.path.join(output_file_dir, output_file_name)

    with open(output_file_path, "w") as file: # Clear the file if it exists
        pass

    data = []
    available_x_values = []
    with open(input_file_path, 'r') as input_file:
        data = input_file.readlines()

    for i in range(len(data)):
        line = data[i]
        parts = line.split()

        if len(parts) == 3 or len(parts) == 11:
            available_x_values.append(float(parts[0]))

    with open(output_file_path, "a") as file:
        count = 0
        while count != num_inputs:
            '''
            # Execute this code snippet if you want to take x_values only from the master_file.txt; Comment the next code snippet accordingly
            # random_number = random.choice(available_x_values)
            # if int(random_number) != random_number:
            #     continue
            '''

            seed(time.time())
            if count % 2 == 0:
                # Generate a random number with a triangular distribution between 1 and 1e10
                random_number = int(random.triangular(1, 1e10, 1e10))
            else:
                # Generate a random number with a triangular distribution between 1e10 and 1e20
                random_number = int(random.triangular(1e10, 1e20, sys.maxsize))
                
            file.write(str(random_number))
            file.write('\n')
            count += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/input_gen.py <num_inputs>")
        exit(1)
    num_inputs = int(sys.argv[1])
    main(num_inputs)
