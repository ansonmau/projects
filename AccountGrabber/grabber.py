import pyperclip
from os import system
from vars import path_accounts_file


def main():
    system('cls')

    accountFile = open(path_accounts_file, "r")

    accountData = []
    accountNumber = 0
    for line in accountFile:
        # remove the \n at the end
        line = line.strip()

        accountData.append(line.split(":"))

        # print out the ign and the number option next to it
        print("[{:2}] {}".format(accountNumber+1,
                                 accountData[accountNumber][0]))

        accountNumber += 1

    choice = input("#: ")

    # make sure the choice is valid
    while int(choice) not in range(1, len(accountData)+1):
        print("Enter smthn 1 - {}".format(len(accountData)))
        choice = input("#: ")

    # get the choice in terms of indices and convert to int
    choice = int(choice) - 1

    username = accountData[choice][1]
    password = accountData[choice][2]

    pyperclip.copy(username)
    input("::> Username copied. Press enter to copy password.")

    pyperclip.copy(password)
    print("::> Password copied.")

    return


if __name__ == "__main__":
    main()
