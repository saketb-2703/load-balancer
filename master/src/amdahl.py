import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def calculate(file_name):
    total_sum = 0
    count = 0
    with open(file_name, 'r') as file:
        for line in file.readlines():
            total_sum += float(line.strip())
            count += 1
    return total_sum

# def calculate(alpha, N):
#     return 1/(alpha + (1 - alpha)/N)

def main(clusters):
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    
    speedups = []
    efficiency = []

    file_name1 = f"outputs/cluster1/times.txt"
    cluster1_sum = calculate(file_name1)
    for cluster in clusters:
        cluster = int(cluster)
        file_name = f"outputs/cluster{cluster}/times.txt"
        cur_sum = calculate(file_name)
        speedups.append(cluster1_sum / cur_sum)
        efficiency.append(speedups[-1] / cluster)

    plt.plot(clusters, speedups, marker='o')
    plt.xlabel('Cluster')
    plt.ylabel('Speedup')
    plt.title('Speedup Value Across Clusters')
    plt.savefig('plots/amdahl_s.jpg')
    plt.clf()

    # Plot the total values
    plt.plot(clusters, efficiency, marker='o')
    plt.xlabel('Cluster')
    plt.ylabel('Efficiency')
    plt.title('Efficiency Across Clusters')
    plt.savefig('plots/amdahl_e.jpg')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/amdahl.py <cluster1> <cluster2> ... <clusterN>")
        exit(1)
    clusters = sys.argv[1:]
    main(clusters)
