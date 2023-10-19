# Load-Balanced System

### Steps to execute sequentially to start and run the cluster manager and then fetch outputs from the cluster
1. Download the data file from (https://www.dropbox.com/scl/fi/90uq8i4k3h3n3xo033a90/master_file.txt?rlkey=094ev8lapojteo30iducby69f&dl=0) and place the data file `master_file.txt` under `cluster_manager/data` and `master/data`
2. Run `cd cluster_manager`
3. Run `python3 src/clusterize.py <cluster_size1> <cluster_size2> ... <cluster_sizeN>  <starting_port>` to create the clusters
4. Run `python3 src/buildContainer.py <cluster_size1> <cluster_size2> ... <cluster_sizeN>` to run the containers
5. Run `cd master`
6. Run `python3 src/input_gen.py <num_inputs>` to generate <num_inputs> random inputs between 1 and `sys.maxsize`
7. Run `python3 src/master.py <cluster> <input_file_path>` depending upon the cluster which you would like to use. Outputs: `times.txt` and `pix.txt` will be saved to the `outpus/cluster` directory
8. Run `python3 src/plotter.py <cluster1> <cluster2> ... <clusterN>` and plots will be saved to `plots` directory
9. Run `python3 src/amdahl.py <cluster1> <cluster2> ... <clusterN>` and plots will be saved to `plots` directory
10. Run `python3 src/gustaf.py <cluster1> <cluster2> ... <clusterN>` and plots will be saved to `plots` directory