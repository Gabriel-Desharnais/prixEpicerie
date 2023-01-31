#!/bin/python3
# -*- coding: utf-8 -*-
 
"""Ce script utilise le module maxi pour importer les données scrubé sur le site de maxi"""
import maxi
import products_info
pInfo = maxi.scrub(products_info.UUIDToName.keys())
for name, price in zip(products_info.UUIDToName.values(), pInfo):
	print(name,":\t\t" , price)