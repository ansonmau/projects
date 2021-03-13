import csv
import openpyxl

key = "Intel 3.0G 1M 800MHz LGA478"

key = key.lower()
occ = {}
rank = {}
csvFile = csv.reader(open("test.csv"))
badChar = [',' , '(' , ')' ,'-']
print("Searching for: {}".format(key))
csvFile = list(csvFile)
for i in range(1,1807):
	name = csvFile[i][4]
	name = name.lower()
	for i in badChar:
		if i in key:
			key = key.replace(i, ' ')
			print(key)
		if i in name:
			name = name.replace(i, ' ')
	if len(name) > 0:
		best_value = 0
		for word in key.split():
			if word in name:
				if name not in occ:
					occ[name] = 1
				else:
					occ[name] += 1

if len(occ) > 0:
	high_val = 0
	for i in occ:
		rank = len(i) - occ[i]
		if occ[i] > high_val:
			best = i 
			high_val = occ[i]

	for item in occ:
		print("{} [common words: {}]".format(item, occ[item]))
	print("BEST: {} [common words: {}]".format(best, occ[best]))
else:
	print("No items found")
		