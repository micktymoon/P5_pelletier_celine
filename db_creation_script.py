#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector
from classe_mysqlconnector import MysqlConnector
from classe_database import CategoryManager, ProductManager, StoreManager,\
    ProductCategoryManager, ProductStoreManager
from classe_api import ApiManageSearch
from db_creation_function import create_db_and_table, insert_first_cat,\
    fill_db


def main():
    """
    Create the database and fill it.
    """
    create_db_and_table()
    connector = MysqlConnector("localhost", "root", "cP93*mR78.")
    connector.use_db()
    api_search = ApiManageSearch()
    cm = CategoryManager(connector)
    sm = StoreManager(connector)
    pm = ProductManager(connector)
    pcm = ProductCategoryManager(connector)
    psm = ProductStoreManager(connector)
    list_categories = ["Boissons",
                       "Snacks",
                       "Pizzas",
                       "Desserts",
                       "Fromages"]
    list_name_prod = ["eau", "jus de pomme", "sprite", "prince", "kinder",
                      "pizza regina", "pizza 4 fromages", "magnum amande",
                      "glace vanille", "camembert", "sainte maure"]
    insert_first_cat(list_categories, connector)
    try:
        fill_db(api_search, cm, sm, pm, pcm, psm, list_name_prod)
    except mysql.connector.errors.InternalError:
        fill_db(api_search, cm, sm, pm, pcm, psm, list_name_prod)


if __name__ == "__main__":
    main()
