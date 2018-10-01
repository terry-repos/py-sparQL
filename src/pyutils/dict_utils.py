import collections
import textwrap
import copy
from copy import deepcopy
from str_utils import *
from pyutils.list_utils import *

import operator


def dict_to_str(inDict, outStr=""):

	for k,v in inDict.items():
		if (len(outStr)>0):
			outStr+="_"
		outStr += k + "-"
		if (isinstance(v, str)):
			outStr += v
		elif (isinstance(v, list)):
			outStr += list_as_str(v)
		elif (isinstance(v, dict)):
			outStr += dict_to_str(v)

	return outStr




def replace_value_text_in_list_of_dicts_for_key(inputDat, valFromThisKey, replaceThisText, withThisText=""):
	outList =[]
	for item in inputDat:
		item[valFromThisKey] = item[valFromThisKey].replace(replaceThisText,withThisText)
		outList.append(item)
	return outList



def replace_val_in_dict_for_key(item, valFromThisKey, newVal):

	item[valFromThisKey] = newVal
	return item




def get_uniques_by_key(inputDat, uniqueKey):
	uniques = list({v[uniqueKey]: v[uniqueKey] for v in inputDat}.values())
	return uniques


def rename_dict_keys(inDict, oldKey, newKey):

	inDict[newKey] = inDict[oldKey]
	del inDict[oldKey]

	return inDict



def copy_val_from_key_to_new_key(inDict, oldKey, newKey):
	inDict[newKey] = inDict[oldKey]

	return inDict


def subset_list_of_dicts_by_keys(listOfDicts, keepTheseKeys):
	# print(inDict.keys())
	outList = []
	for aDict in listOfDicts:
		outList += subset_dict_by_keys( aDict, keepTheseKeys )

	return outList

def subset_dict_by_keys(inDict, keepTheseKeys):
	# print(inDict.keys())
	outDict = {}
	for k in keepTheseKeys:
		outDict[k] = inDict[k]

	return outDict


def subset_list_of_dicts_by_keys(listOfDicts, keepTheseKeys):
	# print(inDict.keys())
	outList = []
	for aDict in listOfDicts:
		outList.append(subset_dict_by_keys( aDict, keepTheseKeys ))

	return outList



def get_vals_of_dict_from_hierarchy(inDict, hierarchyList):
	# print(inDict.keys())
	for k in hierarchyList:
		inDict = copy.deepcopy( inDict[k] )

	return inDict


def get_vals_of_list_of_dicts_from_hierarchy(listOfDicts, hierarchyList):
	outList = []

	for aDict in listOfDicts:
		outList.append(get_vals_of_dict_from_hierarchy( aDict, hierarchyList ))
		# print(diccounter, " ", outVals)

	return outList


def make_dict_serializable(inDictionary):
    newDict = {}

    for k, v in inDictionary.items():
        # print("type: ", str(type(v)))
        if 'ndarray' in str(type(v)):
            if 'float32' or 'float64' in str(type(v)):
                newDict[k] = v.astype(float)

        elif 'int' in str(type(v)):
            newDict[k] = int(v)

        elif isinstance(v, dict):
            newDict[k] = make_dict_serializable(inDictionary[k])

        else:
            newDict[k] = v

    return newDict


def dict_collections_update(oriDict, upDict):
    for kU, vU in upDict.items():
        if isinstance(vU, collections.Mapping):
            upd = dict_collections_update(oriDict.get(kU, {}), vU)
            oriDict[kU] = upd

        else:
            # print( "upDict[KU]: ", upDict[kU] )
            # print("ku: ", kU)
            # print(oriDict.keys())
            oriDict[kU] = upDict[kU]

    return oriDict


def dict_to_text_wrapped_str(dictToText, lineLength=100,sep="''"):

    singleLineDict = sep.join(['   {0} : {1}    '.format(k, v)
                              for k, v in dictToText.items()])
    return textwrap.fill(singleLineDict, lineLength)


def print_keys_hierarchy(tempDict={}, dictName="",  indent=0):
    if len(dictName) > 0:

        print(" **************** ", dictName.upper(), " ***************")

    if isinstance(tempDict, dict):

        for key, value in tempDict.items():

            if isinstance(key, str):
                print('\t' * indent + str(key))

            if isinstance(value, dict):
                print_keys_hierarchy(value, "", indent + 1)

            elif isinstance(value, str):
                print('\t' * (indent + 1) + str(value))

            elif 'ndarray' in str(type(value)):
                nNonNegOneItems = get_num_non_x_items(value, -1)
                print('\t' * (indent + 1) + "(" + list_as_str(value.shape,
                                                              "_") + "), total of: ", nNonNegOneItems)

            elif isinstance(value, int):
                print('\t' * (indent + 1) + str(value))

    else:
        print(tempDict)
        print(" ***************** ")

    if 'tempDict' in globals() or 'tempDict' in locals():
        del tempDict


def print_filenames_in_hier_dic(tempDict={}, indent=0):
    print("==================")

    if isinstance(tempDict, dict):

        for key, value in tempDict.items():

            if isinstance(key, str):
                print('\t' * indent + str(key))

            if isinstance(value, dict):
                print_filenames_in_hier_dic(value, indent + 1)

            elif 'FileAttributes' in str(type(value)):
                print('\t' * (indent + 1) + str(value.attr['Name']))

    if 'tempDict' in globals() or 'tempDict' in locals():
        del tempDict


def get_hierarchies_from_dict(inDictionary, hierToAppend=list(), wrapHierInList=False, allHiers=list(), currHier=list()):

    for keyz, valz in inDictionary.items():
        if keyz not in currHier:
            currHier.append(keyz)
        # print("currHier: ", currHier, " keyz: ", keyz)

        if isinstance(valz, dict):
            allHiers = copy.deepcopy(get_hierarchies_from_dict(
                valz, hierToAppend, wrapHierInList, copy.deepcopy(allHiers), copy.deepcopy(currHier)))

        else:
            if wrapHierInList:
                if len(hierToAppend) > 0:
                    outlist = [hierToAppend]
                else:
                    outlist = []
                outlist += [copy.deepcopy(currHier)]

            else:
                outlist = copy.deepcopy(currHier)

            allHiers.append(copy.deepcopy(outlist))

        # print("currHierPrior: ", currHier)
        currHier = copy.deepcopy(currHier[:-1])
        # print("currHierPost: ", currHier)

    # print("currHierPrior: ", currHier)
    # currHier = copy.deepcopy( currHier[ :-1] )
    # print("currHierPost: ", currHier)

    return allHiers


def get_child_and_parent_keys(hierarchicalDic, parentKeys=list(), childKeys=list()):
    # print("inDict: ", hierarchicalDic, " parentKeys: ", parentKeys, " childKeys: ", childKeys)
    for key, val in hierarchicalDic.items():
        if isinstance(val, dict):

            parentKeys.append(key)
            parentKeys, childKeys = get_child_and_parent_keys(
                val, parentKeys, childKeys)

        elif 'ndarray' in str(type(val)) or (val == None):
            childKeys.append(key)

    return list(set(parentKeys)), list(set(childKeys))


def get_init_x_empty_lists(x):
    return [list() for i in range(0, x)]


def get_first_key_in_dict(dictWithKey):
    return next(iter(dictWithKey))


def fst_k(dctWithKeys):
    if len(dctWithKeys.keys()) == 0:
        return None
    else:
        return next(iter(dctWithKeys))


def combine_listHierarchy_with_dictHierarchy(hierList, dicHier, newDict={}):
    # print("inList: ", inList, "inDict: ", inDict, " newDict: ", newDict)
    # print("upper g.cur: ", g.cur)
    if len(hierList) > 0:
        hItem = caps_under_to_cap_lower(hierList[0])
        if isinstance(hierList, list):
            for k in dicHier.keys():
                # print("item: ", hItem, " k: ", k)
                if hItem == caps_under_to_cap_lower(k):
                    newDict[hItem] = {}
                    newDict[hItem] = dict(combine_listHierarchy_with_dictHierarchy(
                        hierList[1:], dicHier[hItem], newDict[hItem]))
                    break
    else:
        # complete the dict with the hierarchy that was missing from the file
        newDict = merge_dicts(newDict, dicHier)

    # print("lower g.cur: ", g.cur)

    return newDict


def create_hierDict_from_levelsList_and_hierarchyList(lvlsList,  hierarchyLst, expandingDict={}):
    # print("inList: ", inList, "inDict: ", inDict, " expandingDict: ", expandingDict)
    # print("upper g.cur: ", g.cur)
    if len(hierarchyLst) > 0:
        if isinstance(hierarchyLst, list):
            hiItem = caps_under_to_cap_lower(hierarchyLst[0])
        else:
            hiItem = caps_under_to_cap_lower(hierarchyLst)

        for lvlStrs in lvlsList:
            # print("item: ", hItem, " k: ", k)
            formattedLvlStrs = list_of_strs_from_caps_under_to_cap_lower(
                lvlStrs)
            if hiItem in formattedLvlStrs:
                expandingDict[hiItem] = {}
                expandingDict[hiItem] = dict(create_hierDict_from_levelsList_and_hierarchyList(
                    lvlsList, hierarchyLst[1:], expandingDict[hiItem]))
                break

    # else:
    # 	# complete the dict with the hierarchy that was missing from the file
    # 	expandingDict = merge_dicts(expandingDict, dicHier)

    # print("lower g.cur: ", g.cur)

    return expandingDict


def select_events_by_hier_list(hierList, dicHier, newDict={}, tempList=[]):
    # print("inList: ", inList, "inDict: ", inDict, " newDict: ", newDict)
    # print("upper g.cur: ", g.cur)

    if len(tempList) > 0:

        hItem = caps_under_to_cap_lower(tempList[0])

        if isinstance(tempList, list):
            for k in dicHier.keys():
                print("item: ", hItem, " k: ", k)
                if hItem == caps_under_to_cap_lower(k):
                    newDict[hItem] = {}
                    newDict[hItem] = dict(combine_listHierarchy_with_dictHierarchy(
                        tempList[1:], dicHier[hItem], newDict[hItem]))
                    break

    else:
        # complete the dict with the hierarchy that was missing from the file
        if get_children_that_contains_all_specified_hierarchies(newDict, hierList):
            newDict = merge_dicts(newDict, dicHier)

    # print("lower g.cur: ", g.cur)

    return newDict


def remove_common_keys_defined_by_list(aDict, aList):

    if len(aList) > 0:

        aItem = aList[0]

        for k, v in aDict.items():

            if k == aItem:
                aDict = remove_common_keys_defined_by_list(aDict[k], aList[1:])

    return aDict


def stack_list_as_hierarchical_dict(hierLst, growDict={}):
    # print("hierLst: ", hierLst)

    if not hierLst == None and len(hierLst) > 0:

        possibleNewKey = caps_under_to_cap_lower(hierLst[0])
        # print(possibleNewKey)

        if len(possibleNewKey) > 0:

            if not possibleNewKey in growDict.keys():
                growDict[possibleNewKey] = {}

            newList = [item for item in hierLst if item != hierLst[0]]

            growDict[possibleNewKey] = copy.copy(
                stack_list_as_hierarchical_dict(newList, growDict[possibleNewKey]))

    return growDict


def set_nones_from_hierarchical_dict_to(dct, valueToSet):

    if isinstance(dct, dict):

        for k, v in dct.items():
            # print("V: ", v)

            # if v==None or v==False:

            if isinstance(v, dict):

                if len(v.keys()) == 0:
                    dct[k] = copy.copy(valueToSet)
                else:
                    dct[k] = copy.copy(
                        set_nones_from_hierarchical_dict_to(dct[k], valueToSet))

            else:

                dct[k] = copy.copy(valueToSet)

    else:
        dct = valueToSet

    return dct


def set_childmost_value_from_hierarchical_dict(hDict, valueToSet):

    if isinstance(hDict, dict):

        k = fst_k(hDict)
        if not k == None:
            hDict[k] = copy.deepcopy(
                set_childmost_value_from_hierarchical_dict(hDict[k], valueToSet))

        else:
            hDict = copy.deepcopy(valueToSet)

    return hDict


def merge_dicts(a, b):

    if isinstance(b, dict) and isinstance(a, dict):
        a_and_b_keys = a.keys() & b.keys()
        every_key = a.keys() | b.keys()

        return {k: merge_dicts(a[k], b[k]) if k in a_and_b_keys else
                deepcopy(a[k] if k in a else b[k]) for k in every_key}
    return deepcopy(b)


def get_childmost_key_from_hierarchical_dict(nestedDict, inList=[]):

    for key, val in nestedDict.items():
        if isinstance(val, dict):
            hierarchy = get_childmost_key(val, inList.append(key))

        else:
            return hierarchy

    return hierarchy


def set_value_in_dict_as_utmost_child(nestedDct, childElement):

    for key, val in nestedDct.items():

        if not isinstance(val, dict):
            if val == None:
                nestedDct[key.replace(g.params['SEP'], "")
                          ] = copy.copy(childElement)

        else:
            nestedDct[key.replace(g.params['SEP'], "")] = set_value_in_dict_as_utmost_child(
                nestedDct[key], childElement)

    return nestedDct


def get_dict_depth(dctDepth, depth=0):

    for key, val in dctDepth.items():
        if isinstance(val, dict):
            depth += 1
            depth = get_dict_depth(val, depth)

    return depth


def get_dict_depth_structure(dctToGetStructure):

    nSubEvents = 0
    nUnits = 0

    for key, valu in dctToGetStructure.items():

        if isinstance(valu, dict):
            nSubEvents += 1
            nUnits = 0
            for k, v in valu.items():
                nUnits += 1

        else:
            nUnits += 1

    return nSubEvents, nUnits


def insert_index_into_dict_with_hier_list(inputDict, inputHier, chanVal, index, NUM_CHANS):

    inputArr = copy.deepcopy(
        get_vals_from_dict_with_this_hierarchy(inputDict, inputHier))
    # print("inputArr.shape: ", inputArr.shape)
    if inputArr.shape[0] == 0:
        inputArr = get_init_channel_array(NUM_CHANS)
    updatedArr = copy.deepcopy(insert_index_into_arr(
        inputArr, chanVal, index, NUM_CHANS))
    updatedDict = set_vals_in_dict(inputDict, inputHier, updatedArr)

    return updatedDict


def set_indices_within_dict(dt, hierarchy, chanVal, inVals, nChans):

    if not hierarchy == None and len(hierarchy) > 0:

        key = caps_under_to_cap_lower(hierarchy[0])

        if len(key) > 0:

            if 'ndarray' in str(type(dt[key])):
                # print(type(inVals))
                if isinstance(inVals, int) or 'int' in str(type(inVals)):
                    dt[key] = insert_index_into_arr(
                        dt[key], chanVal, inVals, nChans)

                else:
                    # print("inVals: ", inVals)
                    # print("invals.shape: ", inVals.shape)
                    if inVals.shape[0] > dt[key].shape[1]:

                        newArray = np.full(
                            shape=(dt[key].shape[0], inVals.shape[0]), fill_value=-1)
                        newArray[0: dt[key].shape[0],
                                 0: dt[key].shape[1]] = dt[key]
                        dt[key] = np.copy(newArray)

                    dt[key][chanVal, 0:inVals.shape[0]] = copy.deepcopy(inVals)

                return dt

            else:
                newHierarchy = [
                    item for item in hierarchy if item != hierarchy[0]]

                dt[key] = copy.deepcopy(set_indices_within_dict(
                    dt[key], newHierarchy, chanVal, inVals, nChans))

    return dt


def set_vals_in_dict(floatDict, hierarchL, inValues, numChannels=None):
    if not check_hierarchy_in_dict(floatDict, hierarchL):
        # print("Hierarchy ", hierarchL, " not in dict! Initialising...")
        floatDict = copy.deepcopy(update_dict_with_a_new_initialised_hierarchy(
            floatDict,  hierarchL, nChans=numChannels))

    # print_keys_hierarchy(floatDict)
    # print(" hierarchy: ", hierarchL)

    if not hierarchL == None and len(hierarchL) > 0:

        key = caps_under_to_cap_lower(hierarchL[0])
        # print("key: ", key)

        if len(key) > 0:

            if isinstance(floatDict[key], dict):
                if not floatDict[key]:
                    floatDict[key] = copy.copy(inValues)
                    return floatDict

                else:
                    newHierar = [
                        item for item in hierarchL if item != hierarchL[0]]
                    floatDict[key] = copy.copy(set_vals_in_dict(
                        floatDict[key], newHierar, inValues, numChannels))

            else:
                floatDict[key] = copy.copy(inValues)
                return floatDict

    return floatDict


def update_hierarchical_dict_with_flat_dict(hieraDict, flatDict, hierList, chanVal, nChans):
    # print_keys_hierarchy(hieraDict)
    # print_keys_hierarchy(flatDict)
    # print("hierList: ", hierList)

    for ky, vl in flatDict.items():
        ky = caps_under_to_cap_lower(ky)
        hierList.append(ky)

        hieraDict = copy.copy(set_indices_within_dict(
            hieraDict, hierList, chanVal, vl, nChans))
        hierList.pop()

    return hieraDict


def check_hierarchy_in_dict(hierarchyDct, definedHierarchy):

    for khi, vals in hierarchyDct.items():
        if len(definedHierarchy) > 0:

            if khi in definedHierarchy:
                definedHierarchy = copy.deepcopy(
                    remove_this_item_from_list(khi, definedHierarchy))

            if isinstance(vals, dict):
                return copy.deepcopy(check_hierarchy_in_dict(vals, definedHierarchy))

        else:
            return True

    if len(definedHierarchy) > 0:
        return False

    else:
        return True


def update_dict_with_a_new_initialised_hierarchy(origDict, newHierarchy, nChans=None):
    # print(" newHierarchy: ", newHierarchy)
    tempDict = copy.deepcopy(stack_list_as_hierarchical_dict(newHierarchy, {}))
    if not nChans == None:
        initArray = np.full(shape=(nChans, 1), fill_value=-1)
        tempDict = copy.deepcopy(set_childmost_value_from_hierarchical_dict(
            tempDict, get_init_channel_array(nChans)))

    origDict = dict_collections_update(origDict, dict(tempDict))

    return origDict


def update_dict_with_a_new_ndarray(origDict, newHierarchy, inndarray, sl=None, nChans=None):
    # print(" newHierarchy: ", newHierarchy, "inndarray.shape[0]: ", inndarray.shape[0])
    # print("slice: ", sl, " type: ")
    if hasattr(sl, "__getitem__"):
        chan = sl[0]
        vals = get_vals_from_dict_with_this_hierarchy(origDict, newHierarchy)
        if not vals.any():
            vals = np.full(shape=(nChans, inndarray.shape[0]), fill_value=-1)

        if inndarray.shape[0] > vals.shape[1]:
            tempVals = np.full(
                shape=(nChans, inndarray.shape[0]), fill_value=-1)
            tempVals[0:vals.shape[0], 0:vals.shape[1]] = np.copy(vals)
            vals = np.copy(tempVals)

        # print("vals.shape: ", vals.shape, " inndarray.shape: ", inndarray.shape, " chan: ", chan)
        vals[chan, 0:inndarray.shape[0]] = inndarray
    else:
        vals = inndarray

    tempDict = copy.deepcopy(stack_list_as_hierarchical_dict(newHierarchy, {}))
    if not nChans == None:
        tempDict = copy.deepcopy(
            set_childmost_value_from_hierarchical_dict(tempDict, vals))

    origDict = dict_collections_update(origDict, dict(tempDict))

    return origDict


def get_vals_from_dict_with_this_hierarchy(inDictionary, inList, explicit=False, chanSlice=None):

    # print_keys_hierarchy(inDictionary)
    # print("inList: ", inList)

    if list_contains_list(inList):
        # print("note there are multiple lists: ", list_as_str(inList), ". Selecting the largest.")
        inList = get_largest_list(inList)

    for Khi, Val in inDictionary.items():
        if len(inList) > 0:
            if Khi == inList[0]:
                if isinstance(Val, dict):
                    return get_vals_from_dict_with_this_hierarchy(Val, inList[1:], explicit)
                else:
                    if not chanSlice == None:
                        return Val[chanSlice]

                    else:
                        return Val

    return np.array([])


def increment_int_in_hier_dict(inDicti, hire):

    baseVal = get_vals_from_dict_with_this_hierarchy(inDicti, hire)
    if isinstance(baseVal, list):
        if len(baseVal) == 0:
            baseVal = 1
        else:
            baseVal = baseVal[0] + 1
    else:
        baseVal += 1
    return set_vals_in_dict(inDicti, hire, baseVal)
