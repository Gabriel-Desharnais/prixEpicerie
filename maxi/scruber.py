#!/bin/python3
# -*- coding: utf-8 -*-

from . import products
import requests
import time

productUrlPrefix = "https://api.pcexpress.ca/product-facade/v4/products/"



def scrub(pIDs, rateLimit=0.5):
	"""Cette fonction accepte une liste de product id de maxi et recherche l'information à partir de l'api rateLimit max number of request per seconds aloud"""
	#TODO: mettre un paramètre écart-type pour créer de la variation dans les requête
	secTowait = 1/rateLimit
	# Créer les paramètres
	payload = {"lang": "fr",
			   "date": "28012023",
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
	scrubedData = []
	with requests.Session() as s:
		# Déterminer la clée de connection à l'api
		# TODO: se connecter au site et obtenir la clée de connection
		headers["x-apikey"] = "1im1hL52q9xvta16GlSdYDsTsG0dmyhF"
		for pID in pIDs:
			# Créer l'url
			productUrl = f"{productUrlPrefix}{products.UUIDToMaxiID[pID]}"
			# Effectuer la requète
			r = s.get(productUrl, params=payload, headers=headers)
			# Valider que la requète est réalisé avec succès
			if r.status_code != 200:
				scrubedData.append("NaN")
				continue
			res = r.json()
			try:
				scrubedData.append(f"{res['offers'][0]['price']['value']} $/{res['offers'][0]['price']['unit']}    {res['offers'][0]['wasPrice']['value']} $/{res['offers'][0]['wasPrice']['unit']}")
			except:
				scrubedData.append(f"{res['offers'][0]['price']['value']} $/{res['offers'][0]['price']['unit']}")
			time.sleep(secTowait)
	return scrubedData