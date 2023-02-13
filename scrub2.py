#!/bin/python3
# -*- coding: utf-8 -*-

import pandas
import maxi
from pathlib import Path


products = pandas.read_csv("productTable.csv")
#products["maxi"] = products["maxi"].astype("bool")


maxiProds = products.loc[products["maxi"] == True]
infoReturned = maxi.scrub(maxiProds["uuid"])
for uuid, info in infoReturned.items():
	fi = [info["nom"], info["description"], info["marque"], info["format"]]
	products.loc[products["uuid"] == uuid, ["nom","description","marque","Format"]] = fi
	# TODO: ajouter une logique pour si il y a plus d'un uuid pareil

filepath = Path("productTable.csv")
products.to_csv(filepath, index=False)