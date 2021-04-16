import pyperclip
import datetime
import os


def getDay():
    day_num = datetime.datetime.today().weekday()

    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

    day_word = days[day_num]

    return day_word


def getStudents(day):
    #   Students lists
    students_tues = ["Ethan"]
    students_wed = ["Jordan", "James", "Kathryn"]
    students_fri = ["TEMPNAME"]
    students_sat = ["Haorui", "Niven", "Abi"]

    students = []

    if day == "Tuesday":
        students = students_tues
    elif day == "Wednesday":
        students = students_wed
    elif day == "Friday":
        students = students_fri
    elif day == "Saturday":
        students = students_sat

    return students


def SpecialPrint(message):
    if len(message) > 80:
        border = '-' * 80
    else:
        border = '-' * len(message)

    print("{}\n{}\n{}".format(border, message, border))


def EnsurePeriod(string):
    if not string[-1] in {'.', '?', '!'}:
        string += '.'
    return string


def main():
    os.system('cls')
    day = getDay()
    SpecialPrint("{}".format(day.upper()))

    student_list = getStudents(day)

    if not student_list:
        print("No students.")
        return

    opening_sentence = "This week, " + input("[First Sentence]\nThis week, ")
    opening_sentence = EnsurePeriod(opening_sentence)

    print("\n[Personal Sentence]")

    personal_sentence = []

    for student in student_list:
        temp_sentence = "{} ".format(student) + input("{} ".format(student))

        temp_sentence = EnsurePeriod(temp_sentence)

        personal_sentence.append(temp_sentence)
        print()

    print()

    closing_sentence = "Next week, " + input("[Last Sentence]\nNext week, ")
    closing_sentence = EnsurePeriod(closing_sentence)

    if input("\nEncourage MVP? (Y/N): ") in {'Y', 'y'}:
        mvp_sentence = "Students are encouraged to watch the MVP livestreams on Wednesdays at 5pm (twitch.tv/svroboticsacademy or svrobotics.ca/MVP)."
    else:
        mvp_sentence = ""

    for index in range(len(personal_sentence)):
        curr_student = student_list[index]
        curr_personal_sentence = personal_sentence[index]

        final_sentence = opening_sentence + ' ' + curr_personal_sentence + \
            ' ' + closing_sentence + ' ' + mvp_sentence

        print("\n{}:".format(curr_student.upper()))
        SpecialPrint(final_sentence)
        pyperclip.copy(final_sentence)
        input("Text is copied to clipboard. Press enter for next student ({} more)".format(
            len(personal_sentence) - (index + 1)))

    return


if __name__ == "__main__":
    main()
