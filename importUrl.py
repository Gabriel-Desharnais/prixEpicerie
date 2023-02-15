#!/bin/python3
# -*- coding: utf-8 -*-


import pandas
import uuid
from pathlib import Path

batch = pandas.read_csv("batchimport.csv")
maxi = []
for u in batch["url"].values:
	if "maxi" in u:
		id = u.split("/")[-1]
		maxi.append(id)

maxiProduct = pandas.read_csv("maxi/productMaxi.csv")
products = pandas.read_csv("productTable.csv")
print()
for id in maxi:
	if len(maxiProduct.loc[maxiProduct["id_interne"] == id]) == 0:
		print("trouvé")
		uid = uuid.uuid4()
		maxiProduct.loc[len(maxiProduct), ["uuid", "id_interne"]] = [uid, id]

		products.loc[len(products), ["uuid", "maxi"]] = [uid, True]

filepath = Path("productTable.csv")
products.to_csv(filepath, index=False)

filepath = Path("maxi/productMaxi.csv")
maxiProduct.to_csv(filepath, index=False)