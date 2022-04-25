# a version of the game Hangman by Aena Teodocio
# "Hangman is a word guessing game for two players. In this program, you are guessing a word randomly chosen
# by the computer. The user (you) starts with 6 available letter guesses.
# For every letter guess that is not in the secret word, 2 guesses are deducted if the guess is a vowel and
# 1 guess is deducted if the guess is a consonant.
# You are given 3 warnings for invalid input such as a non-alphabet guess,
# or you entered the same letter you've previously guessed.

# The version "Hangman with hints" allows the user to receive hints. However, no warnings are available!!
# After two correct letter guesses, you may ask for a hint by inputting an asterisk ( * ).
# It will show you all the possible words that match what you have currently guessed.

# Good luck and have fun!

import random


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    input_file = open("words.txt", 'r')
    line = input_file.readline()
    list_of_words = line.split()

    return list_of_words


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    secret_list = [char for char in secret_word]
    try:
        compare_word = [char for char in secret_list if letters_guessed[letters_guessed.index(char)] == char]
        return all(compare_word)
    except ValueError:
        return False


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    guessed_word = ''
    for char in secret_word:
        if char in letters_guessed:
            guessed_word += char + " "
        else:
            guessed_word += "_ "

    return guessed_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    not_guessed = [char for char in alphabet if char not in letters_guessed]

    return ''.join(not_guessed)


def update_drawing(drawing, available_guesses):
    """ Takes in a hangman drawing (list of strings) and available_guesses (int).
        Returns a drawing representing the number of available guesses left before
        game is over."""

    drawing_dict = {
        5: (1, '|        |'),
        4: (2, '|        O'),
        3: (3, '|        |  '),
        2: (4, '|      / | \ '),
        1: (5, '|        | '),
        0: (6, '|       / \ ')
    }

    if available_guesses == 6:
        for i in drawing:
            print(i, end='\n')
    elif available_guesses < 6:
        for idx in range(5, available_guesses - 1, -1):
            drawing[drawing_dict[idx][0]] = drawing_dict[idx][1]
        for i in drawing:
            print(i, end='\n')

    return drawing


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.
    """

    # list of strings to represent the beginning of hangman game
    # drawing is updated at each deduction to available_guesses
    drawing = [
        '__________',  # idx 0
        '|         ',  # idx 1
        '|         ',
        '|         ',
        '|         ',
        '|         ',
        '|         ',  # idx 6
        '|         ',
    ]

    avail_guesses = 6
    guessed_letters = []
    warnings = 3
    spacer = '>>>>>>>>>>>>>>>>>>>>>>>>'

    # Welcome message
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is {} letters long.'.format(len(secret_word)))
    print('You have {} warnings left.'.format(warnings))
    print(spacer)

    # Initiate game
    is_winner_found = False
    while avail_guesses > 0:
        if is_winner_found is False:
            update_drawing(drawing, avail_guesses)
            current_guess = get_guessed_word(secret_word, guessed_letters)
            avail_letters = get_available_letters(guessed_letters)

            print('You have {} guesses left.'.format(avail_guesses))
            print('Available letters:', avail_letters)

            user_guess = input('Please guess a letter: ')

            # If letter is in secret word and has not been guessed before
            if user_guess.lower() in secret_word and not user_guess.lower() in guessed_letters:
                guessed_letters.append(user_guess.lower())
                current_guess = get_guessed_word(secret_word, guessed_letters)

                print('Good guess:', current_guess)

            # Otherwise, check what kind of
            else:
                if user_guess.isalpha() and not user_guess.lower() in guessed_letters:
                    if user_guess in 'aeiou':  # deduct 2 guesses if guess is a vowel
                        avail_guesses -= 2
                    else:  # deduct 1 if consonant
                        avail_guesses -= 1

                    guessed_letters.append(user_guess.lower())
                    print('Oops! That letter is not in my word:', current_guess)

                # Otherwise, there are two other incorrect cases
                # 1. Guess is not an alphabet
                # 2. Letter has been guessed before
                else:
                    if warnings == 0:  # decrement to indicate no warnings left
                        warnings -= 1

                    if warnings >= 0:  # deduct from warnings if available
                        warnings -= 1
                        if user_guess in guessed_letters:
                            print("Oops! You've already guessed that letter.")
                        else:
                            print('Oops! That is not a valid letter.')

                        print("You have {} warnings left: {}".format(warnings, current_guess))

                    elif warnings < 0:  # no warnings left, start deducting from available guesses
                        avail_guesses -= 1
                        if user_guess in guessed_letters:
                            print("Oops! You've already guessed that letter.")
                        else:
                            print('Oops! That is not a valid letter.')

                        print('You have no warnings left so you lose one guess:', current_guess)

            is_winner_found = is_word_guessed(secret_word, guessed_letters)
            print(spacer)

        else:  # otherwise, word has been guessed correctly
            unique_letters = len(set(secret_word))
            score = avail_guesses * unique_letters
            print('Congratulations, you won!! :D ')
            return 'Your total score for this game is:' + " " + str(score)

    update_drawing(drawing, avail_guesses)
    return 'Sorry you ran out of guesses. The word was' + ' "' + secret_word + '".'


# The next 3 functions are dedicated for Hangman with Hints


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol _ ,
        and my_word and other_word are of the same length;
        False otherwise:
    """
    character_check = []
    for i in range(len(my_word)):
        if my_word[i] == other_word[i] or my_word[i] == "_":
            character_check.append(True)
        else:
            character_check.append(False)

    return all(character_check)


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
    """
    word_list = load_words()
    the_word = my_word.replace(" ", "")

    length_match = [word for word in word_list if len(the_word) == len(word)]
    word_match = []

    for word in length_match:
        compared_word = match_with_gaps(the_word, word)
        if compared_word is True:
            word_match.append(word)

    if len(word_match) > 0:
        for match in word_match:
            print(match, end=" ")
    else:
        print("No matches found.")


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman with hints.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.
    """
    drawing = [
        '__________',  # idx 0
        '|         ',  # idx 1
        '|         ',
        '|         ',
        '|         ',
        '|         ',
        '|         ',  # idx 6
        '|         ',
    ]

    avail_guesses = 6
    guessed_letters = []
    spacer = '>>>>>>>>>>>>>>>>>>>>>>>>'

    # Welcome message
    print('Welcome to the game Hangman with Hints!')
    print('No warnings are available!' + '\n' + 'After 2 correct guesses, you may type " * " to receive a hint.')
    print('I am thinking of a word that is {} letters long.'.format(len(secret_word)))
    print("\n" + spacer)

    # Initiate game
    is_winner_found = False
    while avail_guesses > 0:
        if is_winner_found is False:
            update_drawing(drawing, avail_guesses)
            current_guess = get_guessed_word(secret_word, guessed_letters)
            avail_letters = get_available_letters(guessed_letters)

            print('You have {} guesses left.'.format(avail_guesses))

            print('Available letters:', avail_letters)

            user_guess = input('Please guess a letter: ')

            if user_guess == "*" and len(guessed_letters) >= 2:  # hints available after two correct guesses
                print('Possible word matches are:')
                show_possible_matches(current_guess)

            # If letter is in secret word and has not been guessed before
            elif user_guess.lower() in secret_word and not user_guess.lower() in guessed_letters:
                guessed_letters.append(user_guess.lower())
                current_guess = get_guessed_word(secret_word, guessed_letters)

                print('Good guess:', current_guess)

            # Otherwise, check what kind of
            else:
                if user_guess.isalpha() and not user_guess.lower() in guessed_letters:
                    if user_guess in 'aeiou':  # deduct 2 guesses if guess is a vowel
                        avail_guesses -= 2
                    else:  # deduct 1 if consonant
                        avail_guesses -= 1

                    guessed_letters.append(user_guess.lower())
                    print('Oops! That letter is not in my word:', current_guess)

                else:
                    avail_guesses -= 1
                    if user_guess in guessed_letters:
                        print("Oops! You've already guessed that letter.")
                    else:
                        print('Oops! That is not a valid letter.')

            is_winner_found = is_word_guessed(secret_word, guessed_letters)
            print("\n" + spacer)

        else:  # otherwise, word has been guessed correctly
            unique_letters = len(set(secret_word))
            score = avail_guesses * unique_letters
            print('Congratulations, you won!! :D')
            return 'Your total score for this game is:' + " " + str(score)

    update_drawing(drawing, avail_guesses)
    return 'Sorry you ran out of guesses. The word was' + ' "' + secret_word + '".'


if __name__ == "__main__":
    print("Loading word list from file...")
    word_list = load_words()
    secret_word = random.choice(word_list)

    print("  ", len(word_list), "words loaded.", '\n')
    chosen_game = input('Would you like to play with hints? Y or N: ')

    if chosen_game in "Nn":
        print(hangman(secret_word))
    elif chosen_game in "Yy":
        print(hangman_with_hints(secret_word))
