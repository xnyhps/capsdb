#!/usr/bin/env python
from xml.dom import minidom, Node
from os.path import join
import xml.dom
import argparse
import base64
import binascii
import unicodedata
import urllib

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

xmldoc = minidom.parse(args.file)
clients = xmldoc.getElementsByTagName('client')

def remove_blanks(node):
	for x in node.childNodes:
		if x.nodeType == Node.TEXT_NODE:
			if x.nodeValue:
				x.nodeValue = x.nodeValue.strip()
		elif x.nodeType == Node.ELEMENT_NODE:
			remove_blanks(x)

for client in clients:
	ver = client.attributes["ver"].value

	if client.attributes.get("hash", None):
		node = unicodedata.normalize('NFKD', client.attributes["node"].value)
		query_doc = xml.dom.getDOMImplementation().createDocument("http://jabber.org/protocol/disco#info", "query", None)
		query_doc.documentElement.setAttribute("xmlns", "http://jabber.org/protocol/disco#info")
		query_doc.documentElement.attributes["node"] = node + "#" + ver
		query_doc.documentElement.childNodes = client.childNodes

		remove_blanks(query_doc.documentElement)

		# Apparently Pidgin loses the xml: prefix on the lang attribute,
		# hacking it back in.
		for identity in query_doc.getElementsByTagName("identity"):
			if identity.attributes.get("lang", None):
				lang = identity.attributes["lang"].value
				identity.removeAttribute("lang")
				new_lang = query_doc.createAttributeNS(xml.dom.XML_NAMESPACE, "xml:lang")
				new_lang.value = lang
				identity.setAttributeNode(new_lang)

		f = open(join("hashes", client.attributes["hash"].value + "_" + urllib.quote(node + "#" + ver, "") + ".xml"), "w")

		f.write(query_doc.toprettyxml("","").encode('utf8'))