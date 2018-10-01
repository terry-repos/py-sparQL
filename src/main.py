import os
import sys
import datetime


# For console colouring
try:
    import IPython.core.ultratb
except ImportError:
    # No IPython. Use default exception printing.
    pass
else:
    import sys
    sys.excepthook = IPython.core.ultratb.ColorTB()


# internal imports
from services.crawler_service import CrawlerService
from services.processing_service import ProcessingService
# from services.ontology_service import OntologyService
from services.pmr_service import PMRService
from pyutils.dict_utils import *


thisPath = os.path.dirname(__file__)
subPaths = ["pyutils", "services"]
for subPath in subPaths:
    sys.path.append(os.path.join(thisPath, subPath))

# processingParams
processingParams = {}
processingParams['nModels'] = 999
# processingParams['eachModel'] = True
processingParams['allModels_process'] = True
processingParams['allModels_removeDuplicates'] = True
processingParams['allModels_filename'] = "allModels"

processingParams['saveModelAfterEachProcessingStep'] = True

processingParams['print_hierAfterProcessing'] = False
processingParams['print_processingStep'] = True
processingParams['print_modelNameBeforeProcessing'] = False
processingParams['print_matches_individual'] = False
processingParams['print_matches_allModels'] = True
processingParams['print_matches_greater_than'] = 0

# dat structure params
dsp = {}
dsp['parsedXmlStr'] = 'parsed_xml'

category = 'variable'
attributes = ['name', 'units']


def main():
    print(" ")
    print(" ")
    print("--- Running at ", datetime.datetime.now())

    # pmrService = PMRService()
    # # pmrService.perform_sparql_query('select_models')
    #
    # cs = CrawlerService(processingParams, dsp)
    # cs.fetch_model_list(fromPMR=False)
    # print(cs.modelList)
    # cs.download_models( )

    dps = ProcessingService(processingParams, dsp)
    dps.load_models()

    # All variables
    dps.get_dat_from_cellml_xml(fromDat=dsp['parsedXmlStr'],
                                category=category, attributes=attributes, toDat="vars_all", save=False)

    # dps.get_match_by_substr(fromDat='name_units',
    #                         keyValMatch={"units": "mol"}, toDat="vars_with_mol")
    #
    # dps.get_match_by_substr(fromDat='name_units',
    #                         keyValMatch={"units": "mM"}, caseSensitive=True,  toDat="vars_with_mM")
    dps.get_match_by_any_of(fromDat='vars_all',
                             key="units", vals=["pM","nM","mM","mol","Mol"], caseSensitive=True,
                             toDat="vars_with_conc")

    # # Unique units
    dps.get_uniques(fromDat='vars_all', uniqueKey='units',
                    uniquesByVal=True, toDat='vars_unique_units')
    dps.get_uniques(fromDat='vars_with_conc', uniqueKey='units',
                    uniquesByVal=True, toDat='vars_conc_unique_units')
    # dps.get_uniques(fromDat='vars_with_mol', uniqueKey='units',
    #                 toDat='unique_units_mol')
    # dps.get_uniques(fromDat='vars_with_mM', uniqueKey='units',
    #                 toDat='unique_units_mM')

    # Annotated models

    dps.get_dat_from_cellml_xml(fromDat=dsp['parsedXmlStr'],
                                category="rdf", extension="rdf", toDat="rdf_extracted", save=False)

    dps.get_dat_from_rdf(fromDat="rdf_extracted", pMatch="http://purl.org/dc/terms/alternative", sKey="name", oKey="readable",
                         toDat="readables_from_rdf", save=False)


    dps.join_matching_by_key(fromDat=['readables_from_rdf', 'vars_all'],
                             matchByKey="name", toDat="readables_all")


    dps.get_match_by_any_of(fromDat='readables_all',
                                key="units", vals=["pM","nM","mM","mol","Mol"], caseSensitive=True, toDat="readables_with_conc")

    dps.get_match_by_substr(fromDat='name_units_readable',
                            keyValMatch={"units": "mM"}, caseSensitive=True, toDat="readables_with_mM")

    # Unique units
    dps.get_uniques(fromDat='readables_all',
                    uniqueKey='units', toDat='readables_unique_units')
    dps.get_uniques(fromDat='readables_with_conc',
                    uniqueKey='units', toDat='readables_conc_unique_units')

    dps.get_uniques(fromDat='readables_with_mol',
                    uniqueKey='units', toDat='readables_unique_units_mol')
    dps.get_uniques(fromDat='readables_with_mM',
                    uniqueKey='units', toDat='readables_unique_units_mM')

    dps.query_ontologies(fromDat='readables_unique',
                   uniqueKey='readable', toDat='readables_conc')

    dps.lookup(fromDat='readables_with_conc', searchByKey="readable",
                       matchesToReturn=5, keysToSubset=['label','iri','ontology_name'],
                       toDat="readables_with_lookup")
    dps.add_referring_id_as_property(fromDat='readables_with_lookup', idKey="models",
                                     includeReferringID=True, toDat="readables_with_lookup_ids")

    dps.replace_values_with_dict_where_matching(fromDat='readables_with_lookup_ids', newValues=cs.modelList, fromDatKey="models",
                                     newValuesKey="filename", mergeDuplicatesByKey="name", toDat="readables_with_lookup_model_objs")

    dps.extract_subset_of_keys(fromDat='readables_with_lookup_model_objs', keysToSubset=["models"], toDat="readables_with_just_models")

    print("complete")


if __name__ == '__main__':
    main()
