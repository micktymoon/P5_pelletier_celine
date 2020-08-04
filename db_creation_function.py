#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector
from classe_mysqlconnector import MysqlConnector
from classe_database import DatabaseManager, CategoryManager
from function_updating_db import get_store_and_add_to_db, \
    associate_cat_to_product, associate_store_to_product


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