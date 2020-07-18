#!/usr/bin/python3
# -*-coding: utf8 -*-

import json
import requests


class ApiSearch:

    def __init__(self):
        self.api_search_terms = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&json=1&search_terms="
        self.api_search_cat = "https://fr.openfoodfacts.org/categories.json"

    def search_product(self, name_product):
        """
        Search a product in Open Food Fact API and return the 1st product found

        """
        final_http = self.api_search_terms + name_product
        response = requests.get(final_http)
        response_text = json.loads(response.text)
        i = 0
        list_product = []
        while i < 2:
            path = response_text["products"][i]
            final_product = {"name": path["product_name"], "brand": path.get("brands", None),
                             "category": path.get("categories", None), "nutri_score": path.get("nutriscore_grade", None),
                             "store": path.get("stores", None), "ingredients": path.get("ingredients_text", None)}
            list_product.append(final_product)
            i += 1
        return list_product

    def search_cat(self, name_cat):
        response = requests.get(self.api_search_cat)
        response_text = json.loads(response.text)
        listcat = []
        for categories in response_text["tags"]:
            listcat.append(response_text["tags"][categories]["name"])
        for cat in listcat:
            if name_cat in listcat[cat]:
                return name_cat





