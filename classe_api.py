import json
import requests


# response = requests.get("https://fr.openfoodfacts.org/categories.json")
# category = json.loads(response.text)
# l = len(category["tags"])
# print(l)
# i = 0
# listcat = []
# while i < l:
#     path = category["tags"][i]
#
#     for item in path:
#         if item == "name":
#             listcat.append(path[item])
#
#     i += 1
# print(listcat)


class ApiSearch:

    def __init__(self):
        self.api_search = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&json=1&search_terms="

    def search_product_by_cate(self, name_product):
        final_http = self.api_search + name_product
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
            if items == "nutriscore_grade":
                final_product["nutri_score"] = path["nutriscore_grade"]
            if items == "stores":
                final_product["store"] = path["stores"]
            if items == "ingredients_text":
                final_product["ingredients"] = path["ingredients_text"]
        return final_product


product = "prince"
blabla = ApiSearch()
prince = blabla.search_product_by_cate(product)
print(prince["category_id"])

