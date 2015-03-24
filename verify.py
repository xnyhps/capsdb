#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom, Node
from os import listdir
from os.path import isfile, join
import urllib
import base64
from xml.sax.saxutils import escape
import hashlib

files = [f for f in listdir("hashes/") if isfile(join("hashes",f))]

def unwrap(x):
	if x == None:
		return ""
	return x.value

def fix_hash(h):
	if h == "sha-1":
		return "sha1"
	return h

def compare_var(a,b):
	return cmp(a.attributes["var"].value, b.attributes["var"].value)

def get_form_type(form):
	types = filter(lambda field: field.attributes["var"].value == "FORM_TYPE", form.getElementsByTagName("field"))


	# If the response includes an extended service discovery information form where
	# [...] the form does not include a FORM_TYPE field, ignore the form but continue
	# processing.
	if len(types) == 0:
		return None

	if len(types) > 1:
		raise ValueError, "Multiple FORM_TYPEs on one form."

	[t] = types

	# If the response includes an extended service discovery information form where
	# the FORM_TYPE field is not of type "hidden" [...] ignore the form but continue
	# processing.
	if t.attributes["type"].value != "hidden":
		return None

	values = t.getElementsByTagName("value")

	if len(values) == 0:
		raise ValueError, "No <value/> child of the FORM_TYPE element."

	v = values[0].firstChild.nodeValue

	# If [...] the FORM_TYPE field contains more than one <value/> element with different
	# XML character data, consider the entire response to be ill-formed.
	for value in values[1:]:
		if value.firstChild.nodeValue != v:
			raise ValueError, "Multiple <value/> children of the FORM_TYPE element with different character data."

	return v


for f in files:
	try:
		[h, node] = f.split(".xml")[0].split("_", 2)

		node = urllib.unquote(node)
		
		[node, ver] = node.split("#", 2)
	except ValueError:
		continue

	try:
		ver = base64.b64decode(ver)

		dom = minidom.parse(join("hashes", f))

		s = []

		identities = dom.getElementsByTagName("identity")

		identity_names = map(lambda x: x.attributes["category"].value + "/"
										+ x.attributes["type"].value + "/"
										+ unwrap(x.attributes.get("xml:lang", None)) + "/"
										+ unwrap(x.attributes.get("name", None)),
							identities)

		# If the response includes more than one service discovery identity with the
		# same category/type/lang/name, consider the entire response to be ill-formed.
		if len([name for name in identity_names if identity_names.count(name) > 1]) > 0:
			raise Exception, "Duplicate identity"

		s += sorted(identity_names)


		features = dom.getElementsByTagName("feature")

		feature_names = map(lambda x: x.attributes["var"].value, features)

		# If the response includes more than one service discovery feature with the same
		# XML character data, consider the entire response to be ill-formed.
		#
		# There are actually 33 caps I have that fail this test, but do have a valid hash,
		# so lets just log a warning.
		duplcate_features = [var for var in feature_names if feature_names.count(var) > 1]
		if len(duplcate_features) > 0:
			print("%s: WARNING: Duplicate feature: %s" % (f, duplcate_features))

		s += sorted(feature_names)


		forms = dom.getElementsByTagNameNS("jabber:x:data", "x")

		forms = sorted(forms, lambda a,b: cmp(get_form_type(a), get_form_type(b)))

		for form in forms:
			t = get_form_type(form)

			if t == None: continue

			# I have yet to see a service discovery result with a different dataform than
			# the urn:xmpp:dataforms:softwareinfo. One of the most serious preimage attacks
			# possible with XEP-0115 is to turn features in to data forms, making some of
			# the features disappear. This tries to check for that.
			if t not in ["urn:xmpp:dataforms:softwareinfo", "http://jabber.org/network/serverinfo"]:
				print("%s: WARNING: Suspicious data form: %s" % (f, t))

			s.append(t)

			for field in sorted(form.getElementsByTagName("field"), compare_var):

				if field.attributes["var"].value == "FORM_TYPE":
					continue

				s.append(field.attributes["var"].value)

				for value in sorted(field.getElementsByTagName("value"), lambda a, b: a.firstChild.nodeValue > b.firstChild.nodeValue):
					if value.firstChild:
						s.append(value.firstChild.nodeValue)
					else:
						s.append("")

		hasher = hashlib.new(fix_hash(h))

		s = "".join(map(lambda x: escape(x).encode("utf8") + "<", s))

		hasher.update(s)

		if hasher.digest() == ver:
			print("%s SUCCESS" % f)
			pass
		else:
			print(f)
			print(s)
			print(hasher.digest(), ver)
			assert(False)
	except ValueError as e:
		print("%s failed: %s" % (f, e))