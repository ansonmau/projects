links = ['a', 'b', 'c', 'd', 'e', 'f']

file = open("info.txt", 'w')

message = '\nLinks that the program could not complete (error)\n'
file.write(('-'*len(message)) + message + ('-'*len(message)) + "\n")
for link in links:
    file.write("{}\n".format(link))

file.close()
