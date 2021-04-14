import pyperclip


def SpecialPrint(message):

    if len(message) > 80:
        border = '-' * 80
    else:
        border = '-' * len(message)

    print("{}\n{}\n{}".format(border, message, border))


def main():

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

    final_string += " || If you have any questions, message me on the SV website."

    SpecialPrint(final_string)
    print("(Text is copied to clipboard)")
    pyperclip.copy(final_string)

    return


if __name__ == "__main__":
    main()
