import pyperclip
from time import sleep
from os import system
from vars import path_accounts_file

# Constants
DIV = "-" * 70
IND_IGN = 0
IND_RANK = 1
IND_BAN = 2
IND_USER = 3
IND_PASS = 4


def getRank(string):

    if len(string) < 2:
        rank = "Unranked"
    else:
        rank_list = {
            'D': 'Diamond',
            'P': 'Platinum',
            'G': 'Gold',
            'S': 'Silver',
            'B': 'Bronze',
            'I': 'Iron'
        }
        rank_letter = string[0]
        rank_division = string[1]
        rank_tier = rank_list[rank_letter]
        rank = "{} {} {}".format(rank_tier, rank_division, string[2:])

    return rank


def updateInfo(accountData):
    # boolean to check if any data was actually changed.
    change = True

    try:
        print("UPDATE...")

        account_num = int(input("Account #: "))

        # numbers are +1 from actual index
        account_num -= 1

        print("ign: {}".format(accountData[account_num][IND_IGN]))

        print("[1] Rank  [2] Ban")
        choice = input("> ")

        if choice == "1":
            new_rank = input("Example: s3\nBlank = unranked\nNew rank: ")
            accountData[account_num][IND_RANK] = new_rank.upper()
        elif choice == "2":
            new_ban = input("Banned until: ")
            if ',' in new_ban:
                print("can't have ','")
            else:
                accountData[account_num][IND_BAN] = new_ban
        else:
            print("Bad input.")
            change = False
    except:
        print("ERROR! Aborting.")
        change = False

    if change:
        accountFile = open(path_accounts_file, "w")

        for account in accountData:
            line = ",".join(account)
            accountFile.write(line + "\n")

        print("Updated!")

        accountFile.close()

    return


def GetAccountData():
    accountFile = open(path_accounts_file, "r+")

    accountData = []

    for line in accountFile:
        # remove the \n at the end
        line = line.strip()

        accountData.append(line.split(","))

        rank = getRank(accountData[-1][IND_RANK])

        ban = accountData[-1][IND_BAN]
        if ban:
            ban = "> Banned until {}".format(ban)

        # print out the ign and the number option next to it
        print("[{:2}] {:15} | {} {}".format(len(accountData),
                                            accountData[-1][IND_IGN],
                                            rank, ban))

    accountFile.close()

    return accountData


def reset(sec):
    sleep(sec)
    system('cls')
    GetAccountData()
    return


def main():
    RUN = True

    system('cls')

    while RUN:

        accountData = GetAccountData()

        while True:
            choice = input("#: ")

            if not choice.isdecimal():
                if choice in {'x', 'exit', ''}:
                    RUN = False
                    print("Goodbye.")
                    break
                elif choice == "update":
                    updateInfo(accountData)
                    reset(1)
                    continue
                else:
                    print("Bad input.")
                    reset(1)
            else:
                if int(choice) not in range(1, len(accountData)+1):
                    print("Enter smthn 1 - {}".format(len(accountData)))
                else:
                    break

        if RUN:
            # get the choice in terms of indices and convert to int
            choice = int(choice) - 1

            # the first and last values are always going to be user then pass (in case I add other things)
            username = accountData[choice][-2]
            password = accountData[choice][-1]

            pyperclip.copy(username)
            input("::> Username copied. Press enter to copy password.")

            pyperclip.copy(password)
            print("::> Password copied.")
            sleep(1)
            system('cls')

    return


if __name__ == "__main__":
    main()
