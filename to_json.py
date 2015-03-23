#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom, Node
from os import listdir
from os.path import isfile, join
import urllib
import base64
import json

files = [f for f in listdir("hashes/") if isfile(join("hashes",f))]

hash_dict = dict()

def get_identity(identity):
	ret = dict()

	ret["category"] = identity.attributes["category"].value
	ret["type"] = identity.attributes["type"].value

	if identity.attributes.get("xml:lang", None):
		ret["lang"] = identity.attributes["xml:lang"].value
	if identity.attributes.get("name", None):
		ret["name"] = identity.attributes["name"].value

	return ret

def get_form_type(form):
	types = filter(lambda field: field.attributes["var"].value == "FORM_TYPE", form.getElementsByTagName("field"))

	return types[0].getElementsByTagName("value")[0].firstChild.nodeValue

def get_forms(forms):
	ret = dict()

	for form in forms:
		form_type = get_form_type(form)

		ret[form_type] = dict()

		for field in form.getElementsByTagName("field"):
			field_name = field.attributes["var"].value

			if field_name == "FORM_TYPE": continue

			values = []

			for value in field.getElementsByTagName("value"):
				if value.firstChild:
					values.append(value.firstChild.nodeValue)
				else:
					values.append("")

			ret[form_type][field_name] = values

	return ret

for f in files:
	try:
		[h, node] = f.split(".xml")[0].split("_", 2)

		node = urllib.unquote(node)
		
		[node, ver] = node.split("#", 2)
	except ValueError:
		continue

	dom = minidom.parse(join("hashes", f))

	identities = map(get_identity, dom.getElementsByTagName("identity"))
	features = sorted(map(lambda feature: feature.attributes["var"].value, dom.getElementsByTagName("feature")))
	forms = get_forms(dom.getElementsByTagNameNS("jabber:x:data", "x"))

	hash_dict[ver] = { "features": features, "identities": identities, "forms": forms }

f = open("db.json", "w")

json.dump(hash_dict, f, indent=1, sort_keys=1)