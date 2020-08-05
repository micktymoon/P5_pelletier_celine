#!/usr/bin/python3
# -*-coding: utf8 -*-

import json
import requests
from tool_function import get_word_remove_spaces


class ApiManageSearch:
    """
    Class that manages the search in the OpenFoodFact API.

    Methods:
        search_product()
            Search a product in OpenFoodFact API and return the first three
             products found.
    """

    def __init__(self):
        """ ApiManagerSearch class constructor."""
        self.api_search_terms = "https://fr.openfoodfacts.org/cgi/search.pl?" \
                                "action=process&json=1&search_terms="

    def search_product(self, name_product):
        """
        Search a product in OpenFoodFact API and return a list of products
         found.

        Complete the link with the name of the product we are looking for,
         search for the corresponding products and return a list of products
         found.

        Parameters:
            name_product: str
                The name of the product we're looking for.

        Returns:
            list
                A list of products found by the API.
        """
        final_http = self.api_search_terms + name_product
        response = requests.get(final_http)
        response_text = json.loads(response.text)
        i = 0
        product_list = []
        while i < len(response_text):
            try:
                path = response_text["products"][i]
                final_product = {"name": path["product_name"],
                                 "brand": path.get("brands", None),
                                 "category": get_word_remove_spaces(path.get("categories", None)),
                                 "nutriscore": path.get(
                                     "nutriscore_grade", None),
                                 "store": get_word_remove_spaces(path.get("stores", None)),
                                 "ingredients": path.get(
                                     "ingredients_text", None),
                                 "url": path.get("url", None)}
                if final_product["url"] is None:
                    start = "https://fr.openfoodfacts.org/produit/"
                    id_prod = path["code"]
                    final_product["url"] = start + id_prod
                product_list.append(final_product)
                i += 1
            except IndexError:
                i += 1
                pass
        return product_list
