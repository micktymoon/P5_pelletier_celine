#!/usr/bin/python3
# -*-coding: utf8 -*-
from fonction_annexe import *


class UserInterfaceManager:
    """
            Class which manages the user interface.

        Attributes:


        Methods:
            first_choice()
                Displays the first choice to the user.
            category_choice()
                Displays the categories to the user.
            product_choice()
                Displays the products of the chosen category to the user.
            substitute_proposal()
                Proposes a substitute for the chosen product to the user.
    """
    def __init__(self, cm, pm, pcm, psm, subm, api):
        """
        UserInterfaceManager class constructor.

        Parameters:

        """
        self.cm = cm
        self.pm = pm
        self.pcm = pcm
        self.psm = psm
        self.subm = subm
        self.api = api
        self.substitute = None
        self.list_sub = None

    def main_menu(self):
        while True:
            print("Que souhaitez-vous faire?\n"
                  "1 : Quel aliment souhaitez-vous remplacer?\n"
                  "2 : Retrouver mes aliments substitutés.\n"
                  "3 : Quitter")
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            if choice == 1:
                self.choice_category()
            elif choice == 2:
                choice = self.show_substitute(self.subm, self.psm, self.pcm, self.pm)
                for prod in self.list_sub:
                    if choice == prod["id"]:
                        self.suggest_substitute(prod)
                    elif choice == 0:
                        quit()
                    elif choice == -1:
                        return
            elif choice == 3:
                print("A bientôt.")
                break

    def choice_category(self):
        while True:
            print("Voici la liste des catégories :")
            print("Entrez -1 si vous désirez retourner au menu précédent.")
            list_cat = self.cm.select()
            for cat in list_cat:
                print("{} : {}".format(cat["id"], cat["name"]))
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            if choice == -1:
                return
            found = None
            for cat in list_cat:
                if choice == cat["id"]:
                    found = cat
                    break
            if found:
                self.choice_product(self.pcm, self.psm, found)

    def choice_product(self, pcm, psm, category):
        while True:
            print("Voici la liste des aliments de la"
                  " catégorie: {}".format(category["name"]))
            print("Entrez 0 si vous désirez quitter.")
            print("Entrez -1 si vous désirez retourner au menu précédent.")
            list_product = self.pm.select(pcm, psm)
            list_prod_cat = []
            for prod in list_product:
                for cat in prod["category"]:
                    if cat == category["name"]:
                        list_prod_cat.append(prod)
                        print("{} : {}, nutri-score = {}".format(prod["id"],
                                                                 prod["name"],
                                                                 prod["nutriscore"]))
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            for prod in list_prod_cat:
                if choice == prod["id"]:
                    list_sub = self.subm.associate_substitute_to_product(self.pm,
                                                                         self.pcm,
                                                                         self.psm,
                                                                         prod)
                    print(list_sub)
                    if list_sub:
                        list_sub.sort(key=lambda d: d["nutriscore"])
                        for sub in list_sub:
                            print("Produit n°{}: {}, magasins où le trouver: {}, nutri-score: {}, url "
                                  "OpenFoodFact: {}.".format(sub["id"],
                                                             sub["name"],
                                                             sub["store"],
                                                             sub["nutriscore"],
                                                             sub["url"]))
                        self.save_substitute(list_sub, self.subm, prod)
                    if list_sub is None:
                        list_api_search = self.api.search_product(prod["name"])
                        self.pm.insert(self.pcm, self.psm, list_prod=list_api_search)
                        list_sub_possible = self.subm.associate_substitute_to_product(self.pm, self.pcm, self.psm, prod)
                        for sub in list_sub_possible:
                            print("Produit n°{}: {}, magasins où le trouver: {}, nutri-score: {}, url "
                                  "OpenFoodFact: {}.".format(sub["id"],
                                                             sub["name"],
                                                             sub["store"],
                                                             sub["nutriscore"],
                                                             sub["url"]))
                        self.save_substitute(list_sub, self.subm, prod)
                elif choice == 0:
                    print("A bientôt.")
                    quit()
                elif choice == -1:
                    return

    def suggest_substitute(self, product):
        list_substitute = self.subm.select_association(product["id"],
                                                       self.psm,
                                                       self.pcm,
                                                       self.pm)
        self.substitute = list_substitute[0]
        print("Voici le substitut proposé pour l'aliment que vous avez choisit")
        print("Substitue n°{}, nom: {}, nutriscore: {},\n "
              "url : {}".format(self.substitute["id"],
                                self.substitute["name"],
                                self.substitute["nutriscore"],
                                self.substitute["url"]))

    def save_substitute(self, list_sub, subm, product):
        """

        Parameters:
            list_sub : list
                The list of substitute possible.

            subm : class SubstituteManager
                The manager of the Substitute table in the database.

            product : dict
                The product to whiwh we want to associate a store.

        Returns:

        """
        print("Voulez vous sauvegarder les substitues?")
        choice = input("Entrez 'o' pour oui ou 'n' pour non")
        if choice == "o":
            for sub in list_sub:
                subm.insert_association(product["id"], sub["id"])
        if choice == "n":
            pass

    def show_substitute(self, subm, psm, pcm, pm):
        list_substituted_prod = self.subm.select_substituted_product()
        print("Voici les produits ayant un substitut:")
        for product in list_substituted_prod:
            print("Produit n°{}: {}".format(product["id"], product["name"]))
        prod = input_int("Entrez le nombre du produit dont vous voulez voir"
                         " les susbtituts.")
        for product in list_substituted_prod:
            if prod == product["id"]:
                self.list_sub = subm.select_association(product["id"],
                                                        psm, pcm, pm)
                return product["id"]


# class Toto(object):
#
#     def main_menu(self):
#         c = input_int()
#         if c == 1:
#             self.choice_categ()
#
#     def choice_categ(self):
#         print('')
#         cat = input_int()
#         self.show_categ(cat)
#
#     def show_categ(self, cat):
#         print()
#         while True:
#
#             prod = input_int()
#             if prod == -1:
#                 break
#
#             self.show_product(prod)
#
#
#     def show_product(self, prod):
#         print(prod)
#         action = input_int()
#         if action == 3:
#             return
#
