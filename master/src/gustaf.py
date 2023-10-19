import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def calculate(alpha, N):
    return alpha + (1 - alpha) * N

def main(clusters):
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)
    
    speedups = []
    efficiency = []

    for cluster in clusters:
        cluster = int(cluster)
        speedup = calculate(1 / cluster, cluster)
        speedups.append(speedup)
        efficiency.append(speedup / cluster)

    # Plot speedup values
    plt.plot(clusters, speedups)
    plt.xlabel('Cluster')
    plt.ylabel('Speedup')
    plt.title('Speedup Value Across Clusters')
    plt.savefig('plots/gustaf_s.jpg')
    plt.clf()

    # Plot efficiency values
    plt.plot(clusters, efficiency)
    plt.xlabel('Cluster')
    plt.ylabel('Efficiency')
    plt.title('Efficiency Across Clusters')
    plt.savefig('plots/gustaf_e.jpg')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/gustaf.py <cluster1> <cluster2> ... <clusterN>")
        exit(1)
    clusters = sys.argv[1:]
    main(clusters)
