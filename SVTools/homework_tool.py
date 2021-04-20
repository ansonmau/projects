import pyperclip
import os


def SpecialPrint(message):
    if len(message) > 80:
        border = '-' * 80
    else:
        border = '-' * len(message)

    print("{}\n{}\n{}".format(border, message, border))


def main():

    os.system('cls')

    SpecialPrint("Homework Text Generator. Enter nothing to finish.")

    final_string = ""

    count = 1

    final_string += ".:: {} ::.".format(input("Title: "))

    keep_going = True

    while keep_going:
        #   get the input as it's own thing so i can check if it's ''
        user_input = input("[{}]: ".format(count))

        #   check if it's ''
        if len(user_input) == 0:
            keep_going = False
        else:
            sentence = "[{}]: {}".format(count, user_input)
            final_string += " || {}".format(sentence)
            count += 1

    #   add in class replit link if i want to
    replit = input("Class Replit: ")

    if not len(replit) == 0:
        final_string += " || Replit for this week's class: {}".format(replit)

    #   add homework answers if i want to
    hw_sol = input("Homework solution Replit: ")

    if not len(hw_sol) == 0:
        final_string += " || My solution for the homework (to use if you are stuck): {}"

    final_string += " || If you have any questions, message me on the SV website."

    SpecialPrint(final_string)
    print("(Text is copied to clipboard)")
    pyperclip.copy(final_string)

    return


if __name__ == "__main__":
    main()
