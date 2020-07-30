#!/usr/bin/python3
# -*-coding: utf8 -*-

from classe_mysqlconnector import MysqlConnector
from classe_database import CategoryManager, ProductManager, StoreManager,\
    ProductCategoryManager, ProductStoreManager, SubstituteManager
from classe_api import ApiManageSearch
from fonction_annexe import create_db_and_table, insert_first_cat, fill_db

create_db_and_table()
connector1 = MysqlConnector("localhost", "root", "cP93*mR78.")
connector1.use_db()
api_search = ApiManageSearch()
cm = CategoryManager(connector1)
sm = StoreManager(connector1)
pm = ProductManager(connector1)
pcm = ProductCategoryManager(connector1)
psm = ProductStoreManager(connector1)
subm = SubstituteManager(connector1)
list_categories = ["Boissons",
                   "Snacks",
                   "Pizza",
                   "Dessert",
                   "Fromage"]
list_name_prod = ["evian", "jus de pomme", "sprite", "prince", "kinder maxi",
                  "pizza regina", "pizza 4 fromages", "magnum amande",
                  "glace vanille", "camembert", "sainte maure"]
insert_first_cat(list_categories, connector1)
fill_db(api_search, cm, sm, pm, pcm, psm, list_name_prod)
