import time
import sys
import os
import json
import socket

def find_pi_x(server_socket, data_path):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}", flush = True)

        input_x = float(client_socket.recv(1024).decode("utf-8"))
        print(f"Received data: {input_x}", flush = True)

        # Initialize variables to store the closest x and its corresponding pi(x)
        closest_x = None
        closest_pi_x = None

        # Start the timer to find backend processing time
        start_time = time.time()

        # Open and read the file
        with open(data_path, 'r') as file:  # The CPU should open the file only when request comes; otherwise data already present in code. So no load-balancing effectively taking place
            lines = file.readlines()

        # Iterate through the lines and search for the closest x value
        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                current_x = float(parts[0])
                current_pi_x = float(parts[1])

                # Check if the current x is closer to the input x than the previous closest x
                if closest_x is None or abs(current_x - input_x) < abs(closest_x - input_x):
                    closest_x = current_x
                    closest_pi_x = current_pi_x

        # Stop the timer to find backend processing time
        end_time = time.time()

        execution_time = end_time - start_time
        # Check if a closest match was found
        result = f"Input_x: {input_x}, Closest_x: {closest_x}, pi_x: {closest_pi_x}, Execution_time: {execution_time:.5f} seconds"
        if closest_x is not None:
            print(f"Input x: {input_x}", flush = True)
            print(f"Closest x: {closest_x}", flush = True)
            print(f"Corresponding pi(x): {closest_pi_x}", flush = True)
        else:
            print("No matching x value found in the file.", flush = True)

        print(f"Execution time: {execution_time:.5f} seconds", flush = True)

        client_socket.send(result.encode("utf-8"))

def main():
    node = os.environ["NODE"]
    data_path = f"data/master_file{node}.txt"
    ports_file = "configs/ports.json"
    with open(ports_file, 'r') as file:
        ports = json.load(file)

    server_host = "0.0.0.0"  # Listen on all available network interfaces
    server_port = ports[node]["port"]

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server host and port
    server_socket.bind((server_host, server_port))

    # Listen for incoming connections
    server_socket.listen(10)
    print(f"Server is listening on {server_host}:{server_port}", flush = True)

    find_pi_x(server_socket, data_path)


if __name__ == "__main__":
    main()

