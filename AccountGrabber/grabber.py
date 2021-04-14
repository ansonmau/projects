import os


def main():

    accountFile = open(
        "F:\\Users\\AnsonM\\Documents\\GitHub\\projects\\assets\\accounts.txt", "r")

    accountNumber = 1
    for line in accountFile:
        accountData = line.split(":")

        # first item is the username
        print("[{}]. {}".format(accountNumber, accountData[0]))

        accountNumber += 1

    return


if __name__ == "__main__":
    main()
