#!/bin/python3
# -*- coding: utf-8 -*-
 
"""Ce script utilise le module maxi pour importer les données scrubé sur le site de maxi"""
from openpyxl import Workbook
from openpyxl import styles
import pandas

produitsEs = pandas.read_csv("produitses.csv",na_filter=False)
productTable = pandas.read_csv("productTable.csv",na_filter=False)
productEquivalency = pandas.read_csv("productEquivalency.csv")


wb = Workbook()
# Activer le classeur
wb.active
# Créer la feuille du rapport
rapport = wb.create_sheet("Analyse",0)
# Ajouter l'entête du tableau
rapport["A1"] = "Produits ?picerie solidaire"
rapport["J1"] = "Produits concurence"
rapport.merge_cells("A1:I1")
rapport.merge_cells("J1:S1")
rapport["A1"].fill = styles.PatternFill(start_color="bf819e", end_color="bf819e", fill_type="solid")
rapport["J1"].fill = styles.PatternFill(start_color="ffe994", end_color="ffe994", fill_type="solid")

rapport["A2"] = "Nom du produit"
rapport["B2"] = "Marque"
rapport["C2"] = "Numéro de produit interne"
rapport["D2"] = "Format"
rapport["E2"] = "Description"
rapport["F2"] = "Prix"
rapport["G2"] = "Unité"
rapport["H2"] = "Prix unitaire"
rapport["I2"] = "Unité"
rapport["J2"] = "Épicerie"
rapport["K2"] = "Nom du produit"
rapport["L2"] = "Marque"
rapport["M2"] = "Numéro de produit"
rapport["N2"] = "Format"
rapport["O2"] = "Description"
rapport["P2"] = "Prix"
rapport["Q2"] = "Unité"
rapport["R2"] = "Prix unitaire"
rapport["S2"] = "Unité"

# Préparer la liste des produit à vérifier
pToLookUp = set(range(6))
#for prod in products_info.produitES:
#	pToLookUp |= products_info.equivalencyTable.get(prod, set())

#pInfo = maxi.scrub(pToLookUp)
#----------------- Simuler les réponses des épiceries ------------------
pInfo = []
for i, p in enumerate(pToLookUp):
	pInfo.append({"Épicerie": "Maxi",
				"nom": "lait 2%",
				"Marque": f"blabla{i}",
				"ndp":"sfsfweerwerewrwerfsfsdffffssfsdfewrwrresdfasdfsdafadf"[6*i:6*i+6],
				"Format":"1L",
				"description":"lait",
				"prix": str(2.15+0.10*i),
				"unité p": "ch",
				"prix unitaire": str((2.05+0.10*i)/10),
				"unité pu" :"/100ml"})

for i, p in enumerate(pToLookUp):
	pInfo.append({"Épicerie": "superC",
				"nom": "lait 2%",
				"Marque": f"blabla{i}",
				"ndp":"sfsfweerwerewrwerfsfsdffffssfsdfewrwrresdfasdfsdafadf"[6*i:6*i+6],
				"Format":"1L",
				"description":"lait",
				"prix": str(2.15+0.10*i),
				"unité p": "ch",
				"prix unitaire": str((2.15+0.10*i)/10),
				"unité pu" :"/100ml"})
#----------------- fin simulation ----------------

startRow = 3
for pes in produitsEs.values:
	uuid = pes[0]
	# Trouver le produit dans la bd producttable
	match = productTable.loc[productTable["uuid"] == uuid,["nom", "marque", "Format", "description"]].values
	if len(match) != 1:
		continue
	match = match[0]
	endRow = startRow + len(pInfo) - 1
	rapport.cell(startRow, 1, match[0]).alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=1, end_row=endRow, end_column=1)
	rapport.cell(startRow, 2, match[1]).alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=2, end_row=endRow, end_column=2)
	rapport.cell(startRow, 3, uuid).alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=3, end_row=endRow, end_column=3)
	rapport.cell(startRow, 4, match[2]).alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=4, end_row=endRow, end_column=4)
	rapport.cell(startRow, 5, match[3]).alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=5, end_row=endRow, end_column=5)
	rapport.cell(startRow, 6, pes[1]).alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=6, end_row=endRow, end_column=6)
	rapport.cell(startRow, 7, "ch").alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=7, end_row=endRow, end_column=7)
	rapport.cell(startRow, 8, "").alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=8, end_row=endRow, end_column=8)
	rapport.cell(startRow, 9, "/100ml").alignment = styles.Alignment(vertical='center')
	rapport.merge_cells(start_row=startRow, start_column=9, end_row=endRow, end_column=9)


	esPrice = float("2.15")
	# Ajouter les produits équivalents
	smallestPrice = None
	spl = []
	for i, p in enumerate(pInfo):
		rapport.cell(startRow+i, 10, p["Épicerie"])
		rapport.cell(startRow+i, 11, p["nom"])
		rapport.cell(startRow+i, 12, p["Marque"])
		rapport.cell(startRow+i, 13, p["ndp"])
		rapport.cell(startRow+i, 14, p["Format"])
		rapport.cell(startRow+i, 15, p["description"])
		rapport.cell(startRow+i, 16, p["prix"])
		rapport.cell(startRow+i, 17, p["unité p"])
		rapport.cell(startRow+i, 18, p["prix unitaire"])
		rapport.cell(startRow+i, 19, p["unité pu"])
		# Vérifié si le moins chers
		price  = float(p["prix"])
		if smallestPrice is None or smallestPrice > price:
			#Nouveau meilleur prix
			smallestPrice = price
			spl = [startRow+i]
		elif smallestPrice == price:
			spl.append(startRow + i)




	side = styles.Side(border_style="thick", color="000000")
	border = styles.Border(top=side,left=side,right=side, bottom=side)

	sideToBorder = ["top", "right", "bottom", "left"]
	row = startRow
	column = 1
	for s in range(4):
		rapport.cell(row,column).border = styles.Border(**{sideToBorder[s]: side, sideToBorder[s-1]: side})
		if s%2:
			borderLen = len(pInfo) - 2
		else:
			borderLen = 17
		match s:
			case 0:
				column += 1
			case 1:
				row += 1
			case 2:
				column -= 1
			case 3:
				row -= 1
		for i in range(borderLen):
			rapport.cell(row,column).border = styles.Border(**{sideToBorder[s]: side})
			match s:
				case 0:
					column += 1
				case 1:
					row += 1
				case 2:
					column -= 1
				case 3:
					row -= 1

	# Ajouter la couleur pour le produit le moins chers
	# Est-ce que es a le meilleur prix
	if esPrice <= smallestPrice:
		# Youpi on a le meilleur prix mettre le produit en vert
		couleur = styles.PatternFill(start_color="81d41a", end_color="81d41a", fill_type="solid")
			
	else:
		# on n'a pas le meilleur prix mettre le produit en rouge
		couleur = styles.PatternFill(start_color="ff3838", end_color="ff3838", fill_type="solid")
	# appliquer la couleur
	for i in range(1, 10):
		rapport.cell(startRow, i).fill = couleur

	# Appliquer la couleur aux meilleur prix équivalent
	couleur = styles.PatternFill(start_color="729fcf", end_color="729fcf", fill_type="solid")
	for row in spl:
		for i in range(10, 20):
			rapport.cell(row, i).fill = couleur
	
	# Augmenter la ligne de départ
	startRow = endRow + 1





wb.save("result/rapport.xlsx")