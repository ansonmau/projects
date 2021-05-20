import random
from os import system
py


def main():
    system('cls')

    num = random.randint(1, 1000)
    print("({})".format(num))

    user_guess = int(input("[1] Guess the number: "))

    if user_guess == num:
        print("Wow you are so lucky! {} is the correct number.".format(num))
    elif user_guess > num:
        print("Too big!")
        prev_diff = user_guess - num
    else:
        print("Too small!")
        prev_diff = num - user_guess

    guess_count = 2
    while not user_guess == num:
        user_guess = int(input("[{}] Guess the number: ".format(guess_count)))

        if user_guess == num:
            curr_diff = 0
            print("You win! {} is the correct number. ".format(num))
        elif user_guess > num:
            curr_diff = user_guess - num
            if curr_diff == prev_diff:
                print("Not hotter or colder...")
            elif curr_diff > prev_diff:
                print("Colder! :(")
            else:
                print("Hotter! :)")
        else:
            curr_diff = num - user_guess
            if curr_diff == prev_diff:
                print("Not hotter or colder...")
            elif curr_diff > prev_diff:
                print("Colder! :(")
            else:
                print("Hotter! :)")

        prev_diff = curr_diff
        guess_count += 1

    return


if __name__ == "__main__":
    main()
