import json
import subprocess
import sys

def create_and_run_container(cluster, node, port):
    # Define the container name and build arguments
    container_name = f'container-{cluster}-{node}'
    build_arg = f'ENV_CLI={node}'

    # Build and run the Docker container
    subprocess.run([
        'docker', 'build', '-t', container_name,
        '--build-arg', build_arg, f"clusters/cluster{cluster}/node{node}"
    ])
    subprocess.run([
        'docker', 'run', '-dp', f'0.0.0.0:{port}:{port}', container_name, str(node)
    ])

def main(clusters):
    # Read the mappings from the JSON file
    with open('configs/mapping.json', 'r') as file:
        mappings = json.load(file)

    # Loop through each cluster
    for cluster in clusters:
        cluster = int(cluster)
        for node in range(cluster):
            port = mappings[f'cluster{cluster}'][str(node)]["port"]
            create_and_run_container(cluster, node, port)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/buildContainer.py <cluster_number> <cluster_number> ...")
        exit(1)
    clusters = sys.argv[1:]
    main(clusters)
