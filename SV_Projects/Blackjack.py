import random
from time import sleep


def hit():
    cards = [
        'A',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'J',
        'Q',
        'K',
    ]
    draw = random.choice(cards)
    return draw


def GetTotal(hand):
    total = 0
    card_values = {
        'A': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
    }
    for card in hand:
        total += card_values[card]
    return total


def DrawHand(hand):
    string = ''
    numCards = len(hand)

    for i in range(numCards):
        string += ('+-----+  ')
    string += '\n'

    for i in range(numCards):
        string += ('|     |  ')
    string += '\n'

    for card in hand:
        string += ('|{:^5}|  '.format(card))
    string += '  Value: {}\n'.format(GetTotal(hand))

    for i in range(numCards):
        string += ('|     |  ')
    string += '\n'

    for card in hand:
        string += ('+-----+  ')
    return string


def main():
    PLAY = True
    while PLAY:

        bot_hand = random.randint(15, 23)
        plr_hand = [hit(), hit()]

        print("Your starting hand:\n{}".format(
            DrawHand(plr_hand), GetTotal(plr_hand)))

        # assume they did not hit. Need this var because the if statement after the following loop uses will_hit,
        # and if we start off with >17, it won't know what will_hit is.
        will_hit = 'n'

        while GetTotal(plr_hand) <= 17:
            will_hit = input("hit? (Y/N): ")
            if will_hit == "Y" or will_hit == "y":
                plr_hand.append(hit())
                print("\nYou drew: {}".format(plr_hand[-1]))
                sleep(1)
                print("Your new hand:\n{}".format(
                    DrawHand(plr_hand)))
            else:
                break

        if will_hit == "Y" or will_hit == "y":
            print("You can no longer hit.")

        if GetTotal(plr_hand) <= 21:
            print("\n{:>10}: {}".format("Your total", GetTotal(plr_hand)))
            print("{:>10}: {}".format("Bot total", bot_hand))
            print()
            if bot_hand <= 21:
                if GetTotal(plr_hand) > bot_hand:
                    print("You win!")
                elif GetTotal(plr_hand) < bot_hand:
                    print("You lose :(")
                else:
                    print("It's a tie!")
            else:
                print("The bot went over 21! You win!")
        else:
            print("\nYou went over 21 :( You lose!")

        play_again = input("\nPlay again? (Y/N): ")

        if play_again != "Y" and play_again != "y":
            PLAY = False
        else:
            print("\n")

    return


if __name__ == "__main__":
    main()
