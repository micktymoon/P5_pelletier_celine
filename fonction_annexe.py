#!/usr/bin/python3
# -*-coding: utf8 -*-


def get_word_remove_spaces(text):
    """

    Parameters:
        text

    Returns:

    """
    list_words = text.split(",")
    list_without_spaces = []
    for word in list_words:
        word = word.strip()
        list_without_spaces.append(word)
    return list_without_spaces


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
    """Associate a category to a product in the database and the category
        to Categories table if it doesn't exist.

    Get a list of product categories.
    Checks if the product categories corresponds to one of the
     categories of the database, and if yes, associates the product with
     the category. But if the category doesn't exist in the Categories table
     of the database, insert the category in the table and then associate it
     with the product.

    Parameters:
        cm : class CategoryManager
            The manager of the Categories table in the database.
        pcm : class ProductCategoryManager
            The manager of the ProductCategory table in the database.
        product : dict
            The product to whiwh we want to associate a category.
     """
    product_cat = get_word_remove_spaces(product["category"])
    for cat in product_cat:
        check = cm.select(name=cat)
        if check is None:
            category = {"name": cat}
            cm.insert(category)
            pcm.insert_association(category["id"], product["id"])
        else:
            pcm.insert_association(check["id"], product["id"])


def associate_store_to_product(sm, psm, product):
    """Associate a store to a product in the database and the store to Store
        table if it doesn't exist.

        Get a list of product store.
        Checks if the product stores corresponds to one of the
         stores of the database, and if yes, associates the product with
         the store. But if the store doesn't exist in the Store table of
         the database, insert the store in the table and then associate it
         with the product.

        Parameters:
            sm : class StoreManager
                The manager of the Store table in the database.
            psm : class ProductStoreManager
                The manager of the ProductStore table in the database.
            product : dict
                The product to whiwh we want to associate a store.
         """
    product_store = get_word_remove_spaces(product["store"])
    for sto in product_store:
        check = sm.select(name=sto)
        if check is None:
            store = {"name": sto}
            sm.insert(store)
            psm.insert_association(store["id"], product["id"])
        else:
            psm.insert_association(check["id"], product["id"])


def associate_substitute_to_product(pm, pcm, subm, product):
    """

    Parameters
    ----------
    pm
    pcm
    subm
    product

    Returns
    -------

    """
    list_product_bdd = pm.select()
    list_cat_product = pcm.select_association(product["id"])
    list_substitute_possible = []
    for prod in list_product_bdd:
        prod["category"] = pcm.select_association(prod["id"])
        for cat in prod["category"]:
            if cat in list_cat_product:
                list_substitute_possible.append(prod)
    for sub in list_substitute_possible:
        if sub["nutriscore"] < product["nutriscore"]:
            subm.insert(product["id"], sub["id"])
    if list_substitute_possible:
        return True
    if not list_substitute_possible:
        return False


