def indexOf(array, value):
	for index, item in enumerate(array):
		if int(item) == value:
			return index
	return -1

def csv(filename):
	with open(filename, 'r') as file:
		lines = file.read().strip().split('\n')
		header = lines[0].strip().split(',')
		unusedIndex = indexOf(header, 0)

		data = []
		for line in lines[1:]:
			attributes = line.strip().split(',')

			if unusedIndex >= 0:
				del attributes[unusedIndex]
			
			data.append([float(value) for value in attributes])

		return data
