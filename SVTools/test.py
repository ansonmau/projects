import random

Movies = ["Iron Man", "Bee Movie", "Avengers", "The Hulk"]

print(random.choice(Movies))

for x in (random.choice(Movies)):
    print(x, end='')
