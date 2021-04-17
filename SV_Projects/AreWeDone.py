
def main():
    # Method 1
    while True:
        user_input = input("are we done yet?\n")
        if user_input == "yes":
            break

    # Method 2
    loop = True
    while loop:
        user_input = input("are we done yet?\n")
        if user_input == "yes":
            loop = False

    # Method 3
    user_input = input("are we dont yet?\n")
    while not user_input == "yes":
        user_input = input("are we done yet?\n")

    return


if __name__ == "__main__":
    main()
