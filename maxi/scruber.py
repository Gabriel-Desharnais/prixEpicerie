#!/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import pandas
from pathlib import Path
import json

productUrlPrefix  = "https://api.pcexpress.ca/product-facade/v4/products/"

# Aller chercher les données dans la bd Maxi
products = pandas.read_csv("maxi/productMaxi.csv")


def search(searchList, rateLimit = 0.5):
	"""Cette fonction accepte une liste d'élément et recherche sur le site de maxi et retourne les résultat"""
	secTowait = 1/rateLimit
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
		"Host": "api.pcexpress.ca",
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "fr",
		"Accept-Encoding": "gzip, deflate, br",
		"Content-Type": "application/json",
		"Site-Banner": "maxi",
		"sentry-trace": "95acb99297f34a49b0362e30ad95242d-a68dea6816cee9f5-1",
		"Content-Length": "337",
		"Origin": "https://www.maxi.ca",
		"Connection": "keep-alive",
		"Referer": "https://www.maxi.ca/",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "cross-site"
	}
	payload = {"pagination":{"from":0,
							 "size":48},
			   "banner":"maxi",
			   "cartId":"992b8f34-fd35-48d2-8b5d-a1937b8f3829",
			   "lang":"fr",
			   "date":"11022023",
			   "storeId":"8922",
			   "pcId":None,
			   "pickupType":"STORE",
			   "offerType":"ALL",
			   "userData":{"domainUserId":"b7958a74-8fd7-42d9-a618-c5f12a850e5e",
			               "sessionId":"4c1f0c2e-17db-41b0-91e5-e94cc55c4177"}}
	# Convertir en set la liste
	searchList = set(searchList)
	searchResult = {}
	with requests.session() as s:
		headers["x-apikey"] = "1im1hL52q9xvta16GlSdYDsTsG0dmyhF"
		url = "https://api.pcexpress.ca/product-facade/v3/products/search"
		for term in searchList:
			payload["term"] = term
			#print(json.dumps(payload, separators=(',', ':')))
			#return
			r = s.post(url, data = json.dumps(payload, separators=(',', ':')), headers=headers)
			if r.status_code != 200:
				print(r.status_code, r.text)
				#scrubedData.append("NaN")
				continue
			results = r.json()
			if results["pagination"]["totalResults"] == 0:
				print("no proudct found for", term, "continuing")
				continue
			elif results["pagination"]["totalResults"] > 1:
				print("found", results["pagination"]["totalResults"], "match continuing")
				continue
			prod = results["results"][0]
			maxiId = prod["code"]
			nom = prod["name"]
			description = prod.get("description", "")
			marque = prod["brand"]
			format = prod["packageSize"]
			prix = prod["prices"]["price"]["value"]
			unite = prod["prices"]["price"]["unit"]
			time.sleep(secTowait)
			searchResult[term] = {"nom":nom, 
								  "description":description, 
								  "marque":marque,  
								  "format": format,
								  "maxiId": maxiId,
								  "prix": prix,
								  "unite": unite}
		return searchResult


def scrub(pIDs, rateLimit=0.5):
	"""Cette fonction accepte une liste de product id de maxi et recherche l'information à partir de l'api rateLimit max number of request per seconds aloud"""
	#TODO: mettre un paramètre écart-type pour créer de la variation dans les requête
	secTowait = 1/rateLimit
	# Créer les paramètres
	payload = {"lang": "fr",
			   "date": "07032023",
			   "pickupType": "STORE",
			   "storeId": "8922",
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
			# TODO Déterminer si le produit est en rabais
			normalPrice = res['offers'][0]['wasPrice']
			if normalPrice is None:
				productInfoMaxi["type_de_prix"].values[0] = "régulier"
			else:
				productInfoMaxi["type_de_prix"].values[0] = "rabais"
			print(res['offers'][0]['price']['value'])
			products.loc[products['uuid'] == pID] = productInfoMaxi
			scrubedData[pID] = {"nom":res["name"], 
								"description":res.get("description", ""), 
								"marque":res.get("brand", ""), 
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