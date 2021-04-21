import random
from os import system
from time import sleep
from colorama import init


def main():

    count = [0 for i in range(10)]

    while True:
        num = random.randint(1, 10)
        count[num-1] += 1
        for i in range(10):
            print("{}: {}".format(i+1, count[i]))
        print('\033[A' * 11)

    return


if __name__ == "__main__":
    init()
    main()
