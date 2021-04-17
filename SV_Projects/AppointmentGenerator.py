import random

makingAppointment = True

while makingAppointment:

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    month_num = random.randint(1, 12)

    month_word = months[month_num]

    if month_num == 2:
        day = random.randint(1, 28)
    elif month_num in {1, 3, 5, 7, 8, 10, 12}:
        day = random.randint(1, 31)
    else:
        day = random.randint(1, 30)

    year = random.randint(2021, 2121)

    print("Your appointment is on {} {}, {}".format(month_word, day, year))

    again = input("Would you like to make another appointment? (Y/N): ")

    if again == "N" or again == 'n':
        makingAppointment = False

    print("\n")
