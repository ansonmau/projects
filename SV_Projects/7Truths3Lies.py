import random
from time import sleep


def Scramble(dict):
    dictList = list(dict)
    random.shuffle(dictList)
    return dictList


def PrintDict(dictList):
    for i in range(len(dictList)):
        print("{}. {}".format(i+1, dictList[i]))
    return


def main():
    dict = {  # dictionary for the 7 truths and 3 lies
        "I once owned 3 cats at the same time": False,
        "I am an only child": False,
        "I go to a cottage every summer with my family": False,
        "I have reached RCM Level 10 piano": True,
        "I am currently getting a Bachelor's in Computer Science": True,
        "My favourite type of food is Japanese": True,
        "I have reached top 1 percent of League of Legends players": True,
        "My favourite sport is badminton": True,
        "I once ate a live cockroach": True,
        "I love snowboarding and skiing": True
    }

    lives = 7  # lives counter
    lies_found = 0  # count the num of lies they have guessed
    # get the current edition of dict (changes everytime we run the program)
    currDict = Scramble(dict)

    print("Anson's 7 truths and 3 lies!")
    while lives > 0 and lies_found < 3:
        # list out the scrambled version of dict
        PrintDict(currDict)
        validChoice = False
        choice = 0

        print("\n{} lives left".format(lives))

        # checks if the input is valid
        while not validChoice:
            choice = input(
                "Guess the lie (1 - {}): ".format(len(currDict)))
            try:
                choice = int(choice) - 1
                if (choice >= 0 and choice < len(currDict)):
                    validChoice = True
                else:
                    print("Invalid selection.")
            except:
                print("Invalid selection.")

        if not (dict[currDict[choice]]):
            print("Correct! That was a lie.")
            currDict.pop(choice)
            lies_found += 1
        else:
            print("Nope! That was true.")
            lives -= 1
            if lives == 0:
                break

        sleep(1)

    if (lives == 0):
        print("You lose :(")
        print("The lies were: ")
        for key in dict:
            if dict[key] == False:
                print(key)
    else:
        print("Congratz, you won with {} lives remaining!".format(lives))

    return


if __name__ == "__main__":
    main()
