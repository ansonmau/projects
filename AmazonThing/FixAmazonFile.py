import datetime

COL_QUICKBOOK_ITEM_NAME = 3
COL_QUICKBOOK_MANU_NUM = 22
COL_AMAZON_ORDERID = 2
COL_AMAZON_SKU = 7


def openFiles():
    opened = False

    while not opened:
        amazon_FileName = input("Enter name of Amazon file: ")
        amazon_FileName += ".txt"
        try:
            file_QuickbookData = open("pricelist.csv", "r")
            file_AmazonData = open(amazon_FileName, "r", encoding="UTF-8")
            print("files loaded successfully.")
            opened = True
        except:
            input(
                "Wrong Amazon file name or pricelist.csv is not in the folder. Press enter to try again")

    return file_QuickbookData, file_AmazonData


# Writes an array to a file.
def writeFile(linesArray, fileName):
    str = ""
    opened = False

    while not opened:
        try:
            file = open(fileName, 'w', encoding="UTF-8")
            opened = True
        except:
            input("That file is open! Close it and press enter to try again")

    for line in linesArray:
        # each element is a string that already has \t seperators and \n at the end, so we can simply concatanate(?)
        str += line

    file.writelines(str)
    file.close()

    return


def main():
    # this will be used to store all the items that aren't found
    not_in_price_list = []

    # stores all the order ids and their invoice #
    dict_orderInvoice = {}

    invoiceNum = 0

    # open the files
    file_QuickbookData, file_AmazonData = openFiles()

    # get initial invoice number (+1 for each item added)
    while invoiceNum == 0:
        try:
            invoiceNum = int(input("Enter first invoice number: "))
        except:
            print("You did not enter a number.")

    # convert each file to lists of their lines
    quickbook_All_Lines = file_QuickbookData.readlines()
    amazon_All_Lines = file_AmazonData.readlines()

    # add titles for invoice #, name, and import date to the first (title) line. Append backwards cus we are inserting at 0.
    amazon_All_Lines[0] = "invoice#\tName\timportdate\t" + amazon_All_Lines[0]

    # get each item name in the amazon file, find what it's full name is in the quickbooks file and replace it.
    # start count at the first index because the first line (index 0) is just titles so we can ignore it.
    for amazon_Line_Index in range(1, len(amazon_All_Lines)):
        # this will be used to check if we should add an item to the "can't find it" list
        found = False

        # get the line into an array. The file seperates them using tabs.
        amazon_Line = amazon_All_Lines[amazon_Line_Index].split('\t')

        # get the item name, dubbed SKU.
        amazon_SKU = amazon_Line[COL_AMAZON_SKU]

        for quickbook_Line in quickbook_All_Lines:
            # the values are surrounded by double quotes in the quickbook csv file. we dont want that.
            quickbook_Line = quickbook_Line.replace('"', '')

            # it's a csv file, so seperate them using commas as delimiter
            quickbook_Info = quickbook_Line.split(',')

            # we want both the manu number and the full item name because:
            #   manu num - processors use this as the name in the amazon file
            #   full item name - we want to replace what's in the amazon file with this.
            quickbook_ManuNum = quickbook_Info[COL_QUICKBOOK_MANU_NUM]
            quickbook_ItemName_Full = quickbook_Info[COL_QUICKBOOK_ITEM_NAME]

            # grab what's after the last ':'.
            quickbook_ItemName = (quickbook_ItemName_Full.split(":"))[-1]

            # in the amazon file, processors and sometimes video cards are named by their manu number
            if "Processors" in quickbook_ItemName_Full or "Video Card" in quickbook_ItemName_Full:
                if amazon_SKU == quickbook_ManuNum:
                    found = True

                    # change the name in the current line
                    amazon_Line[COL_AMAZON_SKU] = quickbook_ItemName_Full
                    break
            else:
                if amazon_SKU == quickbook_ItemName:
                    found = True

                    # change the name in the current line
                    amazon_Line[COL_AMAZON_SKU] = quickbook_ItemName_Full
                    break

        # add slots for invoice #, name, and import date to the current line. Append backwards cus we are inserting at 0.
        # strftime formats date to a specific code. %d = day, %m = month, %Y = long year
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        amazon_Line.insert(0, date)
        amazon_Line.insert(0, "Deals2You.CA")

        # get the order id so we can see if the key value pair exists in the orderID-invoice# dict
        amazon_OrderID = amazon_Line[COL_AMAZON_ORDERID]

        if amazon_OrderID in dict_orderInvoice:
            # if it exists, then insert the invoice # to the same as the existing one.
            amazon_Line.insert(0, str(dict_orderInvoice[amazon_OrderID]))
        else:
            # if it doesn't exist, add the key value pair then insert the new invoice # and increment it.
            dict_orderInvoice.update({amazon_OrderID: invoiceNum})
            amazon_Line.insert(0, str(invoiceNum))
            invoiceNum += 1

        # change the entire line in the collection of all the lines and join them using \t.
        amazon_All_Lines[amazon_Line_Index] = "\t".join(
            amazon_Line)

        # if it wasn't found after looping through all quickbook items, add it to the "can't find it" list
        if not found:
            not_in_price_list.append(
                "[Item " + str(amazon_Line_Index) + "] " + amazon_SKU)

    if not_in_price_list:
        print("Could not find the following items in the quickbooks file: ")
        for item in not_in_price_list:
            print("{}".format(item))

    fileName = input("Enter the name of the output file: ")
    fileName += ".txt"

    # call to the writefile function above
    writeFile(amazon_All_Lines, fileName)

    input("press enter to exit")

    return


if __name__ == "__main__":
    main()
