# External imports
import json
import requests
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from jsonpath_ng import parse, jsonpath

# Internal imports
from pyutils.file_io import *
from pyutils.dict_utils import *
from pyutils.print_formatting import *
from pyutils.xml_utils import *


# serviceUrl = "http://ontology.cer.auckland.ac.nz/"
serviceUrl = "https://www.ebi.ac.uk/ols/api/"
olsLookupEndpoint = serviceUrl + "search?q="
ontologiesUrl = serviceUrl + "ols-boot/api/ontologies"
onts = {}
ontHiers = {}
keysBase = ['_embedded', 'ontologies']
ontHiers['names'] = ['config', 'namespace']


def perform_lookup(query=None, matchesToReturn=1, keysToSubset=None):
    queryUrl = olsLookupEndpoint + query
    r = requests.get(queryUrl)
    matches = json.loads(r.text)['response']['docs'][0:matchesToReturn]
    if (keysToSubset):
        matches = make_list_if_not(matches)
        outMatches = []
        for match in matches:
            match = subset_dict_by_keys(match, keysToSubset)
            # print(match)
            outMatches.append(match)
        matches = list(outMatches)

    return matches


def fetch_ontologies( keysBase):

    r = requests.get(ontologiesUrl)
    onts['raw'] = json.loads(r.text)[keysBase[0]][keysBase[1]]
    # print(onts['raw'] )


def fetch_ontology_names():
    onts['names'] = get_vals_of_list_of_dicts_from_hierarchy(onts['raw'], ontHiers['names'])
    print(onts['names'] )
