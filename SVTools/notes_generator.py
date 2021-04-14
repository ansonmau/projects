import pyperclip
import datetime


def getDay():
    day_num = datetime.datetime.today().weekday()

    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

    day_word = days[day_num]

    return day_word


def getStudents(day):
    # Students lists
    students_tues = ["Ethan"]
    students_wed = ["Jordan", "Kathryn", "James"]
    students_sat = ["Haorui", "Niven", "Abi"]

    students = []

    if day == "Tuesday":
        students = students_tues
    elif day == "Wednesday":
        students = students_wed
    elif day == "Saturday":
        students = students_sat

    return students


def SpecialPrint(message):
    if len(message) > 80:
        border = '-' * 80
    else:
        border = '-' * len(message)

    print("{}\n{}\n{}".format(border, message, border))


def main():
    day = getDay()
    SpecialPrint("{}".format(day.upper()))

    student_list = getStudents(day)

    if not student_list:
        print("No students.")
        return

    opening_sentence = "This week, " + input("[First Sentence]\nThis week, ")

    print("\n[Personal Sentence]")

    personal_sentence = []

    for student in student_list:
        temp_sentence = "{} ".format(student) + input("{} ".format(student))
        personal_sentence.append(temp_sentence)
        print()

    print()

    closing_sentence = "Next week, " + input("[Last Sentence]\nNext week, ")

    if input("\nEncourage MVP? (Y/N): ") in {'Y', 'y'}:
        mvp_sentence = "Students are encouraged to watch the MVP livestreams on Wednesdays at 5pm (twitch.tv/svroboticsacademy or svrobotics.ca/MVP)."
    else:
        mvp_sentence = ""

    print()

    for sentence in personal_sentence:
        final_sentence = opening_sentence + ' ' + sentence + \
            ' ' + closing_sentence + ' ' + mvp_sentence

        SpecialPrint(final_sentence)
        pyperclip.copy(final_sentence)
        input("Text is copied to clipboard. Press enter for next student.")

    return


if __name__ == "__main__":
    main()
