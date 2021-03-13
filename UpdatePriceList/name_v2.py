import csv
import openpyxl

PL_STARTING_ROW = 12
QB_NAME_COL = 3
csvFile = csv.reader(open("test.CSV"))
csvList = list(csvFile)
wb = openpyxl.load_workbook("pricelist.xlsx")
pricelist = wb["PriceList"]
itemNames = pricelist['F']
itemNames = itemNames[PL_STARTING_ROW:] #splice list
for i in itemNames:
	if len(i)==0:
		del i
found = 0
for row in csvList: # iterate through each row of csv file
	qb_name = row[QB_NAME_COL] # set name to third column of the row. 
	qb_name = str(qb_name).lower()
	for i in range(len(itemNames)):
		name = str(itemNames[i].value).lower().strip()
		if name == qb_name[(len(qb_name) - len(name)):]:
			found += 1
			row[-1] = itemNames[i].value
			print("added {} to {}".format(itemNames[i].value, csvList[0][-1]))
writer = csv.writer(open("new.CSV", 'w'), 'unix')
writer.writerows(csvList)

print("found: {}".format(found))

try:
	wb.save('np.xlsx')
	print("saved successfully")
except:
	print("could not save")