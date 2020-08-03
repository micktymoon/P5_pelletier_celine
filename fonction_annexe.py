#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector
from classe_mysqlconnector import MysqlConnector
from classe_database import DatabaseManager, CategoryManager


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


def get_store_and_add_to_db(sm, text):
    """
    Retrieves the stores of a text and adds them to the database.

    Get the stores from a text and put them in a list.
    And if any stores of the list aren't in the database, the fonction
    insert them in the database.

    Parameters:
        sm : class StoreManager
            The Manager of the Categories table in the database.
        text : str
            The text from which we want to retrieve the stores.
    """
    store_db = sm.select()
    list_store_db = []
    for sto in store_db:
        list_store_db.append(sto["name"])
    for word in text:
        word = word.strip()
        store = {"name": word}
        if store["name"] not in list_store_db:
            sm.insert(store)


def associate_cat_to_product(cm, pcm, product):
    """Associate a category to a product in the database and the category
        to Categories table if it doesn't exist.

    Get a list of product categories.
    Checks if the product categories corresponds to one of the
     categories of the database, and if yes, associates the product with
     the category. But if the category doesn't exist in the Categories table
     of the database, insert the category in the table and then associate it
     with the product.

    Parameters:
        cm : class CategoryManager
            The manager of the Categories table in the database.
        pcm : class ProductCategoryManager
            The manager of the ProductCategory table in the database.
        product : dict
            The product to whiwh we want to associate a category.
     """
    for cat in product["category"]:
        check = cm.select(name=cat)
        if check is None:
            category = {"name": cat}
            cm.insert(category)
            pcm.insert_association(category["id"], product["id"])
        else:
            pcm.insert_association(check["id"], product["id"])


def associate_store_to_product(sm, psm, product):
    """Associate a store to a product in the database and the store to Store
        table if it doesn't exist.

        Get a list of product store.
        Checks if the product stores corresponds to one of the
         stores of the database, and if yes, associates the product with
         the store. But if the store doesn't exist in the Store table of
         the database, insert the store in the table and then associate it
         with the product.

        Parameters:
            sm : class StoreManager
                The manager of the Store table in the database.
            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.
            product : dict
                The product to whiwh we want to associate a store.
         """
    for sto in product["store"]:
        check = sm.select(name=sto)
        if check is None:
            store = {"name": sto}
            sm.insert(store)
            psm.insert_association(store["id"], product["id"])
        else:
            psm.insert_association(check["id"], product["id"])


def input_int(text):
    """
    Asks the user to enter a number.

    Asks the user to enter a number and verifies that what they entered
     is a number.
     Returns the result if it is a number.
     Displays an error message if the result is not a number.

    Parameters:
    text : str
        The data that the user enters into the program.

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


def create_db_and_table():
    """
    Create the database and useful tables.

    Create a connector to MySQL.
    If the connector can't use the database because it does not exist,
     it will create it.
    """
    connector = MysqlConnector("localhost", "root", "cP93*mR78.")
    if connector.use_db() is False:
        database = DatabaseManager(connector)
        database.create_db()
        print("La base de donnée a été créée.")
        connector.use_db()
        database.create_table()
        print("Les tables ont bien été créées")
        connector.connexion.close()


def insert_first_cat(list_categories, connector):
    """
    Insert a first list of categories in the database.

    Parameters:
    list_categories : list
        The list of categories that we want to enter in the database.

    connector : Class MysqlConnector
        The database connector.
    """
    for cat in list_categories:
        category = {"name": cat}
        cm = CategoryManager(connector)
        cm.insert(category)
    print("Les catégories ont été insérées")


def fill_db(api_search, cm, sm, pm, pcm, psm, list_name_prod):
    """
    Fills the database with a list of products, associates stores and
     categories with their products.

    Retrieves products for each product name in the list.
    For each product, retrieves stores and categories and adds them to the
     database, then associates the product with its stores and categories.

    Parameters
    ----------
    api_search : Class ApiManagerSearch
        The manager of the OpenFoodFact API research manager.

    cm : class CategoryManager
        The manager of the Categories table in the database.

    sm : class StoreManager
        The manager of the Store table in the database.

    pm : class ProductManager
        The manager of the Product table in the database.

    pcm : class ProductCategoryManager
        The manager of the ProductCategory table in the database.

    psm : class ProductStoreManager
        The manager of the ProductStore table in the database.

    list_name_prod : list
        The list of the names of the products that we want to recover.
    """
    for name_prod in list_name_prod:
        api_list_prod = api_search.search_product(name_prod)
        for product in api_list_prod[:2]:
            try:
                get_store_and_add_to_db(sm, product["store"])
                product = pm.insert(pcm, psm, product=product)
                associate_store_to_product(sm, psm, product)
                product["store"] = psm.select_association_with_id_prod(product["id"])
            except mysql.connector.errors.Error as er:
                print(er)
            try:
                associate_cat_to_product(cm, pcm, product)
                product["category"] = pcm.select_association_with_id_prod(product["id"])
            except mysql.connector.errors.InternalError:
                associate_cat_to_product(cm, pcm, product)
                product["category"] = pcm.select_association_with_id_prod(product["id"])
                print("l'association des catégorie à quand même été faite")