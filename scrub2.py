#!/bin/python3
# -*- coding: utf-8 -*-

import pandas
import maxi


products = pandas.read_csv("productTable.csv")

maxiProds = products.loc[products["maxi"] == True]
print(maxi.scrub(maxiProds["uuid"]))