import json
import requests


class ApiSearch:

    def __init__(self):
        self.api_search_terms = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&json=1&search_terms="
        self.api_search_cat = "https://fr.openfoodfacts.org/categories.json"

    def search_product(self, name_product):
        final_http = self.api_search_terms + name_product
        response = requests.get(final_http)
        response_text = json.loads(response.text)
        path = response_text["products"][0]
        final_product = {}
        for items in path:
            if items == "product_name":
                final_product["name"] = path["product_name"]
            if items == "brands":
                final_product["brand"] = path["brands"]
            if items == "categories_tags":
                if "en:beverages" in path["categories_tags"]:
                    final_product["category_id"] = 22
                elif "en:snacks" in path["categories_tags"]:
                    final_product["category_id"] = 23
                elif "en:pizzas" in path["categories_tags"]:
                    final_product["category_id"] = 24
                elif "en:desserts" in path["categories_tags"]:
                    final_product["category_id"] = 25
                elif "en:cheeses" in path["categories_tags"]:
                    final_product["category_id"] = 26
                else:
                    final_product["category_id"] = None

            if items == "nutriscore_grade":
                final_product["nutri_score"] = path["nutriscore_grade"]
            if items == "stores":
                final_product["store"] = path["stores"]
            if items == "ingredients_text":
                final_product["ingredients"] = path["ingredients_text"]
        return final_product

    def search_cat(self, name_cat):
        response = requests.get(self.api_search_cat)
        response_text = json.loads(response.text)
        len_response_text = len(response_text["tags"])
        i = 0
        listcat = []
        while i < len_response_text:
            path = response_text["tags"][i]
            for item in path:
                if item == "name":
                    listcat.append(path[item])
            i += 1
        x = 0
        list_cat_find = []
        while x < len(listcat):
            if name_cat in listcat[x]:
                list_cat_find.append(listcat[x])
            x += 1
        return list_cat_find




