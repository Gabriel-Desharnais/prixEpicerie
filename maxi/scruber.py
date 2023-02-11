#!/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import pandas
from pathlib import Path

productUrlPrefix = "https://api.pcexpress.ca/product-facade/v4/products/"

# Aller chercher les données dans la bd Maxi
products = pandas.read_csv("maxi/productMaxi.csv")


def scrub(pIDs, rateLimit=0.5):
	"""Cette fonction accepte une liste de product id de maxi et recherche l'information à partir de l'api rateLimit max number of request per seconds aloud"""
	#TODO: mettre un paramètre écart-type pour créer de la variation dans les requête
	secTowait = 1/rateLimit
	# Créer les paramètres
	payload = {"lang": "fr",
			   "date": "11022023",
			   "pickupType": "STORE",
			   "storeId": "8797",
			   "banner": "maxi"}
	# Créer les headers
	# TODO: Varié les user-Agent de manière réaliste
	headers = {"Host": "api.pcexpress.ca",
			  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
			  "Accept": "application/json, text/plain, */*",
			  "Accept-Language": "fr",
			  "Accept-Encoding": "gzip, deflate, br",
			  "Site-Banner": "maxi",
			  "Content-Type": "application/json",
			  "Origin": "https://www.maxi.ca",
			  "Connection": "keep-alive",
			  "Referer": "https://www.maxi.ca/",
			  "Sec-Fetch-Dest": "empty",
			  "Sec-Fetch-Mode": "cors",
			  "Sec-Fetch-Site": "cross-site",
			  "Pragma": "no-cache",
			  "Cache-Control": "no-cache"}
	# Créer la session de requests
	scrubedData = {}
	with requests.Session() as s:
		# Déterminer la clée de connection à l'api
		# TODO: se connecter au site et obtenir la clée de connection
		headers["x-apikey"] = "1im1hL52q9xvta16GlSdYDsTsG0dmyhF"
		for pID in pIDs:
			productInfoMaxi = products.loc[products['uuid'] == pID]
			# Créer l'url
			productUrl = f"{productUrlPrefix}{productInfoMaxi['id_interne'].values[0]}"
			print(productUrl)
			# Effectuer la requète
			r = s.get(productUrl, params=payload, headers=headers)
			# Valider que la requète est réalisé avec succès
			if r.status_code != 200:
				print(r.status_code, r)
				#scrubedData.append("NaN")
				continue
			res = r.json()
			productInfoMaxi["prix"].values[0] = res['offers'][0]['price']['value']
			productInfoMaxi["unité"].values[0] = res['offers'][0]['price']['unit']
			print(res['offers'][0]['price']['value'])
			products.loc[products['uuid'] == pID] = productInfoMaxi
			scrubedData[pID] = {"nom":res["name"], 
								"description":res.get("description", ""), 
								"marque":res["brand"], 
								"sku":None, 
								"format":res["packageSize"]}
			#scrubedData[pID](f"{res['offers'][0]['price']['value']} $/{res['offers'][0]['price']['unit']}    {res['offers'][0]['wasPrice']['value']} $/{res['offers'][0]['wasPrice']['unit']}")
			#scrubedData[pID](f"{res['offers'][0]['price']['value']} $/{res['offers'][0]['price']['unit']}")
			
			time.sleep(secTowait)
	
	# Update db
	print(products)
	filepath = Path("maxi/productMaxi.csv")
	products.to_csv(filepath, index=False)
	return scrubedData