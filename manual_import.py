#!/usr/bin/env python
from xml.dom import minidom, Node
from os.path import join
import xml.dom
import urllib
import sys
import argparse

def remove_blanks(node):
	for x in node.childNodes:
		if x.nodeType == Node.TEXT_NODE:
			if x.nodeValue:
				x.nodeValue = x.nodeValue.strip()
		elif x.nodeType == Node.ELEMENT_NODE:
			remove_blanks(x)

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

node = raw_input("Enter node: ")
ver = raw_input("Enter hash (base64 encoded): ")
h = raw_input("Enter hash algorithm (sha-1, or md5): ")

xmldoc = minidom.parse(args.file)

query_doc = xml.dom.getDOMImplementation().createDocument("http://jabber.org/protocol/disco#info", "query", None)
query_doc.documentElement.setAttribute("xmlns", "http://jabber.org/protocol/disco#info")
query_doc.documentElement.attributes["node"] = node + "#" + ver
query_doc.documentElement.childNodes = xmldoc.childNodes

remove_blanks(query_doc.documentElement)

f = open(join("hashes", h + "_" + urllib.quote(node + "#" + ver, "") + ".xml"), "w")

f.write(query_doc.toprettyxml("","").encode('utf8'))