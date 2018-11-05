# Derek Lance, dlance@calpoly.edu
# Ian Battin, ibattin@calpoly.edu

import parse, sys
from hclustering import Cluster, calculate_distance_matrix

def dbscan(data, epsilon, numPoints):
	print(data, epsilon, numPoints)

# args: <filename> <epsilon> <numPoints>
def main():
	data = parse.csv(sys.argv[1])
	epsilon = float(sys.argv[2])
	numPoints = int(sys.argv[3])

	dbscan(data, epsilon, numPoints)

if __name__ == '__main__':
	main()