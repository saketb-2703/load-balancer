import socket
import json
import sys
import time
import os



def find_port_in_cluster(cluster_dict, cluster_no, x_value):
    cluster_name = f"cluster{cluster_no}"
    x_value = float(x_value)

    # Check if the cluster exists in the dictionary
    if cluster_name in cluster_dict:
        cluster = cluster_dict[cluster_name]

        for _, value in cluster.items():
            start_x, end_x = float(value["first_x"]), float(value["last_x"])
            if start_x <= x_value <= end_x:
                return value["port"]

    return None  

def main(cluster, input_file_path):
    mapping_file = "configs/mapping.json"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_cluster_dir = os.path.join(output_dir, f"cluster{cluster}")
    os.makedirs(output_cluster_dir, exist_ok=True)
    output_times_file_name = "times.txt"
    output_times_file_path = os.path.join(output_cluster_dir, output_times_file_name)       
    output_pix_file_name = "pix.txt"    
    output_pix_file_path = os.path.join(output_cluster_dir, output_pix_file_name)

    mapping = {}
    with open(mapping_file) as file:
        mapping = json.load(file)

    with open(input_file_path, "r") as file:
        for line in file:
            x_value = line.strip()
            if x_value:
                # Finding time taken to execute the request
                start_time = time.time()

                print(f"Sending {x_value} to the server...")
                server_host = "0.0.0.0"  # Change this to the server's IP address if it's running on a different machine
                server_port = find_port_in_cluster(mapping, cluster, x_value)

                if server_port is not None:
                    server_port = int(server_port)
                else:
                    print(f"Invalid port for x_value = {x_value}")  # Server_port not in mapping dictionary
                    continue

                # Create a socket object
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to the server
                try:
                    print(f"Connecting to {server_host}:{server_port}")
                    client_socket.connect((server_host, server_port))
                except socket.error as msg:
                    print(f"Failed to connect: {msg}")
                else:
                    print(f"Successfully connected to {server_host}:{server_port}")

                # Send the number to the server
                client_socket.send(x_value.encode("utf-8"))

                # Receive the response from the server
                response = client_socket.recv(1024).decode("utf-8")

                # Finding the time taken to execute the request
                end_time = time.time()
                execution_time = end_time - start_time

                with open(output_times_file_path, "a") as file:
                    file.write(str(execution_time))
                    file.write('\n')

                key_value_pairs = [pair.strip() for pair in response.split(',')]
                print(key_value_pairs)
                pi_x_value = None
                for pair in key_value_pairs:
                    key, value = pair.split(':')
                    if key.strip() == 'pi_x':
                        pi_x_value = value.strip()
                        with open(output_pix_file_path, "a") as file:
                            file.write(pi_x_value)
                            file.write('\n')



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 src/master.py <cluster> <input_file_path>")
        exit(1)
    cluster = int(sys.argv[1])
    input_file_path = sys.argv[2]
    main(cluster, input_file_path)