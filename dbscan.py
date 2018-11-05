# Derek Lance, dlance@calpoly.edu
# Ian Battin, ibattin@calpoly.edu

import parse, sys
from kmeans import euclidianDistance, findCentroid, findDistanceStats, outputClusterData
import matplotlib.pyplot as plt

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

def findClusters(data, labels, numClusters):
	clusters = [[] for x in range(numClusters)]
	outliers = []

	for index, clusterNum in enumerate(labels):
		if clusterNum == -1:
			outliers.append(data[index])
		else:
			clusters[clusterNum].append(data[index])
	return clusters, outliers

def dbscan(data, epsilon, minPoints):
	numClusters = -1
	labels = [None] * len(data)
	distanceMatrix = findDistanceMatrix(data)
	closePoints = findClosePoints(data, distanceMatrix, epsilon)

	for index, point in enumerate(data):
		if labels[index] is not None:
			continue
		neighbors = closePoints[index]
		neighbors.remove(index)
		if len(neighbors) < minPoints:
			labels[index] = -1
			continue

		numClusters += 1
		labels[index] = numClusters

		for neighbor in neighbors:
			if labels[neighbor] == -1:
				labels[neighbor] = numClusters
			elif labels[neighbor] is None:
				labels[neighbor] = numClusters
				nNeighbors = closePoints[neighbor]
				if len(nNeighbors) >= minPoints:
					union(neighbors, nNeighbors)

	return findClusters(data, labels, numClusters + 1)

def showScatterPlot3D(clusters, outliers):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	colors = ['b', 'g', 'c', 'm', 'y', 'k', 'b', 'g', 'c', 'm', 'y', 'k']
	markers=['o', '^', 's', '+', '*', 'd', '^', 's', '+', '*', 'd', 'o']

	for index, cluster in enumerate(clusters):
		[xs, ys, zs] = zip(*cluster)
		ax.scatter(xs, ys, zs, c=colors[index], marker=markers[index])

	if len(outliers) > 0:
		print(outliers)
		[xs, ys, zs] = zip(*outliers)
		ax.scatter(xs, ys, zs, c='r', marker='x')

	plt.savefig("matplotlib.png")

def showScatterPlot2D(clusters, outliers):
	colors = ['b', 'g', 'c', 'm', 'y', 'k', 'b', 'g', 'c', 'm', 'y', 'k']
	markers=['o', '^', 's', '+', '*', 'd', '^', 's', '+', '*', 'd', 'o']

	for index, cluster in enumerate(clusters):
		[xs, ys] = zip(*cluster)
		plt.scatter(xs, ys, c=colors[index], marker=markers[index])
	if len(outliers) > 0:
		[xs, ys] = zip(*outliers)
		plt.scatter(xs, ys, c='r', marker='x')

	plt.savefig("matplotlib.png")

def showScatterPlot(clusters, outliers):
	dimension = len(clusters[0][0])

	# only show scatter plot if data is 2d or 3d
	if dimension > 3:
		return

	showScatterPlot2D(clusters, outliers) if dimension == 2 else showScatterPlot3D(clusters, outliers)

def outputClusterData(clusters, centroids):
	for index, (cluster, centroid) in enumerate(zip(clusters, centroids)):
		print(f'Cluster {index}:')
		print(f'Center: {", ".join(map(str, centroid))}')
		stats = findDistanceStats(cluster, centroid)
		print(f'Max Dist. to Center: {stats["max"]}')
		print(f'Min Dist. to Center: {stats["min"]}')
		print(f'Avg Dist. to Center: {stats["avg"]}')
		print(f'Sum Squared Error: {stats["sse"]}')
		print(f'{len(cluster)} Points:')

		for dataPoint in cluster:
			print(', '.join(map(str, dataPoint)))
		print()

def outputOutlierData(outliers, numDataPoints):
	print('Outliers:')
	print('Percentage of data:', round(len(outliers) / numDataPoints * 100, 2))
	print(len(outliers), 'Points:')
	for outlier in outliers:
		print(', '.join(map(str, outlier)))

# args: <filename> <epsilon> <numPoints>
def main():
	data = parse.csv(sys.argv[1])
	epsilon = float(sys.argv[2])
	numPoints = int(sys.argv[3])

	clusters, outliers = dbscan(data, epsilon, numPoints)
	centroids = [findCentroid(cluster) for cluster in clusters]
	outputClusterData(clusters, centroids)
	outputOutlierData(outliers, len(data))

	showScatterPlot(clusters, outliers)

if __name__ == '__main__':
  #orig_stdout = sys.stdout
  #f = open(sys.argv[4], 'w')
  #sys.stdout = f

  main()

  #sys.stdout = orig_stdout
  #f.close()