from list_utils import *
import xml.etree.ElementTree as ET
import rdflib
from rdflib.graph import Graph

import pyutils.str_utils


def get_elements_from_xml_tree_by_tag(rootEls, tag):
	outEls = ""

	for el in rootEls:


		if tag in el.tag:
			elAsText = ET.tostring(el).decode('utf-8')
			outEls += elAsText

		else:
			outEls += get_elements_from_xml_tree_by_tag(el, tag)

	return outEls



def get_elements_from_xml_tree_by_attribs( rootEls, matchAttribs, returnThis="matched_attributes" ):
	outEls = []

	for el in rootEls:

		attribKeys = list(el.attrib.keys())
		# print(matchAttribs, " ", attribKeys)

		if (all_of_this_list_in_that_list(matchAttribs, attribKeys)):
			if returnThis=="all_attributes":
				outEls.append(el.attrib)
			elif returnThis=="matched_attributes":
				outDict = {}
				for k in matchAttribs:
					outDict[k] = el.attrib[k]
				outEls.append(outDict)

		else:
			outEls += get_elements_from_xml_tree_by_attribs(el, matchAttribs, returnThis)

	return outEls



def parse_rdf(inRDF, sKey=None, sMatch=None, pKey=None, pMatch=None, oKey=None, oMatch=None):

	outList = []

	g = rdflib.Graph()
	try:

		result = g.parse(data=inRDF)
		for s, p, o in g:
			match=True

			if sMatch:
				if not s.strip()==sMatch.strip():

					match=False

			if pMatch:
				if not p.strip()==pMatch.strip():

					match=False

			if oMatch:
				if not o.strip()==oMatch.strip():

					match=False

			if match:
				# print("s: ", dir(s), " p: ", dir(p), " o: ", dir(o))

				outObj = {}
				if sKey:
					outObj[sKey] = strip_non_alpha_numeric(s.n3())

				if oKey:
					outObj[oKey] = strip_non_alpha_numeric(o.n3())

				if pKey:
					outObj[pKey] = strip_non_alpha_numeric(p.n3())

				outList.append(outObj)

			else:
				pass
				# print("FAIL: ", p)

		# print("success!")
	except Exception as e:
		# print("could not parse rdf: ", e)
		pass
	return outList


def print_els(els):
	for el in els:
		print(el)
		# print(el.tag)
		# print(el.text)
		# print(el.attr)


# for href in hrefs:
#     href = href.replace("/view","")
#     filename = href[href.rfind("/")+1:]
#
#     fileAndPath = datPaths['raw_models'] +filename

#     if not os.path.isfile(fileAndPath):
#         response = requests.get( href )
#         xmlRoot = ET.fromstr( response.text )
#         save_dat_to_file(datPaths['raw_models'], filename,  response.text.encode('utf8'))
#     else:
#         print(fileAndPath, " exists.")
