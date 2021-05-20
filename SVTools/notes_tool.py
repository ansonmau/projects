import pyperclip
import datetime
import os


def getStudents(day):
    #   Students lists
    students_tues = ["Nathaniel", "Ethan", "Gurnoor", "Liam"]
    students_fri_1 = ["Sruti"]
    students_fri_2 = ["Leo", "Madhav"]
    students_sat = ["Ariana", "Asha", "Oscar"]

    students = []

    if day == "Tuesday":
        students = students_tues
    elif day == "Friday":
        choice = input("Friday class 1 or 2?: ")
        while choice not in {'1', '2'}:
            choice = input("[1] 5:00 - 6:00pm\t[2] 6:15-7:15pm\n")
        if choice == "1":
            students = students_fri_1
        else:
            students = students_fri_2
    elif day == "Saturday":
        students = students_sat

    return students


def getDay():
    day_num = datetime.datetime.today().weekday()

    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

    day_word = days[day_num]

    return day_word


def SpecialPrint(message):
    if len(message) > 80:
        border = '-' * 80
    else:
        border = '-' * len(message)

    print("{}\n{}\n{}".format(border, message, border))


def EnsurePeriod(string):
    string = string.strip()
    if string[-1] not in {'.', '?', '!'}:
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
    else:
        print("Students: {}\n".format(", ".join(student_list)))

    opening_sentence = "This week, " + input("[First Sentence]\nThis week, ")
    opening_sentence = EnsurePeriod(opening_sentence)

    print("\n[Personal Sentence]")

    personal_sentences = []

    for student in student_list:
        temp_sentence = "{} ".format(student) + input("{} ".format(student))

        temp_sentence = EnsurePeriod(temp_sentence)

        personal_sentences.append(temp_sentence)
        print()

    print()

    closing_sentence = "Next week, " + input("[Last Sentence]\nNext week, ")
    closing_sentence = EnsurePeriod(closing_sentence)

    if input("\nEncourage MVP? (Y/N): ") in {'Y', 'y'}:
        choice = input("[1] JR\t[2] SR\n")
        if choice in {'1', 'jr'}:
            mvp_sentence = "Students are encouraged to watch the MVP livestreams on Wednesdays at 5pm (twitch.tv/svroboticsacademy or svrobotics.ca/MVP)."
        elif choice in {'2', 'sr'}:
            mvp_sentence = "Students are encouraged to watch the MVP livestreams on Tuesdays at 7pm (twitch.tv/svroboticsacademy or svrobotics.ca/MVP)."
    else:
        mvp_sentence = ""

    for index in range(len(personal_sentences)):
        curr_student = student_list[index]
        curr_personal_sentences = personal_sentences[index]

        final_sentence = opening_sentence + ' ' + curr_personal_sentences + \
            ' ' + closing_sentence + ' ' + mvp_sentence

        print("\n{}:".format(curr_student.upper()))
        SpecialPrint(final_sentence)
        pyperclip.copy(final_sentence)
        input("Text is copied to clipboard. Press enter for next student ({} more)".format(
            len(personal_sentences) - (index + 1)))

    return


if __name__ == "__main__":
    main()
