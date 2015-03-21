#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom, Node
from os import listdir
from os.path import isfile, join
import urllib
import base64
from xml.sax.saxutils import escape
import hashlib

files = [ f for f in listdir("hashes/") if isfile(join("hashes",f)) ]

def unwrap(x):
	if x == None:
		return ""
	return x.value

def fix_hash(h):
	if h == "sha-1":
		return "sha1"
	return h

def p(a,b):
	return cmp(a.attributes["var"].value, b.attributes["var"].value)

for f in files:
	try:
		[h, node] = f.split(".xml")[0].split("_", 2)

		node = urllib.unquote(node)
		
		[node, ver] = node.split("#", 2)
	except ValueError:
		continue

	ver = base64.b64decode(ver)

	dom = minidom.parse(join("hashes", f))

	s = []

	identities = dom.getElementsByTagName("identity")

	s += sorted(map(lambda x: x.attributes["category"].value + "/"
									+ x.attributes["type"].value + "/"
									+ unwrap(x.attributes.get("lang", None)) + "/"
									+ unwrap(x.attributes.get("name", None)),
						identities))

	features = dom.getElementsByTagName("feature")

	s += sorted(map(lambda x: x.attributes["var"].value, features))

	forms = dom.getElementsByTagNameNS("jabber:x:data", "x")

	forms = sorted(forms, lambda form: filter(lambda field: field.attributes["var"].value == "FORM_TYPE", form.getElementsByTagName("field"))[0].getElementsByTagName("value").firstChild.nodeValue)

	for form in forms:
		fields = []
		for field in sorted(form.getElementsByTagName("field"), p):

			if field.attributes["var"].value == "FORM_TYPE":
				s.append(field.getElementsByTagName("value")[0].firstChild.nodeValue)
				continue

			fields.append(field.attributes["var"].value)

			for value in sorted(field.getElementsByTagName("value"), lambda a, b: a.firstChild.nodeValue > b.firstChild.nodeValue):
				if value.firstChild:
					fields.append(value.firstChild.nodeValue)
				else:
					fields.append("")

		s += fields

	hasher = hashlib.new(fix_hash(h))

	s = "".join(map(lambda x: escape(x).encode("utf8") + "<", s))

	hasher.update(s)

	if hasher.digest() == ver:
		print("SUCCESS")
		pass
	else:
		print(f)
		print(s)
		print(hasher.digest(), ver)
		assert(False)