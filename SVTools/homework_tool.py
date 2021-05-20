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
    replit_class_string = input("Class Replit: ")

    if len(replit_class_string) > 0:
        final_string += " || Replit for this week's class: {}".format(
            replit_class_string)

    #   add homework answers if i want to
    replit_homework_string = input("Homework solution Replit: ")

    if len(replit_homework_string) > 0:
        final_string += " || My solution for the homework (use if stuck): {}".format(
            replit_homework_string)

    final_string += " || If you have any questions, message me on the SV website."

    SpecialPrint(final_string)
    pyperclip.copy(final_string)
    print("(Text is copied to clipboard)")

    return


if __name__ == "__main__":
    main()
