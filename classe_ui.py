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
    def __init__(self, cm, pm, pcm, psm, subm):
        """
        UserInterfaceManager class constructor.

        Parameters:

        """
        self.cm = cm
        self.pm = pm
        self.pcm = pcm
        self.psm = psm
        self.subm = subm
        self.choice1 = None
        self.choice_cat = None
        self.choice_prod = None
        self.substitute = None
        self.list_sub = None
        self.save = None

    def main_menu(self):
        while True:
            print("Que souhaitez-vous faire?"
                  "1 : Quel aliment souhaitez-vous remplacer?"
                  "2 : Retrouver mes aliments substitutés."
                  "3 : Quitter")
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            if choice == 1:
                self.choice_category()
            elif choice == 2:
                self.choice1 = 2
            elif choice == 3:
                print("A bientôt.")
                quit()

    def choice_category(self):
        while True:
            print("Voici la liste des catégories :")
            print("Entrez 0 si vous désirez quitter.")
            print("Entrez -1 si vous désirez retourner au menu précédent.")
            list_cat = self.cm.select()
            for cat in list_cat:
                print("{} : {}".format(cat["id"], cat["name"]))
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            for cat in list_cat:
                if choice == cat["id"]:
                    self.choice_product()
                elif choice == 0:
                    print("A bientôt.")
                    quit()
                elif choice == -1:
                    return

    def choice_product(self):
        print("Voici la liste des aliments de la"
              " catégorie: {}".format(self.choice_cat))
        print("Entrez 0 si vous désirez quitter.")
        print("Entrez -1 si vous désirez retourner au menu précédent.")
        list_product = self.pm.select()
        for prod in list_product:
            print("{} : {}, nutri-score = {}".format(prod["id"],
                                                     prod["name"],
                                                     prod["nutriscore"]))
        choice = input_int("Entrer le nombre correspondant à votre choix.")
        for prod in list_product:
            if choice == prod["id"]:
                list_sub = self.subm.associate_substitute_to_product(self.pm,
                                                                     self.pcm,
                                                                     choice)
                if list_sub:
                    for sub in list_sub:
                        print("Produit n°{}: {}, magasins où le trouver: {}, url "
                              "OpenFoodFact: {}.".format(sub["id"],
                                                         sub["name"],
                                                         sub["store"],
                                                         sub["url"]))
                    self.save_substitute(list_sub, self.subm, prod)
            elif choice == 0:
                print("A bientôt.")
                quit()
            elif choice == -1:
                return

    def suggest_substitute(self):
        list_substitute = self.subm.select_association(self.choice_prod["id"],
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

        # list_product_bdd = pm.select()
        # list_cat_product = pcm.select_association(product["id"])
        # list_substitute_possible = []
        # for prod in list_product_bdd:
        #     prod["category"] = pcm.select_association(prod["id"])
        #     for cat in prod["category"]:
        #         if cat in list_cat_product:
        #             if prod["nutriscore"] < product["nutriscore"]:
        #                 list_substitute_possible.append(prod)
        # if list_substitute_possible:
        print("Voulez vous sauvegarder les substitues? \n"
              )
        choice = input("Entrez 'o' pour oui ou 'n' pour non")
        if choice == "o":
            for sub in list_sub:
                subm.insert_association(product["id"], sub["id"])
            self.save = True
        if choice == "n":
            self.save = False
        # if not list_substitute_possible:
        #     self.save = False

    def show_substitute(self, subm, psm, pcm, pm):

        list_substituted_prod = subm.select_substituted_product()
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


class Toto(object):

    def main_menu(self):
        c = input_int()
        if c == 1:
            self.choice_categ()

    def choice_categ(self):
        print('')
        cat = input_int()
        self.show_categ(cat)

    def show_categ(self, cat):
        print()
        while True:

            prod = input_int()
            if prod == -1:
                break

            self.show_product(prod)


    def show_product(self, prod):
        print(prod)
        action = input_int()
        if action == 3:
            return

