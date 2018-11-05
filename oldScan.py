# Derek Lance, dlance@calpoly.edu
# Ian Battin, ibattin@calpoly.edu

import parse, sys
from kmeans import euclidianDistance

def findDistanceMatrix(data):
	return [
		[euclidianDistance(dataPointA, dataPointB) for dataPointB in data]
		for dataPointA in data
	]

def findClosePoints(data, distanceMatrix, epsilon):
	closePoints = []

	for i, distances in enumerate(distanceMatrix):
		points = []
		for j ,(point, distance) in enumerate(zip(data, distances)):
			if distance <= epsilon:
				points.append(j)
		closePoints.append(points)

	return closePoints

# def findCluster(data, index, closePoints, isVisited, epsilon, numPoints):
# 	cluster = []
# 	point = data[index]
# 	isCorePoint = len(closePoints[index] >= numPoints)

# 	if isCorePoint:
# 		if isVisited[index] == 0:
# 			cluster.append(point)
# 			isVisited[index] = 1
	

def union(S, neighbors):
	for neighbor in neighbors:
		if neighbor not in S:
			S.append(neighbor)

def findClusters(labels, numClusters):
	clusters = [[] for x in range(numClusters)]
	for index, clusterNum in enumerate(labels):
		clusters[clusterNum].append(index)
	filter(lambda cluster: len(cluster), clusters)

def dbscan(data, epsilon, minPoints):
	numClusters = -1
	labels = [None] * len(data)
	distanceMatrix = findDistanceMatrix(data)
	closePoints = findClosePoints(data, distanceMatrix, epsilon)

	for index, point in enumerate(data):
		if labels[index] is not None:
			continue
		neighbors = closePoints[index]
		if len(neighbors) < minPoints:
			labels[index] = -1
			continue
		numClusters += 1
		labels[index] = numClusters
		S = list(neighbors)
		S.remove(index)
		for nIndex, neighbor in enumerate(S):
			if labels[nIndex] == -1:
				labels[nIndex] = numClusters
			if labels[nIndex] is not None:
				continue
			labels[nIndex] = numClusters
			neighbors = closePoints[nIndex]
			if len(neighbors) >= minPoints:
				union(S, neighbors)

	return labels



# args: <filename> <epsilon> <numPoints>
def main():
	data = parse.csv(sys.argv[1])
	epsilon = float(sys.argv[2])
	numPoints = int(sys.argv[3])

	labels = dbscan(data, epsilon, numPoints)
	print(labels)

if __name__ == '__main__':
	main()