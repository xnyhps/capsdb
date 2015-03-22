#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom, Node
from os import listdir
from os.path import isfile, join
import urllib
import base64
import sqlite3

files = [f for f in listdir("hashes/") if isfile(join("hashes",f))]

conn = sqlite3.connect('db.sqlite')

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS clients;")
c.execute("DROP TABLE IF EXISTS features;")
c.execute("DROP TABLE IF EXISTS client_features;")

c.execute("CREATE TABLE clients (id INTEGER PRIMARY KEY, node TEXT NOT NULL, hash TEXT NOT NULL);")
c.execute("CREATE TABLE features (id INTEGER PRIMARY KEY, var TEXT NOT NULL UNIQUE);")
c.execute("CREATE TABLE client_features (client_id INTEGER, feature_id INTEGER, FOREIGN KEY(client_id) REFERENCES clients(id), FOREIGN KEY(feature_id) REFERENCES features(id));")

for f in files:
	try:
		[h, node] = f.split(".xml")[0].split("_", 2)

		node = urllib.unquote(node)
		
		[node, ver] = node.split("#", 2)
	except ValueError:
		continue

	dom = minidom.parse(join("hashes", f))

	c.execute("INSERT INTO clients (node, hash) VALUES (?,?)", (node, ver))

	features = dom.getElementsByTagName("feature")

	for feature in features:
		try:
			c.execute("INSERT INTO features (var) VALUES (?)", (feature.attributes["var"].value,))
		except sqlite3.IntegrityError:
			pass

		c.execute("INSERT INTO client_features SELECT clients.id, features.id FROM clients, features WHERE node = ? AND hash = ? AND var = ? LIMIT 1" , (node, ver, feature.attributes["var"].value))


conn.commit()
conn.close()