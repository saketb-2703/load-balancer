clus=$1

input_file="data/inputs.txt"

while IFS= read -r x; 
do
instance=$(python3 src/instance_finder.py $clus $x)

docker build -t trial-$clus cluster$clus/
docker run final-$clus-$instance $instance $x
done < "$input_file"