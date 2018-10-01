from pyutils.file_io import *

pths = {}
pths['root'] = "/_/reps/cellml/dat/"
pths['models'] = pths['root'] + "models/"
pths['models_raw'] = pths['models'] + "raw/"
pths['models_processed'] = pths['models'] + "processed/"

ensure_paths_exist(pths.values())

fls = {}
fls['models'] = pths['models'] + "models.json"
fls['models_cleaned'] = pths['models'] + "models_cleaned.json"
