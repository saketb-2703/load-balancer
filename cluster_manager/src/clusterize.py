import os
import sys
import json

def masterconfigFileCreate(starting_port, node_dir, cluster, node):
    master_config_dir = "../master/configs"

    os.makedirs(master_config_dir, exist_ok=True)
    master_config_file_name = "mapping.json"
    master_config_file_path = f"{master_config_dir}/{master_config_file_name}"
    cluster_config_dir = f"configs"
    os.makedirs(cluster_config_dir, exist_ok=True)
    cluster_config_file_name = "mapping.json"
    cluster_config_file_path = f"{cluster_config_dir}/{cluster_config_file_name}"
    
    mapping = {}
    if os.path.exists(master_config_file_path):
        with open(master_config_file_path, 'r') as file:
            mapping = json.load(file)
    mapping.setdefault(f"cluster{cluster}", {})
    data_path = f"{node_dir}/data/master_file{node}.txt"
    with open(data_path, 'r') as file:
        lines = file.readlines()
    
    first_x = None
    last_x = None
    for line in lines:
        parts = line.split()
        if len(parts) == 3 or len(parts) == 11:
            if first_x is None:
                first_x = float(parts[0])
            last_x = float(parts[0])
    port = starting_port + ((cluster + 1) * 10) + node
    mapping[f"cluster{cluster}"][node] = {"first_x": first_x, "last_x": last_x, "port": port}


    with open(master_config_file_path, 'w') as file:
        json.dump(mapping, file, indent=4)
    with open(cluster_config_file_path, 'w') as file:
        json.dump(mapping, file, indent=4)


def configFileCreate(node_dir, cluster):
    config_file = "../master/configs/mapping.json"
    with open(config_file, 'r') as file:
        ports = json.load(file)

    node_config_dir = os.path.join(node_dir, "configs")
    os.makedirs(node_config_dir, exist_ok=True)
    node_config_file_name = "ports.json"
    node_config_file_path = f"{node_config_dir}/{node_config_file_name}"

    cluster_configs = ports[f"cluster{cluster}"]   # entire cluster node's config file included in every node
    with open(node_config_file_path, 'w') as file:
        json.dump(cluster_configs, file, indent=4)

def dataFileCreate(node_dir, cluster, node):
    data_file = 'data/master_file.txt'
    pix_data = []
    with open(data_file, 'r') as file:
        pix_data = file.readlines()
    lines_per_file = len(pix_data) // cluster

    start_idx = node * lines_per_file
    end_idx = (node + 1) * lines_per_file if node < cluster - 1 else None

    node_data_dir = os.path.join(node_dir, "data")
    os.makedirs(node_data_dir, exist_ok=True)
    node_data_file_name = f"master_file{node}.txt"
    node_data_file_path = f"{node_data_dir}/{node_data_file_name}"

    with open(node_data_file_path, 'w') as output_file:
        if end_idx is not None:
            output_file.writelines(pix_data[start_idx:end_idx])
        else:
            output_file.writelines(pix_data[start_idx:])  # For the last output_file, since it may not cover exactly cluster_size's dividable number of lines

def srcFileCreate(node_dir):
    src_file = "src/node.py"
    with open(src_file, 'r') as file:
        src = file.read()

    node_src_dir = os.path.join(node_dir, "src")
    os.makedirs(node_src_dir, exist_ok=True)
    node_src_file_name = "node.py"
    node_src_file_path = f"{node_src_dir}/{node_src_file_name}"

    with open(node_src_file_path, 'w') as file:
        file.write(src)

def dockerFileCreate(node_dir):
    docker_file = "src/Dockerfile"
    with open(docker_file, 'r') as file:
        docker = file.read()

    node_docker_dir = node_dir
    node_docker_file_name = "Dockerfile"
    node_docker_file_path = f"{node_docker_dir}/{node_docker_file_name}"

    with open(node_docker_file_path, 'w') as file:
        file.write(docker)

def main(clusters, starting_port):
    for cluster in clusters:
        cluster = int(cluster)
        clusters_dir = f"clusters"
        os.makedirs(clusters_dir, exist_ok=True)
        cluster_dir = os.path.join(clusters_dir, f"cluster{cluster}")
        os.makedirs(cluster_dir, exist_ok=True)

        for node in range(cluster):
            node_dir = os.path.join(cluster_dir, f"node{node}")
            os.makedirs(node_dir, exist_ok=True)

            dockerFileCreate(node_dir)
            dataFileCreate(node_dir, cluster, node)
            masterconfigFileCreate(starting_port, node_dir, cluster, node)
            configFileCreate(node_dir, cluster)
            srcFileCreate(node_dir)
        print(f"Cluster{cluster} created with {cluster} node(s).")
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/clusterize.py <cluster_size1> <cluster_size2> ... <cluster_sizeN>  <starting_port>")
        sys.exit(1)
    clusters = sys.argv[1:-1]
    starting_port = int(sys.argv[-1])
    main(clusters, starting_port)
