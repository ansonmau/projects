import csv
import openpyxl

PL_STARTING_ROW = 12
QB_NAME_COL = 29
QB_QUANTITY_COL = 12
QB_PRICE_COL = 25
PL_NAME_COL_LIST = ['B', 'F', 'J', 'N', 'R', 'V', 'Z', 'AD', 'AH']
PL_PRICE_COL_LIST = ['D', 'H', 'L', 'P', 'T', 'X', 'AB', 'AF', 'AJ']
csvFile = csv.reader(open("test.CSV", 'r'))
wb = openpyxl.load_workbook("pricelist.xlsx")
pricelist = wb["PriceList"]
found_items = []
found_total = 0
total_items = 0
for l in PL_NAME_COL_LIST:
	for x in pricelist[l][PL_STARTING_ROW:]:
		n = str(x.value).strip()
		if n != '' and n != "None":
			total_items += 1
			print("found ", str(n))
print(total_items)