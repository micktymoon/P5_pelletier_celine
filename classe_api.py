import json
import requests


response = requests.get("https://fr.openfoodfacts.org/categories.json")
category = json.loads(response.text)
l = len(category["tags"])
print(l)
i = 0
listcat = []
while i < l:
    path = category["tags"][i]

    for item in path:
        if item == "name":
            listcat.append(path[item])

    i += 1
print(listcat)

