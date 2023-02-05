#!/bin/python3
# -*- coding: utf-8 -*-

barcodeToUUID = {}
UUIDToName = {'59ce37ce-9de5-11ed-afbd-e4029b8a2c99': 'Lait partiellement écrémé 2% Québon',
              '7efc3b56-67cb-4cb0-a9dd-ccaf94a919e1': 'Lait Finement filtré 2% (1L)',
              '00ce1ad1-6fd6-4573-bc53-f2c718c8d7ca': 'Lait biologique 2% (1L)',
              '63a35e24-aad9-440f-b6a7-2e80a4e04096': 'Lait 2 %',
              '67df6c8e-e2f0-4d53-bcec-5ccd8f20c6d4': 'Boisson au lait 2 %',
              '1facadc0-9de8-11ed-afbd-e4029b8a2c99': 'Yogourt Probiotique, 3X Fraise, 3X Bleuets, 3X Framboise, 3X Pêche'}
UUIDToDescription = {'59ce37ce-9de5-11ed-afbd-e4029b8a2c99': 'Lait partiellement écrémé 2% Québon',
                     '1facadc0-9de8-11ed-afbd-e4029b8a2c99': 'Quatre saveurs exquises disponibles en un seul format pratique de 12 x 100 g.'}
                     
equivalencyTable = {'59ce37ce-9de5-11ed-afbd-e4029b8a2c99':{'7efc3b56-67cb-4cb0-a9dd-ccaf94a919e1', '00ce1ad1-6fd6-4573-bc53-f2c718c8d7ca', '63a35e24-aad9-440f-b6a7-2e80a4e04096', '67df6c8e-e2f0-4d53-bcec-5ccd8f20c6d4'}}

produitES = {'59ce37ce-9de5-11ed-afbd-e4029b8a2c99'}
