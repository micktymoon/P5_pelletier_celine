#!/usr/bin/python3
# -*-coding: utf8 -*-

import mysql.connector
from classe_mysqlconnector import MysqlConnector
from classe_database import DatabaseManager, CategoryManager, ProductManager, StoreManager, ProductCategoryManager, ProductStoreManager
from classe_api import ApiSearch
from fonction_annexe import get_store_and_add_to_db, associate_cat_to_product, associate_store_to_product

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

list_categories = ["Boissons",
                   "Snacks",
                   "Pizza",
                   "Bières",
                   "Chocolats"]
for cat in list_categories:
    category = {"name": cat}
    cm = CategoryManager(connector1)
    cm.insert(category)

print("Les catégories ont été insérées")

product = ["evian", "jus de pomme", "sprite", "prince", "kinder maxi", "pizza regina",
           "pizza 4 fromages", "magnum amande", "glace vanille", "camembert", "sainte maure"]
api_search = ApiSearch()

cm = CategoryManager(connector1)
sm = StoreManager(connector1)
pm = ProductManager(connector1)
pcm = ProductCategoryManager(connector1)
psm = ProductStoreManager(connector1)
for pdt in product:
    prdct = api_search.search_product(pdt)
    for product in prdct:
        try:
            get_store_and_add_to_db(sm, product["store"])
            pm.insert(product)
            if associate_cat_to_product(cm, pcm, product) is not True:
                product_cat = product["category"].split(",")
                product_cat_strip = []
                for cat in product_cat:
                    cat = cat.strip()
                    product_cat_strip.append(cat)
                category = {"name": product_cat_strip[0]}
                cm.insert(category)
                associate_cat_to_product(cm, pcm, product)
            if associate_store_to_product(sm, psm, product) is not True:
                product_store = product["store"].split(",")
                product_store_strip = []
                for sto in product_store:
                    sto = sto.strip()
                    product_store_strip.append(sto)
                store = {"name": product_store_strip[0]}
                sm.insert(store)
                associate_store_to_product(sm, psm, product)

        except mysql.connector.Error:
            pass

print("les produit ont été ajouté et associé à leurs catégories")
print(pcm.select_association(11))