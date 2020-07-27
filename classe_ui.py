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
    def __init__(self):
        """
        UserInterfaceManager class constructor.

        Parameters:

        """
        self.choice1 = None
        self.choice_cat = None
        self.choice_prod = None
        self.substitute = None
        self.save = None

    def first_choise(self):
        print("Que souhaitez-vous faire?"
              "1 : Quel aliment souhaitez-vous remplacer?"
              "2 : Retrouver mes aliments substitutés.")
        choice = input_int("Entrer le nombre correspondant à votre choix.")
        if choice == 1:
            self.choice1 = 1
        elif choice == 2:
            self.choice1 = 2

    def choice_category(self, list_cat):
        print("Voici la liste des catégories :")
        for cat in list_cat:
            print("{} : {}".format(cat["id"], cat["name"]))
        choice = input_int("Entrer le nombre correspondant à votre choix.")
        for cat in list_cat:
            if choice == cat["id"]:
                self.choice_cat = cat

    def choice_product(self, list_product):
        print("Voici la liste des aliments de la"
              " catégorie: {}".format(self.choice_cat))
        for prod in list_product:
            print("{} : {}, nutri-score = {}".format(prod["id"],
                                                     prod["name"],
                                                     prod["nutriscore"]))
        choice = input_int("Entrer le nombre correspondant à votre choix.")
        for prod in list_product:
            if choice == prod["id"]:
                self.choice_prod = prod

    def suggest_substitute(self, subm, psm, pcm, pm):
        list_substitute = subm.select_association(self.choice_prod["id"],
                                                  psm, pcm, pm)
        self.substitute = list_substitute[0]
        print("Voici le substitut proposé pour l'aliment que vous avez choisit")
        print("Substitue n°{}, nom: {}, nutriscore: {},\n "
              "url : {}".format(self.substitute["id"],
                                self.substitute["name"],
                                self.substitute["nutriscore"],
                                self.substitute["url"]))

    def save_substitute(self, pm, pcm, subm, product):
        """

        Parameters:
            pm : class ProductManager
                The manager of the Product table in the database.
            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.
            subm : class SubstituteManager
                The manager of the Substitute table in the database.
            product : dict
                The product to whiwh we want to associate a store.

        Returns:


        """
        list_product_bdd = pm.select()
        list_cat_product = pcm.select_association(product["id"])
        list_substitute_possible = []
        for prod in list_product_bdd:
            prod["category"] = pcm.select_association(prod["id"])
            for cat in prod["category"]:
                if cat in list_cat_product:
                    if prod["nutriscore"] < product["nutriscore"]:
                        list_substitute_possible.append(prod)
        if list_substitute_possible:
            for sub in list_substitute_possible:
                subm.insert_association(product["id"], sub["id"])
            self.save = True
        if not list_substitute_possible:
            self.save = False
