def csv(filename):
	with open(filename, 'r') as file:
		lines = file.read().strip().split('\n')
		unusedColumnIndex = lines[0].strip().split(',')
		print(unusedColumnIndex)

		for line in lines:
			attributes = line.strip().split(',')