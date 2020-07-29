#!/usr/bin/python3
# -*-coding: utf8 -*-

from classe_mysqlconnector import MysqlConnector
from classe_database import CategoryManager, ProductManager, StoreManager,\
    ProductCategoryManager, ProductStoreManager, SubstituteManager
from classe_api import ApiManageSearch
from fonction_annexe import create_db_and_table, insert_first_cat, fill_db, associate_substitute_to_product
from classe_ui import UserInterfaceManager

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


def run(cm, pm, pcm, subm):
    while 1:
        uim = UserInterfaceManager()
        uim.main_menu()
        if uim.choice1 == 1:
            list_cat = cm.select()
            uim.choice_category(list_cat)
            if uim.choice_cat is not None:
                list_prod = pm.select()
                uim.choice_product(list_prod)
                list_sub = associate_substitute_to_product(pm, pcm,
                                                           uim.choice_prod)
                if list_sub:
                    for sub in list_sub:
                        print("Produit n°{}: {}, magasins où le trouver: {}, url "
                              "OpenFoodFact: {}.".format(sub["id"],
                                                         sub["name"],
                                                         sub["store"],
                                                         sub["url"]))
                    uim.save_substitute(list_sub, subm, uim.choice_prod)
        if uim.choice1 == 2:
            id_prod = uim.show_substitute(subm, psm, pcm, pm)
            print("Voici les substituts du produit "
                  "n°{}".format(id_prod))
            for sub in uim.list_sub:
                print("Produit n°{}: {}, magasins où le trouver: {}, url "
                      "OpenFoodFact: {}.".format(sub["id"],
                                                 sub["name"],
                                                 sub["store"],
                                                 sub["url"]))

        if uim.choice1 == 3:
            print("A bientôt.")
            break


main(cm, pm, pcm, subm)
