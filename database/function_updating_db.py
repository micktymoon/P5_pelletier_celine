#!/usr/bin/python3
# -*-coding: utf8 -*-


def get_store_and_add_to_db(sm, text):
    """
    Retrieves the stores of a text and adds them to the database.

    Get the stores from a text and put them in a list.
    And if any stores of the list aren't in the database, the fonction
    insert them in the database.

    Parameters:
        sm : class StoreManager
            The Manager of the Categories table in the database.
        text : str
            The text from which we want to retrieve the stores.
    """
    store_db = sm.select()
    list_store_db = []
    for sto in store_db:
        list_store_db.append(sto["name"])
    for word in text:
        word = word.strip()
        store = {"name": word}
        if store["name"] not in list_store_db:
            sm.insert(store)


def associate_cat_to_product(cm, pcm, product):
    """
    Associate a category to a product in the database and the category
     to Categories table if it doesn't exist.

    Get a list of product categories.
    Checks if the product categories corresponds to one of the
     categories of the database, and if yes, associates the product with
     the category.
    But if the category doesn't exist in the Categories table
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
    for cat in product["category"]:
        check = cm.select(name=cat)
        if check is None:
            category = {"name": cat}
            cm.insert(category)
            pcm.insert_association(category["id"], product["id"])
        else:
            pcm.insert_association(check["id"], product["id"])


def associate_store_to_product(sm, psm, product):
    """
    Associate a store to a product in the database and the store to Store
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
    for sto in product["store"]:
        check = sm.select(name=sto)
        if check is None:
            store = {"name": sto}
            sm.insert(store)
            psm.insert_association(store["id"], product["id"])
        else:
            psm.insert_association(check["id"], product["id"])


def insert_product_db(pm, cm, sm, pcm, psm, prod):
    """
    Insert a given product in the database.

    Retrieve the product stores and insert them into the database.
    Insert the product in the database.
    Associates the product with its stores.
    Retrieves the product categories and associates them with it.
    And return the product.

    Parameters:
        pm : class ProductManager
            The manager of the Product table in the database.

        cm : class CategoryManager
            The manager of the Categories table in the database.

        sm : class StoreManager
            The Manager of the Categories table in the database.

        pcm : class ProductCategoryManager
            The manager of the ProductCategory table in the database.

        psm : class ProductStoreManager
            The manager of the ProductStore table in the database.

        prod : dict
            The product that we want to insert into the database.

    Returns:
        dict
            The product that has been inserted into the database.
    """
    get_store_and_add_to_db(sm, prod["store"])
    product = pm.insert(pcm, psm, product=prod)
    associate_store_to_product(sm, psm, product)
    product["store"] = psm.select_asso_with_id_prod(product["id"])
    associate_cat_to_product(cm, pcm, product)
    product["category"] = pcm.select_asso_with_id_prod(product["id"])
    return product
