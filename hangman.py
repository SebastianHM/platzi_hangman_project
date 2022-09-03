import os
import random
from typing import List, Dict


def define_hangman() -> tuple:
    """Contains hangman draw divided in 5 parts, this defines  the
    total amount of tries for the game
    Args: None

    Returns: (tuple(List)): one list with hangman draw and other with an empty draw
    """

    err11 = "        ______   "
    err12 = "       |         "
    err13 = "       |         "
    err14 = "       |         "
    err15 = "       |         "
    err16 = "       |         "
    err17 = "       |         "
    err18 = " _____ | _____   "

    err21 = "            __   "
    err22 = "           |__|  "

    err31 = "             |   "
    err32 = "             |   "

    err41 = "            / \  "
    err42 = "           /   \ "

    err51 = "            / \  "
    err52 = "           /   \ "

    draw1 = {
        "err10": err11,
        "err11": err12,
        "err12": err13,
        "err13": err14,
        "err14": err15,
        "err15": err16,
        "err16": err17,
        "err17": err18,
    }

    draw2 = {"err21": err21, "err22": err22}
    draw3 = {"err33": err31, "err34": err32}
    draw4 = {"err43": err41, "err44": err42}
    draw5 = {"err55": err51, "err56": err52}

    initial_draw = {
        "0": "",
        "1": "",
        "2": "",
        "3": "",
        "4": "",
        "5": "",
        "6": "",
        "7": "",
    }

    return [draw1, draw2, draw3, draw4, draw5], [initial_draw]


def define_letters() -> Dict:
    """Contains initial draw of all the letters
    Args:None

    Returns (Dict): with list of strings to draw initial letters
    """
    line1 = "  Avaliable  "
    line2 = "   Letters   "
    line3 = "             "
    line4 = "  A B C D E  "
    line5 = " F G H I J K "
    line6 = "  L M N O P  "
    line7 = "   Q R S T   "
    line8 = " U V W X Y Z "

    letters = {
        "line1": line1,
        "line2": line2,
        "line3": line3,
        "line4": line4,
        "line5": line5,
        "line6": line6,
        "line7": line7,
        "line8": line8,
    }
    return letters


def get_current_letters(current_letters: Dict, new_letter: str) -> Dict:
    """Updates avaliable letters
    Args:
         current_letters(Dict[List]): avaliable letters
         new_letters(str): new letter guessed

    Returns (Dict[List]): with letters dictionary updated
    """
    letters_copy = current_letters.copy()
    [letters_copy.pop(key) for key in ["line1", "line2", "line3"]]

    for key, value in letters_copy.items():
        if new_letter.upper() in value:
            current_letters[key] = value.replace(new_letter.upper(), "*")
            break

    return current_letters


def get_hangman_words() -> List:
    """Brings some english words from a word.txt file in the same folder
    Args: None

    Returns (List): with some english words

    """
    words = []
    with open("words.txt", "r") as f:
        for word in f:
            words.append(word)
    return words


def word_with_guess(word: str, guessed_word: List[str], tmp_letter: str) -> List[str]:
    """Updates current guessed word with a new letter given, if no letter has benn correct
       the guessed word would be a series of '_' if the letter is correct it will be placed
       in all locations
    Args:
        word (str): current word to be guessed
        guessed_word(List[str]): current guessed word
        tmp_letter(str): new letter guessed

    Returns (List[str]): current guessed word updated

    """
    positions = [index for index in range(len(word)) if tmp_letter == word[index]]

    guessed_word = list(
        map(
            lambda i: word[i] if i in positions else guessed_word[i],
            list(range(len(word) - 1)),
        )
    )
    return guessed_word


def overwrite_string(base_line: str, new_line: str) -> str:
    """takes two strings of same length and combines them putting the first one as the base
    and replacing the characters with the corresponding characters from the second string
    where they are diffrent than a blank ' '
    Args:
         base_line(str): base string to get replaced
         new_line(str): line to replace with

    Returns (str): combined line
    """
    overwrited_string = ""
    for index in range(len(new_line)):
        new_char = base_line[index] if new_line[index] == " " else new_line[index]
        overwrited_string += new_char
    return overwrited_string


def merge_draws(draws: List[List]) -> List[Dict]:
    """takes a list containing draws and combines them
    Args:
        draws(List[List]): draws to be merged

    Returns(List[Dict]): merged draw
    """
    if len(draws) == 1:
        added_draw = draws[0]
    else:
        added_draw = draws[0]
        for draw in draws:
            for line in draw.keys():
                key = list(added_draw.keys())[int(line[-1])]
                added_draw[key] = overwrite_string(added_draw[key], draw[line])
    return added_draw


def add_draws(draw1: List[Dict], draw2: List[Dict], spacing: int = 10) -> List[Dict]:
    """Adds draws horizontally
    Args:
        draw1(List[Dict]): first draw
        draw(List[Dict]): second draw
        spacing(int): spacing wanted between the two draws

    Returns (List[Dict]): with the 2 initial draws added
    """
    added_draw = draw1.copy()
    spaces = " " * spacing
    for i in range(len(draw1)):
        draw1_key = list(draw1.keys())[i]
        draw2_key = list(draw2.keys())[i]

        added_draw.update({draw1_key: draw1[draw1_key] + spaces + draw2[draw2_key]})

    return added_draw


def print_draw(draw: List[Dict]) -> List[Dict]:
    """Prints a draw
    Args:
        draw (List[Dict]): draw to print
    Returns: None
    """
    for part in draw.values():
        print(part)
    return None


def draw_hangman(word: str, tmp_letter: str, number_errors: int, complete_draw: Dict):
    """Builds the hangman draw and adds a new part of it if the guessed letter was incorrect
    Args:
        word(str): word to guess
        tmp_letter(str): new guessed letter
        number_errors(int): amount of errors made
        complete_draw(Dict[List]): current hangman draw
    Returns (Dict[List]): new hangman draw
    """
    new_draw = complete_draw
    if tmp_letter not in word:
        number_errors += 1
        draw = complete_draw[0:number_errors]
        new_draw = merge_draws(draw)

    new_draw = new_draw if isinstance(new_draw, list) else [new_draw]

    return number_errors, new_draw


def main():
    """runs the hangman game"""

    print()
    print("Welcome to the hangman game!")
    cond = True
    words = get_hangman_words()
    word = ""
    complete_draw = define_hangman()[0]

    while cond:
        if word == "":
            print("Get ready for a New Word!!")
            current_letters = define_letters()
            rand_index = random.randint(0, len(words))
            word = words[rand_index]
            number_errors = 0
            guessed_word = ["_" for i in word][0:-1]
            print()
            print_draw(current_letters)
            print("".join(guessed_word))
            complete_draw = define_hangman()[0]

        print()
        tmp_letter = input("Guess a letter:")
        os.system("cls")

        if tmp_letter.isnumeric() or len(tmp_letter) != 1:
            print("your guess must be a single letter")
            continue

        guessed_word = word_with_guess(word, guessed_word, tmp_letter)
        print("debug main complete_draw type:", type(complete_draw))
        number_errors, hangman_draw = draw_hangman(
            word, tmp_letter, number_errors, complete_draw
        )

        current_letters = get_current_letters(current_letters, tmp_letter)
        game_draw = (
            add_draws(current_letters, hangman_draw[0])
            if number_errors > 0
            else current_letters
        )
        print_draw(game_draw)

        guess = "".join(guessed_word)
        print()
        print(guess)
        print()
        print("number of errors:", number_errors)

        if number_errors == 5:
            print("You loose, looser")
            print(f"The word was: {word}")
            continue_ = input("wanna keep playing?(Y/N)")
            cond = False if continue_.lower() == "n" else True
            word = ""
            os.system("cls")

        print()

        if not ("_" in guess):
            print("Congratulations you guessed the word")
            continue_ = input("wanna keep playing?(Y/N)")
            cond = False if continue_.lower() == "n" else True
            word = ""
            number_errors = 0
            os.system("cls")


if __name__ == "__main__":
    main()
