#!/bin/python3
# -*- coding: utf-8 -*-

from secret import key
import xmlrpc.client
import pandas

products = pandas.read_csv("productTable.csv")
productsEs = pandas.read_csv("produitses.csv")

url = 'https://test618.odoo.com'
db = "test618"
username = "gabriel.desharnais@hotmail.com"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
ouid = common.authenticate(db, username, key, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, ouid, key, 'ir.model.data', 'search_read',[[['name', '=', 'bc402d78-b9e5-46f1-a11e-e67c77e2deaa']]] , {'fields':['name', 'res_id']})


# Faire le tour de la liste des produits de l'épicerie
for uid in productsEs["uuid"].values:
	# Déterminer si le produit est taxable
	try:
		taxable = products.loc[products["uuid"]==uid,["taxable"]].values[0][0]
	except IndexError:
		print("Erreur avec", uid)
		continue
	# Aller chercher le id produit à partir de la bd odoo
	print(uid)
	match = models.execute_kw(db, ouid, key, 'ir.model.data', 'search_read',[[['name', '=', uid]]] , {'fields':['res_id']})
	if len(match) !=1:
		print("erreur avec", uid, "produit absent de odoo (ou trop de match)")
		continue
	odooProductId = match[0]["res_id"]
	# Aller mettre à jour les taxe
	if taxable:
		models.execute_kw(db, ouid, key, 'product.template', 'write',[[odooProductId], {'taxes_id':[25]} ] )
	else:
		models.execute_kw(db, ouid, key, 'product.template', 'write',[[odooProductId], {'taxes_id':[(5,0,0)]} ] )