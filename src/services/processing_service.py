# External imports
import json
import requests
from jsonpath_rw import parse, jsonpath
import pandas as pd
import xml.etree.ElementTree as ET


# Internal imports
from pyutils.file_io import *
from pyutils.print_formatting import *
from pyutils.xml_utils import *
from pyutils.list_utils import *
from pyutils.tuple_utils import *
from pyutils.str_utils import *


from services.base_service import BaseService
from services.ontology_utils import *

from pths import *

import operator
from itertools import chain, groupby



class ProcessingService(BaseService):

    def __init__(self, p=None, dsp=None):
        self.models = {}
        self.allModels = {}


        if (p):
            super().__init__(p)

        if (dsp):
            self.dsp = dsp



    def load_models(self, modelPath=pths['models_raw'], fromDat=None):
        if fromDat==None:
            fromDat = self.p['parsedXmlStr']
        count = 0
        for root, dirs, files in os.walk(modelPath):
            print("Number of models available for analysing ", len(files))
            for file in files:
                if ".DS_Store" not in file:
                    count += 1
                    if self.nModels and isinstance(self.nModels,int) and count > self.nModels:
                        print("Max models ", self.nModels, " reached.")
                        break

                    fileAndPath = modelPath + file

                    try:
                        if file not in self.models.keys():
                            self.models[file] = {}
                        if (modelPath==pths['models_raw']):
                            self.models[file][fromDat] = ET.parse(fileAndPath)
                        else:
                            self.models[file][fromDat] = load_file(fileAndPath)

                    except Exception as e:
                        print("Failed for ", file, " ", e)




    def processing_scope(processing_function):
        ''' Defines what gets processed '''

        def wrapper(self, *args, **kwargs):
            if 'extension' in kwargs.keys():
                extension = kwargs["extension"]
                del kwargs["extension"]
            else:
                extension = "json"

            if 'fromDat' in kwargs:
                self.fromDat = kwargs['fromDat']
                del kwargs['fromDat']

            else:
                self.fromDat = self.newDatStruct
                print("getting dat from: ", self.fromDat)


            if 'toDat' in kwargs:
                self.newDatStruct = kwargs['toDat']
                del kwargs['toDat']

            else:
                self.newDatStruct = processing_function.__name__ + \
                    "-" + dict_to_str(kwargs)

            if 'save' in kwargs:
                self.save = kwargs['save']
                del kwargs['save']

            else:
                self.save = self.p['saveModelAfterEachProcessingStep']


            if (self.p['print_processingStep']):
                print("- ** Step: ", processing_function.__name__, " ", self.fromDat," ",self.newDatStruct)

            if len(self.models)==0:
                fromPath = pths['models_processed']+self.fromDat+"/"
                self.load_models(fromPath, self.fromDat)

            print("self.newDatStruct: ", self.newDatStruct )
            nMatchingModels = 0

            if 'includeReferringID' in kwargs:
                includeReferringID = True
                del kwargs['includeReferringID']
            else:
                includeReferringID = False


            if 'mergeDuplicatesByKey' in kwargs:
                mergeDuplicatesByKey = kwargs['mergeDuplicatesByKey']
                del kwargs['mergeDuplicatesByKey']
            else:
                mergeDuplicatesByKey = False


            for model in self.models:
                if includeReferringID:
                    kwargs['referringID'] = model

                if (self.p['print_modelNameBeforeProcessing']):
                    print(model)

                # Get input dat
                # print("self.models[model]: ", self.models[model])
                # print("self.models[model][self.fromDat]: ", self.models[model][self.fromDat])
                try:
                    if (isinstance(self.fromDat, list)):
                        # print("multiple fromDats detected: ", self.fromDat)
                        modelDat = []
                        for fromD in self.fromDat:
                            modelDat.append(self.models[model][fromD])

                    else:
                        modelDat = self.models[model][self.fromDat]

                    # Append input dat as args
                    kwargs['inputDat'] = modelDat

                    # Produce output dat
                    modelNewDat = processing_function( *args, **kwargs )

                    nMatches = len(modelNewDat)

                    if nMatches > 0:
                        nMatchingModels += 1
                        self.models[model][self.newDatStruct] = modelNewDat


                        if (self.p['allModels_process']):
                            if not self.newDatStruct in self.allModels.keys():
                                self.allModels[self.newDatStruct] = []
                            self.allModels[self.newDatStruct] += self.models[model][self.newDatStruct]


                        if (self.p['print_matches_individual']):
                            if ('print_matches_greater_than' in self.p.keys()):
                                if (nMatches > self.p['print_matches_greater_than']):
                                    print(nMatches, " matches for ", model)
                                else:
                                    print('no matches for ', model)
                            else:
                                print(nMatches, " matches for ", model) #, " of ", self.newDatStruct)

                        if (self.save):
                            newPath = pths['models_processed']+self.newDatStruct+"/"
                            save_dat( self.models[model][self.newDatStruct], filename=model, directory=newPath, extension=extension )

                except Exception as e:
                    print("could not process ", model, " e: ", e)
                    pass

            if (self.newDatStruct in self.allModels.keys()):
                nMatches = len(self.allModels[self.newDatStruct])
                if (self.p['print_matches_allModels']):
                    if nMatches > 0:

                        print(nMatches, " matches for ",nMatchingModels," models")
                    else:
                        print("no matches.")

                if self.p['allModels_removeDuplicates']:
                    self.allModels[self.newDatStruct] = self.remove_duplicates(self.allModels[self.newDatStruct])

                if mergeDuplicatesByKey:
                    self.allModels[self.newDatStruct] = self.merge_duplicates(self.allModels[self.newDatStruct], byKey=mergeDuplicatesByKey)


                newFileName = self.p['allModels_filename'] + "_" + self.newDatStruct
                if self.save:
                    save_dat( self.allModels[self.newDatStruct], filename=newFileName, directory=pths['models_processed'], extension=extension )
                nMatches = len(self.allModels[self.newDatStruct])

                if (self.p['print_matches_allModels']):
                    print(nMatches, " unique matches for ",nMatchingModels," models")


            if (self.p['print_hierAfterProcessing']):
                print_keys_hierarchy(self.models[model])

        return wrapper


    @processing_scope
    def get_dat_from_cellml_xml(inputDat=None, category=None, attributes=None, removeDuplicates=True):
        root = inputDat.getroot()

        if (not attributes):
            return get_elements_from_xml_tree_by_tag(root, category)
        else:
            return get_elements_from_xml_tree_by_attribs(root, attributes)


    @processing_scope
    def get_dat_from_rdf(inputDat=None, sKey=None, sMatch=None, pKey=None, pMatch=None, oKey=None, oMatch=None, removeDuplicates=True):
        return parse_rdf(inputDat,  sKey=sKey, sMatch=sMatch, pKey=pKey, pMatch=pMatch, oKey=oKey, oMatch=oMatch)



    @processing_scope
    def lookup(inputDat=None, searchByKey=None, keysToSubset=None, matchesToReturn=1):
        outList = []
        for item in inputDat:
            matches = perform_lookup(item[searchByKey], matchesToReturn, keysToSubset)
            if len(matches) > 0:
                item['lookup'] = list(matches)
                outList += make_list_if_not(item)
        # print("outList:", outList)

        return outList



    @processing_scope
    def get_uniques(inputDat=None, uniqueKey=None, uniquesByVal=False):
        return get_uniques_by_key(inputDat, uniqueKey)


    @processing_scope
    def get_match_by_substr(inputDat=None, keyValMatch=None, caseSensitive=False):

        k = list(keyValMatch.keys())[0]
        val = list(keyValMatch.values())[0]
        if not caseSensitive:
            val = val.lower()
            matches = list(v for v in inputDat if (val in v[k].lower()))
        else:
            matches = list(v for v in inputDat if (val in v[k]))

        return matches



    @processing_scope
    def get_match_by_any_of(inputDat=None, key=None, vals=None, caseSensitive=False):

        matches = []
        if not caseSensitive:
            for val in vals:
                matches += list(v for v in inputDat if (val.lower() in v[key].lower()))
        else:
            for val in vals:
                matches += list(v for v in inputDat if (val in v[key]))

        return matches

    @processing_scope
    def get_match_exact(inputDat=None, keyValMatch=None, caseSensitive=False, joinWithCurrMatches=False):

        k = list(keyValMatch.keys())[0]
        val = list(keyValMatch.values())[0]

        matches = list(v for v in inputDat if (val == v[k]))

        return matches

    @processing_scope
    def join_matching_by_key(inputDat=None, matchByKey=None, returnOnlyMatches=True, joinWithCurrMatches=False):
        allKeys = list(set(list(inputDat[0][0].keys()) + list(inputDat[1][0].keys())))

        matches = sorted(chain(inputDat[0],inputDat[1]), key=lambda x:x[matchByKey])

        matches = [dict(y for x in g for y in x.items()) for k,g in groupby(matches,key=lambda x:x[matchByKey])]

        if (returnOnlyMatches):
            matches = [x for x in matches if all_of_this_list_in_that_list(allKeys, list(x.keys()))]

        return matches




    @processing_scope
    def replace_values_with_dict_where_matching(inputDat, newValues, fromDatKey="id", newValuesKey="id"):
        outItems = []
        for item in inputDat:
            # print(item)
            for newVal in newValues:
                # print(item[fromDatKey],"-",newVal[newValuesKey],"-")
                try:
                    if strip_extension(item[fromDatKey].strip()) == strip_extension(newVal[newValuesKey].strip()):
                        item[fromDatKey] = copy.deepcopy(newVal)
                        # print("match! ")
                except Exception as e:
                    print(e)
            outItems.append(item)

        return outItems


    @processing_scope
    def add_referring_id_as_property(inputDat, referringID, idKey="id"):
        outItems = []
        for item in inputDat:
            item[idKey] = referringID
            outItems.append(item)

        return outItems



    @processing_scope
    def extract_subset_of_keys(inputDat, keysToSubset):
        return subset_list_of_dicts_by_keys(inputDat, keysToSubset)


    def merge_duplicates(self, inputDat=None, byKey=None):
        copyOfDat = copy.deepcopy(inputDat)
        outList = []
        for x in inputDat:
            for y in copyOfDat:
                if x[byKey]==y[byKey]:
                    if not x == y:
                        x = merge_dicts(x, y)
            outList.append(x)

        return outList



    def remove_duplicates(self, listOfDicts=None):
        # print("All matches *with* duplicates: ", len(listOfDicts))
        # Make dict hashable, get uniques
        if (len(listOfDicts) > 0):
            if isinstance(listOfDicts[0], dict):
                try:
                    uniqueSets = set(frozenset(d.items()) for d in listOfDicts)
                    listOfDicts = [dict(s) for s in uniqueSets]
                except Exception as e:
                    print(e)
            else:
                listOfDicts = list(set(listOfDicts))
        # print("All matches without duplicates: ", len(listOfDicts))

        return listOfDicts
