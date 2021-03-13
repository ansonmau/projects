import csv
import openpyxl

PL_STARTING_ROW = 12
QB_NAME_COL = 29
QB_QUANTITY_COL = 12
QB_PRICE_COL = 25
csvFile = csv.reader(open("new.CSV"))
wb = openpyxl.load_workbook("pricelist.xlsx")
pricelist = wb["PriceList"]
itemNames = pricelist['B']
prices = pricelist['D']
itemNames = itemNames[PL_STARTING_ROW:] #splice list
prices = prices[PL_STARTING_ROW:]
found = 0
for row in csvFile: # iterate through each row of csv file
	qb_name = row[QB_NAME_COL] # set name to Price List Name column of the row. 
	for i in range(len(itemNames)):
		name = itemNames[i].value
		if name == qb_name:
			found += 1
			price = prices[i].value
			qb_price = row[QB_PRICE_COL]
			if "/" in qb_price:
				qb_price = qb_price[:qb_price.index("/")]
			print("{} : {} || {} : {}".format(qb_name, qb_price, name, price))
			qb_quantity = row[QB_QUANTITY_COL]
			if qb_quantity == '0' and price != 'call':
				prices[i].value = 'call'
				print("{} changed to {}".format(price, 'call'))
			elif qb_price != '' and str(price) != str(qb_price):
					prices[i].value = float(qb_price)
					print("{} changed to {}".format(price, qb_price))

print("found: {}".format(found))
try:
	saveName = 'NEWPRICELIST.xlsx'
	wb.save(saveName)
	print("saved successfully as {}".format(saveName))
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