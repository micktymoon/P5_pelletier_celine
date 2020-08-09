#!/usr/bin/python3
# -*-coding: utf8 -*-

from tool_function import input_int


class UserInterfaceManager:
    """
    Class which manages the user interface.

    Attributes:
        cm : class CategoryManager
            The manager of the Categories table in the database.

        pm : class ProductManager
            The manager of the Product table in the database.

        sm : class StoreManager
            The Manager of the Categories table in the database.

        pcm : class ProductCategoryManager
            The manager of the ProductCategory table in the database.

        psm : class ProductStoreManager
            The manager of the ProductStore table in the database.

        subm : class SubstituteManager
            The manager of the Substitute table in the database.

        api : Class ApiManagerSearch
            The manager of the OpenFoodFact API research manager.

    Methods:
        main_menu()
            Displays the first possible choice for the user.

        category_choice()
            Displays the categories the user can choose from.

        product_choice(category)
            Displays the products of the chosen category.

        show_sub_of_choosen_prod(prod)
            Displays possible substitutes for the chosen product.

        save_substitute(list_sub, subm, product)
            Save the substitutes for the chosen product in the database.

        substitute_menu()
            Displays the choice of products already substituted.

        suggest_substitute(product)
            Displays the substitutes for the chosen product.
    """
    def __init__(self, cm, pm, sm, pcm, psm, subm, api):
        """
        UserInterfaceManager class constructor.

        Parameters:
            cm : class CategoryManager
                The manager of the Categories table in the database.

            pm : class ProductManager
                The manager of the Product table in the database.

            sm : class StoreManager
                The Manager of the Categories table in the database.

            pcm : class ProductCategoryManager
                The manager of the ProductCategory table in the database.

            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.

            subm : class SubstituteManager
                The manager of the Substitute table in the database.

            api : Class ApiManagerSearch
                The manager of the OpenFoodFact API research manager.
        """
        self.cm = cm
        self.pm = pm
        self.sm = sm
        self.pcm = pcm
        self.psm = psm
        self.subm = subm
        self.api = api
        self.substitute = None
        self.list_sub = None

    def main_menu(self):
        """
        Displays the first possible choice for the user.

        Offers three possible choices to the user.
        If the choice is 1, then it redirects to the choice of categories.
        If the choice is 2, then it redirects to the choice of products
         already substituted.
        If the choice is 3, then it stops the program.
        """
        while True:
            print("============================================== \n"
                  "MENU PRINCIPAL: \n"
                  "Que souhaitez-vous faire?\n"
                  "1 : Quel aliment souhaitez-vous remplacer?\n"
                  "2 : Retrouver mes aliments substitutés.\n"
                  "3 : Quitter \n"
                  "============================================== \n")
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            if choice == 1:
                self.category_choice()
            elif choice == 2:
                self.substitute_menu()
            elif choice == 3:
                print("A bientôt.")
                break

    def category_choice(self):
        """
        Displays the categories the user can choose from.

        Offers the user to choose a category.
        If the choice is -1, then it returns to the previous menu.
        If the choice corresponds to the ID of a category, then it redirects
         to the choice of products in this category.

        Returns:
            None
        """
        while True:
            print("============================================== \n"
                  "Voici la liste des catégories :\n"
                  "============================================== \n"
                  "Entrez -1 si vous désirez retourner au menu précédent.\n")
            list_cat = self.cm.select()
            for cat in list_cat:
                print("{} : {}".format(cat["id"], cat["name"]))
            print("============================================== \n")
            choice = input_int("Entrer le nombre correspondant à votre choix.")
            if choice == -1:
                return
            found = None
            for cat in list_cat:
                if choice == cat["id"]:
                    found = cat
                    break
            if found:
                self.product_choice(found)

    def product_choice(self, category):
        """
        Displays the products of the chosen category.

        Offers the user to choose a product from the previously chosen
         category.
        If the choice is -1, then it returns to the previous menu.
        If the choice matches the ID of a product, then it redirects to
         the display of possible substitutes for that product.

        Parameters:
            category: dict
                The category chosen in the previous menu.

        Returns:
            None
        """
        while True:
            print("\n============================================== \n"
                  "Voici la liste des aliments de la"
                  " catégorie: {}".format(category["name"]))
            print("============================================== \n"
                  "Entrez -1 si vous désirez retourner au menu précédent.\n")
            list_product = self.pcm.select_asso_with_cat(category["name"])
            for prod in list_product:
                print("{} : {}, nutri-score = {}".format(prod["id"],
                                                         prod["name"],
                                                         prod["nutriscore"]))
            choice = input_int("\nEntrez le nombre correspondant à "
                               "votre choix.")
            for prod in list_product:
                if choice == prod["id"]:
                    self.show_sub_of_choosen_prod(prod)
                elif choice == -1:
                    return

    def show_sub_of_choosen_prod(self, prod):
        """
        Displays possible substitutes for the chosen product.
        Retrieves a list of possible substitutes for the chosen product.
        If the list is full, then displays the substitutes and redirects
         to the choice to save or not these substitutes.
        If the list is empty then displays a message saying that no substitute
         could be found.
        Parameters:
            prod: dict
                The product for which we want to find substitutes.

        Returns:
            None
        """
        list_sub = self.subm.associate_sub_to_prod(self.pm,
                                                   self.cm,
                                                   self.sm,
                                                   self.pcm,
                                                   self.psm,
                                                   self.api,
                                                   prod)
        if list_sub:
            list_sub.sort(key=lambda d: d["nutriscore"])
            print("\n============================================== \n"
                  "Voici la liste des substituts du produit: "
                  "{}\n".format(prod["name"]))
            for sub in list_sub:
                print("Produit n°{}: {}, magasins où le trouver: {}, "
                      "nutri-score: {}, url OpenFoodFact: "
                      "{}.".format(sub["id"],
                                   sub["name"],
                                   sub["store"],
                                   sub["nutriscore"],
                                   sub["url"]))
            print("============================================== \n")
            self.save_substitute(list_sub, prod)
        if not list_sub:
            print("============================================== \n"
                  "Désolé nous n'avons pas trouvé de substitut pour ce "
                  "produit.\n"
                  "============================================== \n")
            return

    def save_substitute(self, list_sub, product):
        """
        Save the substitutes for the chosen product in the database.

        Offers the user to save the substitutes found.
        If the choice is 'o', then save the substitutes in the database.
        If the choice is 'n', then do not save the substitutes and return to
         the previous menu.

        Parameters:
            list_sub : list
                The list of substitute possible.

            product : dict
                The product whose substitutes we want to save.

        Returns:
            None
        """
        while True:
            print("Voulez vous sauvegarder les substitues?")
            choice = input("Entrez 'o' pour oui ou 'n' pour non.")
            if choice == "o":
                for sub in list_sub:
                    self.subm.insert_association(product["id"], sub["id"])
                print("\nSauvegarde des substituts effectuée.")
                return
            if choice == "n":
                print("\nSubstituts non sauvegardés.")
                return
            print("============================================== \n")

    def substitute_menu(self):
        """
        Displays the choice of products already substituted.

        Retrieves the products already replaced from the database in a list
         and displays them.
        Offers the user to choose a product from the list.
        If the choice is -1, then redirects to the previous menu.
        If the choice corresponds to the ID of one of the products in the
         list, then display its substitutes.

        Returns:
            None
        """
        list_substituted_prod = self.subm.select_substituted_product()
        print("============================================== \n"
              "\nVoici les produits ayant un substitut:\n")
        for product in list_substituted_prod:
            print("Produit n°{}: {}".format(product["id"], product["name"]))
        choice = input_int("\nEntrez le nombre du produit dont vous voulez "
                           "voir les susbtituts.")
        for product in list_substituted_prod:
            if choice == product["id"]:
                self.suggest_substitute(product)
            if choice == -1:
                return

    def suggest_substitute(self, product):
        """
        Displays the substitutes for the chosen product.

        Displays the substitutes saved in the database for the chosen product.

        Parameters:
            product : dict
                The product for which we want to see the substitutes.
        """
        list_substitute = self.subm.select_association(product["id"],
                                                       self.pcm,
                                                       self.psm)
        print("============================================== \n"
              "Voici les substituts sauvegardés pour "
              ": {}.".format(product["name"]))
        for sub in list_substitute:
            print("Produit n°{}, nom: {}, nutriscore: {},\n "
                  "url : {}".format(sub["id"],
                                    sub["name"],
                                    sub["nutriscore"],
                                    sub["url"]))
        print("============================================== \n")
