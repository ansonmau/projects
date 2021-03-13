import csv
import openpyxl

VERSION = 1.3
PL_START_ROW = 12
PL_END_ROW = 150
QB_NAME_COL = 29
QB_QUANTITY_COL = 12
QB_PRICE1_COL = 25
QB_PRICE2_COL = 26
PL_NAME_COL_LIST = ['B', 'G', 'L', 'Q', 'V', 'AA', 'AF', 'AK', 'AP']
PL_PRICE1_COL_LIST = ['D', 'I', 'N', 'S', 'X', 'AC', 'AH', 'AM', 'AR']
PL_PRICE2_COL_LIST = ['E', 'J', 'O', 'T', 'Y', 'AD', 'AI', 'AN', 'AS']
print("VERSION={}".format(VERSION))
while True:
    try:
        csvFile = csv.reader(open("pricelist.CSV", 'r'))
        print("CSV loaded successfully")
        break
    except:
        print("[pricelist.csv] does not exist in current directory")
        input("press enter to try again...")
while True:
    try:
        wbName = input("Enter name of price list that needs to be updated: ")
        wbName += ".xlsx"
        wb = openpyxl.load_workbook(wbName)
        pricelist = wb["PriceList"]
        if str(pricelist['B11'].value).strip() != "ITEM NAME" or str(pricelist['D11'].value).strip() != "PRICE" or str(pricelist['E11'].value).strip() != "PRICE":
            print("the given price list does not match proper format")
        else:
            print("[{}] opened successfully".format(wbName))
            break
    except:
        print("File does not exist")
found_items = []
notfound_items = []
dup_items = []
found_total = 0
total_items = 0
total_actions = 0
total_csv_items = 0
for l in PL_NAME_COL_LIST:
    for x in pricelist[l][PL_START_ROW:PL_END_ROW]:
        n = str(x.value).strip()
        if n != '' and n != "None":
            total_items += 1
csvFile = list(csvFile)[1:]
for row in csvFile:  # iterate through each row of csv file
    total_csv_items += 1
    if len(row[QB_NAME_COL]) > 0 and (row[QB_PRICE1_COL] != '' or row[QB_PRICE2_COL] != ''):
        total_actions += 1
        # set name to Price List Name column of the row.
        qb_name = str(row[QB_NAME_COL]).strip()
        found = False
        for col_letter_index in range(len(PL_NAME_COL_LIST)):
            itemNames = pricelist[PL_NAME_COL_LIST[col_letter_index]]
            prices1 = pricelist[PL_PRICE1_COL_LIST[col_letter_index]]
            prices2 = pricelist[PL_PRICE2_COL_LIST[col_letter_index]]
            itemNames = itemNames[PL_START_ROW:PL_END_ROW]
            prices1 = prices1[PL_START_ROW:PL_END_ROW]
            prices2 = prices2[PL_START_ROW:PL_END_ROW]
            for i in range(len(itemNames)):
                name = str(itemNames[i].value).strip().lstrip()
                if name != "None" and name != '' and name not in found_items:
                    if str(name) == str(qb_name):
                        found_total += 1
                        price1 = prices1[i].value
                        price2 = prices2[i].value
                        qb_price1 = row[QB_PRICE1_COL]
                        qb_price2 = row[QB_PRICE2_COL]
                        if "/" in qb_price1:
                            qb_price1 = qb_price1[:qb_price1.index("/")]
                        if "/" in qb_price2:
                            qb_price2 = qb_price2[:qb_price2.index("/")]
                        qb_quantity = row[QB_QUANTITY_COL]
                        if int(qb_quantity) <= 0:
                            if str(price1).lower() != 'call' or str(price2).lower() != 'call':
                                print("---[{}]---".format(name))
                                prices1[i].value = 'call'
                                prices2[i].value = 'call'
                                print(
                                    "prices changed to \'call\' (NO STOCK, BOTH PRICES)\n")
                        elif str(price1) != str(qb_price1) or str(price2) != str(qb_price2):
                            print("---[{}]---".format(name))
                            if qb_price1 != '' and str(price1) != str(qb_price1):
                                prices1[i].value = float(qb_price1)
                                print("PRICE1: ${} changed to ${} (stock: {})".format(
                                    price1, qb_price1, qb_quantity))
                            if qb_price2 != '' and str(price2) != str(qb_price2):
                                prices2[i].value = float(qb_price2)
                                print("PRICE2: ${} changed to ${} (stock: {})".format(
                                    price2, qb_price2, qb_quantity))
                            print()
                        found_items.append(name)
                        found = True
                if found:
                    break
            if found:
                break
        if not found and qb_name in found_items:
            dup_items.append(qb_name)
        elif not found:
            notfound_items.append(qb_name)
        found_curr = 0

print("[  {} / {}  ]".format(found_total, total_items))
if len(notfound_items) > 0:
    print("Could not find (not on outgoing price list): ")
    for i in notfound_items:
        print(i)
if len(dup_items) > 0:
    print("Duplicate Items in QuickBook (MUST FIX!): ")
    for i in dup_items:
        print(i)
print("[ {} / {} ] (ignore) ".format(total_actions, total_csv_items))
saved = False
while not saved:
    saveName = input("save updated price list as: ")
    saveName += '.xlsx'
    try:
        wb.save(saveName)
        print("saved successfully as {}".format(saveName))
        saved = True
    except:
        print("(!!!) could not save! (!!!)")
input("press enter to exit")
