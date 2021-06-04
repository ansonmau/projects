
def countLetters(string_list, charToFind):
    letter_count = []
    for s in string_list:
        letter_count.append(s.count(charToFind))

    return letter_count


all_sentences = []

print("Enter as many sentences as you want. Enter nothing to stop entering sentences.")

sentence = input("Enter a sentence/word \n>>> ")
while not sentence == '':
    all_sentences.append(sentence)
    sentence = input("Enter another sentence/word \n>>> ")


char = input("Enter the character you want to count \n>>> ")
while len(char) == 0:
    char = input("Please enter a proper character \n>>> ")
letter_count = countLetters(all_sentences, char)

print("----- '{}' COUNT -----".format(char))
for i in range(len(all_sentences)):
    print("{} : {}".format(all_sentences[i], letter_count[i]))
