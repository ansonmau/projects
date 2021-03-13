import csv
import openpyxl

PL_STARTING_ROW = 12
QB_NAME_COL = 3
QB_QUANTITY_COL = 12
QB_PRICE_COL = 25
csvFile = csv.reader(open("test.CSV"))
csvList = list(csvFile)
wb = openpyxl.load_workbook("pricelist.xlsx")
pricelist = wb["PriceList"]
itemNames = pricelist['B']
prices = pricelist['D']
itemNames = itemNames[PL_STARTING_ROW:] #splice list
prices = prices[PL_STARTING_ROW:]
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


# for i in range(len(itemNames)):
# 	name = itemNames[i].value
# 	if name != None:
# 		name = str(name).lower()
# 		print("searching for: {}".format(name))
# 		price = prices[i].value
# 		for row in csvFile:
# 			print(row[3])
# 			if len(row[3])>0 and name in row[3].lower():
# 				cName = row[3]
# 				print(cName)

# for i in range(len(itemNames)):
# 	if name != None:
# 		print("{} : {} : {}".format(name, price, cName))