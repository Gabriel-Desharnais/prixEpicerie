#!/bin/python3
# -*- coding: utf-8 -*-
#import products
import uuid
import pandas
from pathlib import Path

# Import data
productMaxi = pandas.read_csv("productMaxi.csv")
productTable = pandas.read_csv("../productTable.csv")


IDs = ["21290213_EA", "21289774_EA", '20913404_EA']
toAdd = set()
for id in IDs:
	match = productMaxi.loc[productMaxi['id_interne'] == id]
	if len(match) == 0:
		toAdd.add(id)

for id in toAdd:
	u = uuid.uuid4()
	productMaxi.loc[len(productMaxi)] = [u, id, None, ""]
	productTable.loc[len(productTable)] = [u, "", "", "", "", "", []]

# Export data
filepath = Path("productMaxi.csv")
productMaxi.to_csv(filepath, index=False)
filepath = Path("../productTable.csv")
productTable.to_csv(filepath, index=False)

print(toAdd, "added\n\n\n\n")