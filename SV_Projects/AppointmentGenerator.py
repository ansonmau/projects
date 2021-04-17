import random

makingAppointment = True

while makingAppointment:

    month = random.randint(1, 12)

    if month == 2:
        day = random.randint(1, 28)
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day = random.randint(1, 31)
    else:
        day = random.randint(1, 30)

    year = random.randint(2021, 2121)

    if month == 1:
        month_word = "January"
    elif month == 2:
        month_word = "February"
    elif month == 3:
        month_word = "March"
    elif month == 4:
        month_word = "April"
    elif month == 5:
        month_word = "May"
    elif month == 6:
        month_word = "June"
    elif month == 7:
        month_word = "July"
    elif month == 8:
        month_word = "August"
    elif month == 9:
        month_word = "September"
    elif month == 10:
        month_word = "October"
    elif month == 11:
        month_word = "November"
    elif month == 12:
        month_word = "December"

    print("Your appointment is on {} {}, {}".format(month_word, day, year))

    again = input("Would you like to make another appointment? (Y/N): ")

    if again == "N" or again == 'n':
        makingAppointment = False

    print("\n")
