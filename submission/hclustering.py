# Derek Lance, dlance@calpoly.edu
# Ian Battin, ibattin@calpoly.edu
import sys
import parse
from anytree import Node, RenderTree
from anytree.exporter import JsonExporter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Cluster:
  def __init__(self, uid, data, min_max, distance = 0, children = None):
    self.uid = uid
    self.data = data
    self.min_max = min_max
    self.distance = distance
    self.children = children 
    self.centroid = self.calculate_centroid()

  def __eq__(self, other):
    return self.uid == other.uid

  def get_data_count(self):
    count = 0

    if self.children:
      for child in self.children:
        count += child.get_data_count()
    else:
      return 1

    return count

  def calculate_centroid(self):
    centroid = list()
    for i in range(len(self.data[0])):
      value, count = 0, 0
      for data in self.data:
        value += data[i]
        count += 1
      centroid.append(value / count)
    return centroid

  def normalize(self, data):
    norm = list()
    for i in range(len(data)):
      normed = (data[i] - self.min_max[i][0]) / (self.min_max[i][1] - 
        self.min_max[i][0])
      norm.append(normed)
    return norm

  def distance_to(self, cluster, normalized = False):
    if normalized:
      self_centroid = self.normalize(self.centroid)
      other_centroid = cluster.normalize(cluster.centroid)
    else:
      self_centroid = self.centroid
      other_centroid = cluster.centroid

    total_dist = 0
    for i in range(len(self_centroid)):
      total_dist += pow(self_centroid[i] - other_centroid[i], 2)
    return total_dist

def calculate_distance_matrix(clusters):
  distance_matrix = []
  for i in range(len(clusters)):
    distances = []
    for j in range(len(clusters)):
      if j < i:
        distances.append(clusters[j].distance_to(clusters[i], True))
      elif i == j:
        distances.append(float("inf"))
    distance_matrix.append(distances)

  return distance_matrix

def get_min_distance(distance_matrix, clusters):
  min_dist = float("inf")
  min_clusters = (None, None)
  for row in range(len(distance_matrix)):
    for col in range(len(distance_matrix[row])):
      if distance_matrix[row][col] < min_dist:
        min_dist = distance_matrix[row][col]
        min_clusters = (clusters[row], clusters[col])

  return min_dist, min_clusters

def calculate_min_max(data):
  min_max = list()
  for i in range(len(data[0])):
    min_val = float("inf")
    max_val = -float("inf")
    for j in range(len(data)):
      val = data[j][i]
      min_val = min(min_val, val)
      max_val = max(max_val, val)
    min_max.append((min_val, max_val))
  return min_max

def xml_print_dendrogram(root, indent = 0):
  # Root
  if indent == 0:
    print('<tree height="', root.distance, '">', sep='')
    for child in root.children:
      xml_print_dendrogram(child, indent + 1)
    print('</tree>')
  elif root.children:
    print(indent * '  ', '<node height="', root.distance, '">', sep='')
    for child in root.children:
      xml_print_dendrogram(child, indent + 1)
    print(indent * '  ', '</node>', sep='')
  else:
    print(indent * '  ', '<leaf height="0" data="', root.data[0], '" />', sep='')

def agglomerative_cluster(dataset):
  min_max = calculate_min_max(dataset)

  clusters = []
  for i in range(len(dataset)):
    cluster = Cluster(str(i), [dataset[i], ], min_max, 0, None)
    clusters.append(cluster)

  while(len(clusters) > 1):
    distance_matrix = calculate_distance_matrix(clusters)
    min_distance, min_clusters = get_min_distance(distance_matrix, clusters)
    merged = Cluster(uid = min_clusters[0].uid + min_clusters[1].uid,
                     data = min_clusters[0].data + min_clusters[1].data, 
                     min_max = min_max,
                     distance = min_clusters[0].distance_to(min_clusters[1]),
                     children = [min_clusters[0], min_clusters[1]])

    clusters.remove(min_clusters[0])
    clusters.remove(min_clusters[1])
    clusters.append(merged)

  return clusters

def get_clusters(dendrogram, threshold):
  if dendrogram.distance < threshold:
    return [dendrogram]
  
  clusters = []
  for child in dendrogram.children:
    clusters += get_clusters(child, threshold)

  return clusters

def get_point_clusters(cluster):
  if not cluster.children:
    return [cluster]

  data = []
  for child in cluster.children:
    data += get_point_clusters(child)
  
  return data

def get_min_max_average_distance(cluster):
  point_clusters = get_point_clusters(cluster)
  max_dist, min_dist, total_dist = -float("inf"), float("inf"), 0

  for point in point_clusters:
    distance = point.distance_to(cluster)
    max_dist = max(max_dist, distance)
    min_dist = min(min_dist, distance)
    total_dist += distance

  return min_dist, max_dist, (total_dist / len(point_clusters))

def sse(cluster):
  points = get_point_clusters(cluster)

  sse = 0
  for point in points:
    sse += pow(point.distance_to(cluster), 2)

  return sse

def showScatterPlot2D(clusters):
  colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', \
            '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', \
            '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', \
            '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', \
            '#ffffff', '#000000']
  markers=['.', ',', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', \
           'P', '*', 'h', '+', 'x', 'X']


  for index, cluster in enumerate(clusters):
    points = get_point_clusters(cluster)
    xs = [x.data[0][0] for x in points]
    ys = [y.data[0][1] for y in points]
    plt.scatter(xs, ys, c=colors[index], marker=markers[index])

  plt.savefig("matplotlib.png")
  
def showScatterPlot3D(clusters):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', \
            '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', \
            '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', \
            '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', \
            '#ffffff', '#000000']
  markers=['.', ',', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', \
           'P', '*', 'h', '+', 'x', 'X']


  for index, cluster in enumerate(clusters):
    points = get_point_clusters(cluster)
    xs = [x.data[0][0] for x in points]
    ys = [y.data[0][1] for y in points]
    zs = [z.data[0][2] for z in points]
    ax.scatter(xs, ys, zs, c=colors[index], marker=markers[index])

  plt.savefig("matplotlib.png")

def main():
  dataset = parse.csv(sys.argv[1])
  threshold = None
  if len(sys.argv) >= 3:
    threshold = float(sys.argv[2])

  print("Dendrogram:")
  dendrogram = agglomerative_cluster(dataset)[0]
  xml_print_dendrogram(dendrogram)
  print()

  if threshold:
    clusters = get_clusters(dendrogram, threshold)
    for i, cluster in enumerate(clusters):
      print()
      print("Cluster:", i)
      print("Center:", cluster.centroid)
      min_dist, max_dist, average_dist = get_min_max_average_distance(cluster)
      print("Max Dist. to Center:", max_dist)
      print("Min Dist. to Center:", min_dist)
      print("Avg Dist. to Center:", average_dist)
      points = get_point_clusters(cluster)
      print("SSE:", sse(cluster))
      print(len(points), "Points:")
      for point in points:
        print(point.data[0])

    print()
    print(len(clusters), "clusters total")

    if len(clusters[0].data[0]) == 2:
      showScatterPlot2D(clusters)
    else:
      showScatterPlot3D(clusters)


if __name__ == '__main__':
  #orig_stdout = sys.stdout
  #f = open(sys.argv[3], 'w')
  #sys.stdout = f

  main()

  #sys.stdout = orig_stdout
  #f.close()