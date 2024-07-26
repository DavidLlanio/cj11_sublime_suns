import random

file = open("./data/jumble_words.txt")
content = file.readlines()
file.close()
for ii in range(len(content)):
    content[ii] = content[ii].replace("\n", "")
"""
TODO
- Create validate function that takes 2 parameters (user input, unjumbled? word)
and checks if the user correctly finds the jumbled word.
"""

def Play(words: list) -> None:
    word = random.choice(words).lower()
    wordBroken = list(word)
    jumbled = Jumble(wordBroken)
    print(jumbled)
    userAnswer = input("What is the word?\n:")
    if Validate(word, userAnswer):
        print("Level completed!")
        """
        TODO
        - Integrate PvP point system
        - add timer for respective points
        """
    else:
        print("Failed!")

def Jumble(word: str) -> str:
    random.shuffle(word)
    jumbledWord = "".join(word)
    return jumbledWord

def Validate(word: str, userInput: str) -> bool:
    result = False
    if word == userInput:
        result = True
    return result


Play(content)