#!/bin/python3
# -*- coding: utf-8 -*-

"""
Ce script permet d'importer une série de code zébré et de les ajouter à la base de donnée
"""
import pandas
import uuid
from pathlib import Path

productsku = pandas.read_csv("skutoadd.csv")
productsES = pandas.read_csv("produitses.csv")
products = pandas.read_csv("productTable.csv")

for sku in productsku["sku"]:
	match = products.loc[products['sku'] == sku]
	if len(match):
		# En cas de match on passe au produit suivant
		continue
	# Créer un uuid pour le nouveau produit
	u = uuid.uuid4()
	productsES.loc[len(productsES)] = [u,None]
	products.loc[len(products)] = [u, "", "", "", sku, "", []]

filepath = Path("produitses.csv")
productsES.to_csv(filepath, index=False)
filepath = Path("productTable.csv")
products.to_csv(filepath, index=False)