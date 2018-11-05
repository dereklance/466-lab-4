# Derek Lance, dlance@calpoly.edu
# Ian Battin, ibattin@calpoly.edu

import sys, parse, random, math
from operator import add
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

def euclidianDistance(pointA, pointB):
	total = sum((pointA[index] - pointB[index]) ** 2 for index in range(len(pointA)))
	return math.sqrt(total)

def findCentroid(data):
	centroid = [0] * len(data[0])

	for dataPoint in data:
		for index, value in enumerate(dataPoint):
			centroid[index] += value

	return [value / len(data) for value in centroid]

def findFurthestPoint(data, centroids):
	maxDistance = 0
	maxPoint = []

	for dataPoint in data:
		distance = sum(euclidianDistance(dataPoint, centroid) for centroid in centroids)

		if distance > maxDistance:
			maxDistance = distance
			maxPoint = dataPoint

	return maxPoint

def findClosestCluster(dataPoint, centroids):
	minDistance = sys.maxsize
	minIndex = -1

	for index, centroid in enumerate(centroids):
		distance = euclidianDistance(centroid, dataPoint)
		if distance < minDistance:
			minDistance = distance
			minIndex = index

	return minIndex

def selectInitialCentroids(data, numClusters):
	centroidOfDataset = findCentroid(data)
	initialCentroids = []
	removedData = []

	furthestPoint = findFurthestPoint(data, [centroidOfDataset])
	initialCentroids.append(furthestPoint)
	data.remove(furthestPoint)
	removedData.append(furthestPoint)

	for index in range(numClusters - 1):
		furthestPoint = findFurthestPoint(data, initialCentroids)
		initialCentroids.append(furthestPoint)
		data.remove(furthestPoint)
		removedData.append(furthestPoint)

	data.extend(removedData)

	return initialCentroids

# def isStoppingCondition(centroids, oldCentroids):
# 	return all(centroid == oldCentroid for centroid, oldCentroid in 

def kMeansClustering(data, numClusters):
	centroids = selectInitialCentroids(data, numClusters)

	stopCondition = False
	while not stopCondition:
		s = [[0] * len(data[0])] * numClusters
		num = [0] * numClusters
		cl = [[] for i in range(numClusters)]

		for dataPoint in data:
			cluster = findClosestCluster(dataPoint, centroids)
			cl[cluster].append(dataPoint)
			s[cluster] = list(map(add, s[cluster], dataPoint))
			num[cluster] += 1

		oldCentroids = list(centroids)
		for index in range(numClusters):
			centroids[index] = [value / num[index] for value in s[index]]

		if oldCentroids == centroids:
			return cl, centroids

	return None

def showScatterPlot3D(clusters):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k']
	markers=['o', '^', 's', 'x', '+', '*', 'd']

	for index, cluster in enumerate(clusters):
		[xs, ys, zs] = zip(*cluster)
		ax.scatter(xs, ys, zs, c=colors[index], marker=markers[index])

	plt.savefig("matplotlib.png")

def showScatterPlot2D(clusters):
	colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k']
	markers=['o', '^', 's', 'x', '+', '*', 'd']

	for index, cluster in enumerate(clusters):
		[xs, ys] = zip(*cluster)
		plt.scatter(xs, ys, c=colors[index], marker=markers[index])

	plt.savefig("matplotlib.png")

def findDistanceStats(cluster, centroid):
	maxDistance = minDistance = euclidianDistance(cluster[0], centroid)
	totalDistance = 0
	sse = 0

	for dataPoint in cluster:
		distance = euclidianDistance(dataPoint, centroid)
		
		if distance > maxDistance:
			maxDistance = distance
		if distance < minDistance:
			minDistance = distance

		totalDistance += distance
		sse += distance ** 2

	return {
		'max': maxDistance,
		'min': minDistance,
		'avg': totalDistance / len(cluster),
		'sse': sse
	}

def outputClusterData(clusters, centroids):
	for index, (cluster, centroid) in enumerate(zip(clusters, centroids)):
		print(f'Cluster {index}:')
		print(f'Center: {", ".join(map(str, centroid))}')
		stats = findDistanceStats(cluster, centroid)
		print(f'Max Dist. to Center: {stats["max"]}')
		print(f'Min Dist. to Center: {stats["min"]}')
		print(f'Avg Dist. to Center: {stats["avg"]}')
		print(f'SSE: {stats["sse"]}')
		print(f'{len(cluster)} Points:')

		for dataPoint in cluster:
			print(', '.join(map(str, dataPoint)))
		print()

def showScatterPlot(clusters):
	dimension = len(clusters[0][0])

	# only show scatter plot if data is 2d or 3d
	if dimension > 3:
		return

	showScatterPlot2D(clusters) if dimension == 2 else showScatterPlot3D(clusters)

def main():
	data = parse.csv(sys.argv[1])
	numClusters = int(sys.argv[2])
	clusters, centroids = kMeansClustering(data, numClusters)
	outputClusterData(clusters, centroids)
	showScatterPlot(clusters)

if __name__ == '__main__':
  #orig_stdout = sys.stdout
  #f = open(sys.argv[3], 'w')
  #sys.stdout = f

  main()

  #sys.stdout = orig_stdout
  #f.close()