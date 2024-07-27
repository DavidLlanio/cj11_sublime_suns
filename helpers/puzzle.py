import random
import json

WORDS: list[str] = []
ANAGRAMS: list[str] = []
ANAGRAMS_DATA: dict[str, list[str]] = {}

with open("./data/anagrams_adventure.json") as file:
    data = json.load(file)
    ANAGRAMS = list(data.keys())
    ANAGRAMS_DATA = data


with open("./data/jumble_words.txt") as file:
    WORDS = [line.strip() for line in file.readlines()]


def jumble_word(word: list[str]) -> str:
    word_list = list(word)
    random.shuffle(word_list)
    jumbled_word = "".join(word_list)
    return jumbled_word


def jumble() -> tuple[str, str]:
    word = random.choice(WORDS).lower()
    return word, jumble_word(list(word))
