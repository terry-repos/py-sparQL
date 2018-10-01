import requests
import json
import rdflib

from rdflib.graph import Graph
from rdflib.plugins.sparql import prepareQuery
# from rdflib.processor import prepareQuery
from SPARQLWrapper import SPARQLWrapper, JSON, N3


class PMRService():
    def __init__(self):
        self.pmrEndpoint = "https://models.physiomeproject.org/@@search"
        self.pmrSparqlEndpoint = "https://models.physiomeproject.org/pmr2_virtuoso_search"

        self.sparqlEndpoint = SPARQLWrapper(self.pmrSparqlEndpoint)
        self.init_queries()

# var sendPostRequest = function (requestUrl, query, responseHandler, isJsonResponse) {
#     var request = getRequestObject();
#
#     request.onreadystatechange = function () {
#         handleResponse(request, responseHandler, isJsonResponse);
#     };
#
#     request.open("POST", requestUrl, true);
#
#     request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
#     request.setRequestHeader("Accept", "application/sparql-results+json");
#
#     request.send(query); // for POST only
# };

    def request_model_list(self):
        r = requests.post(self.pmrEndpoint, headers={'Accept': 'application/vnd.physiome.pmr2.json.1'}, dat=json.dumps(
            {'template': {"dat": [{"name": "Subject", "value": "CellML Model"}]}}))
        return r.text

    def perform_sparql_query(self, query=None):

        r = requests.post(self.pmrSparqlEndpoint, headers={'Accept': 'application/sparql-results+json'}, data=self.queries[query])
        print(r.text)



    def init_queries(self):
       self.queries={}
       self.queries['select_models'] = """
                     SELECT ?cellmlmodel ?located_in
                     WHERE { GRAPH ?g { ?cellmlmodel <http://www.obofoundry.org/ro/ro.owl#located_in> ?located_in. }}
                 """
       # self.queries['select_models'] = prepareQuery(
       #      'SELECT ?cellmlmodel ?located_in WHERE { GRAPH ?g { ?cellmlmodel <http://www.obofoundry.org/ro/ro.owl#located_in> ?located_in.')

        # query = "SELECT ?Workspace ?Model_entity ?Title ?Author ?Abstract ?Keyword ?Protein ?Compartment " +
        #     "?Located_in ?DOI WHERE { GRAPH ?Workspace { " +
        #     "<" + cellmlModel + "> <http://purl.org/dc/terms/title> ?Title . " +
        #     "?Model_entity <http://purl.org/dc/terms/title> ?Title . " +
        #     "OPTIONAL { <" + cellmlModel + "> <http://www.w3.org/2001/vcard-rdf/3.0#FN> ?Author } . " +
        #     "OPTIONAL { <" + cellmlModel + "> <http://purl.org/dc/terms/abstract> ?Abstract } . " +
        #     "OPTIONAL { <" + cellmlModel + "> <http://purl.org/dc/terms/keyword> ?Keyword } . " +
        #     "OPTIONAL { <" + cellmlModel + "> <http://www.obofoundry.org/ro/ro.owl#modelOf> ?Protein } . " +
        #     "OPTIONAL { <" + cellmlModel + "> <http://www.obofoundry.org/ro/ro.owl#compartmentOf> ?Compartment } . " +
        #     "OPTIONAL { <" + cellmlModel + "> <http://www.obofoundry.org/ro/ro.owl#located_in> ?Located_in } . "

        # PREFIX semsim: <http://www.bhi.washington.edu/SemSim#>
        # SELECT ?opb WHERE {
        # < model semsim:isComputationalComponentFor ?model_prop.
        # ?model_prop semsim:hasPhysicalDefinition ?opb.
        # }
