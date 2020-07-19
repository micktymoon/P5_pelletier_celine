#!/usr/bin/python3
# -*-coding: utf8 -*-


def get_store_and_add_to_db(sm, text):
    """Retrieves the stores of a text and adds them to the database.

    Get the stores from a text and put them in a list.
    And if any stores of the list aren't in the database, the fonction
    insert them in the database.

    Parameters:
        sm : class StoreManager
            The Manager of the Categories table in the database.
        text : str
            The text from which we want to retrieve the stores.
    """
    list_words = text.split(",")
    store_db = sm.select()
    list_store_db = []
    for sto in store_db:
        list_store_db.append(sto["name"])
    for word in list_words:
        word = word.strip()
        store = {"name": word}
        if store["name"] not in list_store_db:
            sm.insert(store)


def associate_cat_to_product(cm, pcm, product):
    """Associate a category to a product in the database

    Get the product categories and the categories of the database.
    Checks if one of the product categories corresponds to one of the
     categories of the database, and if yes, associates the product with
     the category.

    Parameters:
        cm : class CategoryManager
            The manager of the Categories table in the database.
        pcm : class ProductCategoryManager
            The manager of the ProductCategory table in the database.
        product : dict
            The product to whiwh we want to associate a category.
     """
    product_cat = product["category"].split(",")
    product_cat_strip = []
    for cat in product_cat:
        cat = cat.strip()
        product_cat_strip.append(cat)
    list_cat_db = cm.select()
    for cat in list_cat_db:
        for cat_prod in product_cat_strip:
            if cat_prod == cat["name"]:
                pcm.insert_product_category(cat["id"], product["id"])
                return True


def associate_store_to_product(sm, psm, product):
    """Associate a store to a product in the database

        Get the product store and the stores of the database.
        Checks if one of the product stores corresponds to one of the
         stores of the database, and if yes, associates the product with
         the store.

        Parameters:
            sm : class StoreManager
                The manager of the Store table in the database.
            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.
            product : dict
                The product to whiwh we want to associate a store.
         """
    product_store = product["store"].split(",")
    product_store_strip = []
    for sto in product_store:
        sto = sto.strip()
        product_store_strip.append(sto)
    list_store_db = sm.select()
    for store in list_store_db:
        for prod_store in product_store_strip:
            if prod_store == store["name"]:
                psm.insert_product_store(store["id"], product["id"])
                return True