# Load-Balanced System

### Steps to execute sequentially to start and run the cluster manager and then fetch outputs from the cluster
1. Run `cd cluster_manager`
2. Run `python3 src/clusterize.py <cluster_size1> <cluster_size2> ... <cluster_sizeN>  <starting_port>` to create the clusters
3. Run `python3 src/buildContainer.py <cluster_size1> <cluster_size2> ... <cluster_sizeN>` to run the containers
4. Run `cd master`
5. Run `python3 src/input_gen.py <num_inputs>` to generate <num_inputs> random inputs between 1 and `sys.maxsize`
6. Run `python3 src/master.py <cluster> <input_file_path>` depending upon the cluster which you would like to use. Outputs: `times.txt` and `pix.txt` will be saved to the `outpus/cluster` directory
7. Run `python3 src/plotter.py <cluster1> <cluster2> ... <clusterN>` and plots will be saved to `plots` directory
8. Run `python3 src/amdahl.py <cluster1> <cluster2> ... <clusterN>` and plots will be saved to `plots` directory
9. Run `python3 src/gustaf.py <cluster1> <cluster2> ... <clusterN>` and plots will be saved to `plots` directory