import random
from os import system

system('cls')

points = [0, 0, 0, 0, 0, 0]
GAMEOVER = False
roundNum = 0
setNum = 0
points_to_win = 10


def roll():
    player_choices = []

    for i in range(6):
        player_choices.append(random.randint(1, 6))

    return player_choices


def checkWin(scores, winningPoints):
    winners = []
    p = 0
    while p < len(scores):
        if scores[p] == winningPoints:
            winners.append(p+1)
        p += 1

    if winners:
        print("\nGame over! The winners are:")
        for playerNum in winners:
            print("Player {}".format(playerNum))
        return True

    return False


def printScoreboard(scores):
    i = 0
    print("-----------SCOREBOARD-----------")
    while i < len(scores)/2:
        print("|  Player {}: {:<4}Player {}: {:<4}|".format(
            i + 1, scores[i], i + 4, scores[i + 3]))
        i += 1
    print("--------------------------------")

    return


def printTitle(title, num):
    if num == 1:
        print("----------{:^18}----------".format(title))
    else:
        print("<<<<<<<<<<{:^18}>>>>>>>>>>".format(title))

    return


introMessage = "Welcome to Anson's dice game! In this game, each player tries to roll the round number to score a point. First one to " + \
    str(points_to_win) + " wins!\nPress enter to begin."

input(introMessage)

roundCounter = 0
roundCounter_end = 1
while not GAMEOVER:
    while roundCounter < roundCounter_end:
        rolls = roll()
        roundNum = (roundNum % 6) + 1
        if roundNum == 1:
            setNum += 1

        print("\n\n")
        printTitle("SET {} | ROUND {}".format(setNum, roundNum), 2)
        print()

        for pNum in range(len(rolls)):
            if rolls[pNum] == roundNum:
                print(
                    "Player {} rolled: {} [ +1 ]".format(pNum+1, rolls[pNum]))
                points[pNum] += 1
            else:
                print("Player {} rolled: {}".format(pNum+1, rolls[pNum]))

        print()
        printScoreboard(points)

        if checkWin(points, points_to_win):
            GAMEOVER = True
            break

        roundCounter += 1
    if not GAMEOVER:
        roundCounter_end = int(input("Enter the number of rounds to run: "))
        roundCounter = 0
