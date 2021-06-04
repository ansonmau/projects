import random


def ChooseWord(user_choice):
    if user_choice == 1:
        word = random.choice(movies_list)
    elif user_choice == 2:
        word = random.choice(games_list)
    elif user_choice == 3:
        word = random.choice(songs_list)
    return word


def printGame(word, user_guesses):
    complete = True
    output_string = ""

    for letter in word:
        if letter == " ":
            output_string += "   "
        elif letter.lower() not in user_guesses:
            output_string += "_ "
            complete = False
        else:
            output_string += "{} ".format(letter)

    print(output_string + "\n")

    return complete


movies_list = [
    "Godzilla vs Kong",
    "The Matrix",
    "Bee Movie",
    "Inception",
    "The Martian",
    "Interstellar",
    "It",
    "Coroline",
    "Avengers End Game",
    "Parasite"
]

games_list = [
    "League of Legends",
    "Counter Strike",
    "Grand Theft Auto",
    "Overwatch",
    "Minecraft",
    "Fortnite",
    "Left 4 Dead",
    "Portal",
    "Smash Bros"
]

songs_list = [
    "Payphone",
    "Radioactive",
    "Thrift Shop",
    "Wide Awake",
    "Call Me Maybe",
    "Counting Stars",
    "Wake Me Up"
]

user_guesses = []

lives = 6

intro = "Welcome to hangman! Choose a topic.\n[1] Movies\n[2] Games\n[3] Songs\n"
while True:
    user_choice = int(input(intro))
    if user_choice not in [1, 2, 3]:
        print("Please enter a valid choice")
        continue
    break

word = ChooseWord(user_choice)

while lives > 0 and not printGame(word, user_guesses):
    print("Lives left: {} \nYour guesses: {}".format(
        lives, ", ".join(user_guesses)))
    while True:
        guess = input("Enter your guess: ")

        if guess in user_guesses:
            print("You have already guessed {}".format(guess))
        elif len(guess) > 1:
            print("You can only guess one letter at a time.")
        else:
            user_guesses.append(guess.lower())
            print()
            if guess.lower() not in word.lower():
                lives -= 1
                print("{} is NOT in the word :(".format(guess))
            else:
                print("{} is in the word!".format(guess))

            print("\n\n")
            break

if lives > 0:
    print("Congrats! You won with {} lives left!".format(lives))
else:
    print("You lost :( Bob was hanged.\nThe word was:")

    for letter in word:
        user_guesses.append(letter.lower())
    printGame(word, user_guesses)
