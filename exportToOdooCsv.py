#!/bin/python3
# -*- coding: utf-8 -*-

"""Ce script exporte les produits dans la table produitses dans un fichier  csv
   qui pourra être importé dans Odoo par la suite"""

import pandas
from pathlib import Path

# Importer les donner dans les tables produitses et productTable
products = pandas.read_csv("productTable.csv")
productses = pandas.read_csv("produitses.csv")

# Créer le tableau qui servira à exporter les données
odoo = pandas.DataFrame(columns=["External ID", "Name", "Product Type", "Barcode", "Sales Price"])
for p in productses.values:
	# Aller
	u = p[0]
	prix = p[1]
	match = products.loc[products["uuid"] == u, ["nom", "sku"]].values
	if len(match) != 1:
		print("erreur", u)
		continue
	m = match[0]
	odoo.loc[len(odoo)] = [u, m[0], "Consumable", m[1], prix]

filepath  = Path("odooExport.csv")
odoo.to_csv(filepath, index=False)
