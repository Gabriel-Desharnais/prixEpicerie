#!/bin/python3
# -*- coding: utf-8 -*-

"""Ce module cherche via l'api de maxi les termes dans leur produits"""

import pandas
import maxi
from pathlib import Path


# maxi.search(["059749969420", "055742561951", "064420254016", "055872025019"])






products = pandas.read_csv("productTable.csv")
maxiProducts = pandas.read_csv("maxi/productMaxi.csv")

productToSearch = products.loc[products["maxi"] == False]

#print(productToSearch)
#exit()
res = maxi.search(productToSearch["sku"])
for sku, info in res.items():

	uid = products.loc[products["sku"] == sku]["uuid"].values[0]
	# update maxi table
	if len(maxiProducts.loc[maxiProducts["uuid"] == uid])<1:
		maxiProducts.loc[len(maxiProducts)] = [uid, info["maxiId"], info["prix"], info["unite"]]
	elif len(maxiProducts.loc[maxiProducts["uuid"] == uid])==1:
		maxiProducts.loc[maxiProducts["uuid"] == uid] = [uid, info["maxiId"], info["prix"], info["unite"]]
	else:
		print("erreur too much uuid")
	# update product table
	if len(products.loc[products["uuid"] == uid]) == 1:
		fi = [info["nom"], info["description"], info["marque"], info["format"], True, False]
		products.loc[products["uuid"] == uid, ["nom","description","marque","Format","maxi","taxable"]] = fi


filepath = Path("productTable.csv")
products.to_csv(filepath, index=False)

filepath = Path("maxi/productMaxi.csv")
maxiProducts.to_csv(filepath, index=False)

#maxiProds = products.loc[products["maxi"] == True]
#infoReturned = maxi.scrub(maxiProds["uuid"])
#for uuid, info in infoReturned.items():
#	fi = [info["nom"], info["description"], info["marque"], info["format"]]
#	products.loc[products["uuid"] == uuid, ["nom","description","marque","Format"]] = fi
	# TODO: ajouter une logique pour si il y a plus d'un uuid pareil

#filepath = Path("productTable.csv")
#products.to_csv(filepath, index=False)