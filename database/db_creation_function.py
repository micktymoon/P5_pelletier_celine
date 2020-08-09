#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector
from database.classe_mysqlconnector import MysqlConnector
from database.classe_database import DatabaseManager, CategoryManager
from database.function_updating_db import get_store_and_add_to_db, \
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

    Looks up the products in the name list in the API and retrieves them.
    For each product recovered:
    Retrieves, inserts and associates stores and categories in the database,
     and inserts the product into the database.

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
            except mysql.connector.Error as er:
                print("Problème d'ajout des magasins à la base de donnée.")
                print(er)
                get_store_and_add_to_db(sm, product["store"])
                print("Ajout des magasins réalisé avec succès.")
            try:
                product = pm.insert(pcm, psm, product=product)
            except mysql.connector.Error as er:
                print("Problème de création du produit")
                print(er)
                product = pm.insert(pcm, psm, product=product)
                print("Produit créé avec succès.")
            try:
                associate_store_to_product(sm, psm, product)
            except mysql.connector.errors.Error as er:
                print("Problème d'association des magasins au produit.")
                print(er)
                associate_store_to_product(sm, psm, product)
                print("Association des magasins réalisée avec succès")
            try:
                product["store"] = psm.select_association(product["id"])
            except mysql.connector.errors.Error as er:
                print("Problème de récupération des magasins")
                print(er)
                product["store"] = psm.select_association(product["id"])
                print("Récupération des magasins réalisée avec succès.")
            try:
                associate_cat_to_product(cm, pcm, product)
            except mysql.connector.errors.InternalError as er:
                print("Problème d'association des catégories au produit.")
                print(er)
                associate_cat_to_product(cm, pcm, product)
                print("Association des catégories réalisée avec succès.")
            try:
                product["category"] = \
                    pcm.select_asso_with_id_prod(product["id"])
            except mysql.connector.errors.InternalError as er:
                print("Problème de récupération des catégories.")
                print(er)
                product["category"] = \
                    pcm.select_asso_with_id_prod(product["id"])
                print("Récupération des catégories réalisée avec succès.")
