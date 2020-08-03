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
                self.substitute_menu()
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
                self.choice_product(found)

    def choice_product(self, category):
        while True:
            print("Voici la liste des aliments de la"
                  " catégorie: {}".format(category["name"]))
            print("Entrez -1 si vous désirez retourner au menu précédent.")
            list_product = self.pcm.select_association_with_cat(category["name"])
            for prod in list_product:
                print("{} : {}, nutri-score = {}".format(prod["id"],
                                                         prod["name"],
                                                         prod["nutriscore"]))
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            for prod in list_product:
                if choice == prod["id"]:
                    self.show_sub_of_choosen_prod(prod)
                elif choice == -1:
                    return

    def show_sub_of_choosen_prod(self, prod):
        list_sub = self.subm.associate_substitute_to_product(self.pm,
                                                             self.pcm,
                                                             self.psm,
                                                             prod)
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
            print("Désolé nous n'avons pas trouvé de substitut pour ce produit.")
            return

    def substitute_menu(self):
        choice = self.show_substitute(self.subm, self.psm, self.pcm, self.pm)
        for prod in self.list_sub:
            if choice == prod["id"]:
                self.suggest_substitute(prod)
            elif choice == -1:
                return

    def suggest_substitute(self, product):
        list_substitute = self.subm.select_association_with_id_prod(product["id"],
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
                self.list_sub = subm.select_association_with_id_prod(product["id"],
                                                                     psm, pcm, pm)
                return product["id"]
