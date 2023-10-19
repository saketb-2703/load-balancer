import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def calculate(file_name):
    total_sum = 0
    count = 0
    with open(file_name, 'r') as file:
        for line in file.readlines():
            total_sum += float(line.strip())
            count += 1
    return total_sum, total_sum/count

def main(clusters):
    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)

    averages = []
    sums = []
    for cluster in clusters:
        cluster = int(cluster)
        file_name = f"outputs/cluster{cluster}/times.txt"
        cur_sum, cur_avg = calculate(file_name)
        averages.append(cur_avg)
        sums.append(cur_sum)

    # Plot the average values
    plt.plot(averages, marker='o')
    plt.xlabel('Cluster')
    plt.ylabel('Average Value')
    plt.title('Average Value Across Files')
    plt.savefig('plots/avg.jpg')
    plt.clf()

    # Plot the total values
    plt.plot(sums, marker='o')
    plt.xlabel('File Index')
    plt.ylabel('Sum of Values')
    plt.title('Sum of Values Across Files')
    plt.savefig('plots/total.jpg')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/amdahl.py <cluster1> <cluster2> ... <clusterN>")
        exit(1)
    clusters = sys.argv[1:]
    main(clusters)
