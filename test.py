#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector
from classe_mysqlconnector import MysqlConnector
from classe_database import DatabaseManager, CategoryManager, ProductManager, StoreManager
from classe_api import ApiSearch
from fonction_annexe import get_cat_and_add_to_db, get_store_and_add_to_db

connector = MysqlConnector("localhost", "root", "cP93*mR78.")
if connector.use_db() is False:
    database = DatabaseManager(connector)
    database.create_db()
    print("La base de donnée a été créée.")
    connector.use_db()
    database.create_table()
    print("Les tables ont bien été créées")
    connector.connexion.close()

connector1 = MysqlConnector("localhost", "root", "cP93*mR78.")
connector1.use_db()

# list_categories = ["Boissons",
#                    "Snacks",
#                    "Pizza",
#                    "Bières",
#                    "Chocolats"]
# for cat in list_categories:
#     category = {"name": cat}
#     cm = CategoryManager(connector1)
#     cm.insert(category)
#     print(type(cm))
# print("Les catégories ont été insérées")

product = ["evian", "jus de pomme", "sprite", "prince", "kinder maxi", "pizza regina",
           "pizza 4 fromages", "magnum amande", "glace vanille", "camembert", "sainte maure"]
api_search = ApiSearch()
api_search
for pdt in product:
    prdct = api_search.search_product(pdt)
    print(prdct)
    for product in prdct:
        cm = CategoryManager(connector1)
        sm = StoreManager(connector1)
        pm = ProductManager(connector1)
        try:
            get_cat_and_add_to_db(cm, product["category"])
            get_store_and_add_to_db(sm, product["store"])
            pm.insert(product)
        except mysql.connector.Error:
            pass



print("Les produits ont bien été créés")

# product = "evian"
# api_search = ApiSearch()
# prdct = api_search.search_product(product)
# print(prdct)
# print(api_search.search_cat("Fromage"))
# product1 = ProductManager(connector, prdct["name"], prdct["brand"], prdct["category_id"],
#                           prdct["nutri_score"], prdct["store"], prdct["ingredients"])
# product1.insert()
# pizza_jambon = ProductManager(connector, "Pizza au jambon", "Sodebo", 20, 4, "Magasin U", "Pâte, jambon, fromage")
# pizza_jambon.insert()
# pizza_jambon.select()
# pizza_jambon.get(4)
# product = ["evian", "jus de pomme", "sprite", "prince", "kinder maxi", "pizza regina",
#            "pizza 4 fromages", "magnum amande", "glace vanille", "camembert", "sainte maure"]
# api_search = ApiSearch()
# for pdt in product:
#     prdct = api_search.search_product(pdt)
#     product1 = ProductManager(connector, prdct["name"], prdct["brand"], prdct["category_id"],
#                               prdct["nutri_score"], prdct["store"], prdct["ingredients"])
#     product1.insert()
# print("Les produits ont bien été créés")
# connector.connexion.close()
