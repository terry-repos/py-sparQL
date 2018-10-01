# External imports
import json
import requests
# from jsonpath_rw import parse, jsonpath
from jsonpath_ng import parse, jsonpath

# Internal imports
from pyutils.file_io import *
from pyutils.print_formatting import *
from pyutils.xml_utils import *

from services.pmr_service import PMRService
from services.base_service import BaseService
from cellml.models import *
from pths import *


class CrawlerService(BaseService):
    def __init__(self, p=None, dp=None):
        self.PMRService = PMRService()

        if (p):
            super().__init__(p)

    def start():
        pass


    def fetch_model_list(self, fromPMR=False):
        if (fromPMR):
            self.modelList = self.PMRService.request_model_list()
            save_dat( self.modelList, fls['models'] )

        else:
            self.modelList = load_file( fls['models'] )

        self.modelList = self.modelList['collection']['links']
        print("self.modelList: ", self.modelList)
        # modelsCleaned = list({'href':item['href'].replace("/view",""), item} for item in self.modelList.items())
        modelsCleaned = []

        modelsCleaned = replace_value_text_in_list_of_dicts_for_key(self.modelList, valFromThisKey="href", replaceThisText="/view", withThisText="")
        modelsCleaned = [ rename_dict_keys(item, "prompt", "model_name") for item in modelsCleaned ]
        modelsCleaned = subset_list_of_dicts_by_keys(modelsCleaned, ['href', 'model_name'])
        modelsCleaned = [ copy_val_from_key_to_new_key( item, "href", "filename" ) for item in modelsCleaned ]

        outModels = []
        for modelC in modelsCleaned:
            modelC['filename'] = get_file_from_path(modelC['filename'])
            outModels.append(modelC)

        self.modelList = modelsCleaned
        save_dat(modelsCleaned, fls['models_cleaned'] )

        self.modelUrls = get_vals_of_list_of_dicts_from_hierarchy(self.modelList, ['href'])

        print("number of model urls: ", len(self.modelUrls))



    def download_models(self, nModels=None, overwrite=False):

        count = 0
        print(dir(self))
        for url in self.modelUrls:
            if self.nModels and count > self.nModels:
                print("Max models ", nModels, " reached.")
                break

            count += 1

            url = url.replace("/view", "")
            filename = get_file_from_path(url)

            fileAndPath = pths['models_raw'] + filename

            if not os.path.isfile(fileAndPath) or overwrite:
                print("Model ", filename, " not found. Downloading ...")
                response = requests.get(url)
                save_file(response.text.encode('utf8'), fileAndPath)
