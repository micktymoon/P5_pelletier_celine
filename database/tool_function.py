#!/usr/bin/python3
# -*-coding: utf8 -*-


def get_word_remove_spaces(text):
    """
    Retrieves the words of a text in a list and removes spaces before
     and after each word.

    Parameters:
        text : str
            The text whose words we want to recover.

    Returns:
        list
            The list of text words.
    """
    list_words = text.split(",")
    list_without_spaces = []
    for word in list_words:
        word = word.strip()
        list_without_spaces.append(word)
    return list_without_spaces


def input_int(text):
    """
    Asks the user to enter a number.

    Asks the user to enter a number and verifies that what they entered
     is a number.
    Returns the result if it is a number.
    Displays an error message if the result is not a number.

    Parameters:
        text : str
            The resource that the user enters into the program.

    Returns:
        int
            Number that the user has entered into the program.
    """
    while 1:
        chiffre = input(text)
        try:
            chiffre = int(chiffre)
            return chiffre
        except ValueError:
            print("ce n'est pas un entier.")
