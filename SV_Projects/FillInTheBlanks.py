
# Yesterday, I was talking to ____. We talked about how James found a _____! It's insane! He is so lucky he
# just happened to be in ____. He had a ____ on him, though, so it makes sense.

full_string = ""
while True:
    print("Yesterday, I bumped into ____")
    choice = input("[1] Bob\n[2] Nick\n[3] Chris\n")
    if choice == "1":
        blank = "Bob"
    elif choice == "2":
        blank = "Nick"
    elif choice == "3":
        blank = "Chris"
    else:
        print("Enter a number from 1-3")
        continue
    break
full_string += "Yesterday, I bumped into {}.".format(blank)

while True:
    print("\n{} We talked about how James found a ____!".format(full_string))
    choice = input("[1] diamond\n[2] meteorite\n[3] snail\n")
    if choice == "1":
        blank = "diamond"
    elif choice == "2":
        blank = "meteorite"
    elif choice == "3":
        blank = "snail"
    else:
        print("Enter a number from 1-3")
        continue
    break
full_string += " We talked about how James found a {}!".format(blank)

while True:
    print("\n{} It's insane! He is so lucky he just happened to be in ____.".format(
        full_string))
    choice = input("[1] New York\n[2] Toronto\n[3] Antarctica\n")
    if choice == "1":
        blank = "New York"
    elif choice == "2":
        blank = "Toronto"
    elif choice == "3":
        blank = "Antarctica"
    else:
        print("Enter a number from 1-3")
        continue
    break
full_string += " It's insane! He is so lucky he just happened to be in {}.".format(
    blank)

while True:
    print("\n{} He had a ____ on him, though, so I guess it makes sense.".format(
        full_string))
    choice = input("[1] Shovel\n[2] Radar\n[3] Gun\n")
    if choice == "1":
        blank = "shovel"
    elif choice == "2":
        blank = "radar"
    elif choice == "3":
        blank = "gun"
    else:
        print("Enter a number from 1-3")
        continue
    break
full_string += " He had a {} on him, though, so I guess it makes sense.".format(
    blank)

print("\n{}".format(full_string))
