#!/usr/bin/python3
# -*-coding: utf8 -*-


def get_cat_and_add_to_db(cm, text):
    """Retrieves the categories of a text and adds them to the database.

    Get the categories from a text and put them in a list.
    And if any categories of the list aren't in the database, the fonction
    insert them in the database.

    Parameters:
        cm : class CategoryManager
            The Manager of the Categories table in the database.
        text : str
            The text whose categories we want to retrieve.
    """
    list_words = text.split(",")
    list_cat_db = []
    response = cm.select()
    for cat in response:
        list_cat_db.append(cat[1])
    for word in list_words:
        word = word.strip()
        category = {"name": word}
        if category["name"] not in list_cat_db:
            cm.insert(category)


def get_store_and_add_to_db(sm, text):
    """Retrieves the stores of a text and adds them to the database.

    Get the stores from a text and put them in a list.
    And if any stores of the list aren't in the database, the fonction
    insert them in the database.

    Parameters:
        sm : class StoreManager
            The Manager of the Categories table in the database.
        text : str
            The text from which we want to retrieve the stores.
    """
    list_words = text.split(",")
    list_store_db = []
    response = sm.select()
    for st in response:
        list_store_db.append(st[1])
    for word in list_words:
        word = word.strip()
        store = {"name": word}
        if store["name"] not in list_store_db:
            sm.insert(store)
