def getGameState(guessed_letters, word):
    gameState = ''
    for letter in word:
        if letter == ' ':
            gameState += '  '
        elif letter in guessed_letters:
            gameState = gameState + (letter) + ' '
        else:
            gameState = gameState + '_ '
    return gameState


guesses = []
word = 'anson'
