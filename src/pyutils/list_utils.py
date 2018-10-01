import collections
import textwrap
import copy
from copy import deepcopy
from str_utils import *





def list_contains_list(obj):
	return any(isinstance(item, list) for item in obj)


def list_as_str(lstToMakeStr, joinerStr="_", outSt=""):
	if isinstance( lstToMakeStr, list ) :
		if list_contains_list_of_list(lstToMakeStr) :
			lstToMakeStr = copy.deepcopy(lstToMakeStr[0])

		if list_contains_list(lstToMakeStr) :
			for listI in lstToMakeStr :
				outSt += list_as_str( listI, joinerStr , outSt)
		else:
			outSt = ''.join( [ str(itStr) + joinerStr for itStr in lstToMakeStr ] )
	else :
		return str(lstToMakeStr)

	if len(outSt) > 0:
		if outSt[-1] == joinerStr:
			return outSt[:-1]
		else:
			return outSt
	else:
		return ""



def remove_str_from_list(obj):
	return [item for item in obj if not isinstance(item, str)]



def list_has_substr_of_str(incomingLst, compareStr):
	for item in incomingLst:
		if item in compareStr:
			return True
	return False


def round_items_in_list(inList, nDecimals=4) :
	# print("inList: ", inList)
	inList = remove_str_from_list(inList)
	# print("after Removing Str from list: ", inList)

	float_formatter = lambda x: "%.4f" % x
	roundedList = [ float_formatter( item ) for item in inList ]
	return roundedList


def list_contains_list_of_list(potentialListsOfLists) :
	listContainsListOfList = False

	for potentialLists in potentialListsOfLists :
		if isinstance(potentialLists, list):
			if len(potentialLists) > 0 :
				listContainsListOfList = list_contains_list(potentialLists)

	return listContainsListOfList


def list_contains_list_of_list_of_lists(potentialListsOfLists) :
	listContainsListOfListOfLists = False

	for potentialLists in potentialListsOfLists :
		if isinstance(potentialLists, list):
			if len(potentialLists) > 0 :
				listContainsListOfListOfLists = list_contains_list_of_list(potentialLists)

	return listContainsListOfListOfLists



def get_init_x_empty_lists(x):
	return [list() for i in range(0,x)]



def one_of_this_list_in_that_list(thisList, thatList) :
	for thisItem in thisList :
		if thisItem in thatList :
			return True
	return False



def get_item_in_bothLists(thisList, thatList) :
	for thisItem in thisList:
		if thisItem in thatList:
			return thisItem
	return None



def make_list_if_not(strOrList):
	if not isinstance(strOrList, list):
		return [strOrList]
	else:
		return strOrList



def all_of_this_list_in_that_list(thisList, thatList) :

	thisList = make_list_if_not(thisList)
	thatList = make_list_if_not(thatList)

	for thisItem in thisList:
		if not thisItem in thatList:
			print("no match")
			return False
	return True



def get_unique_items_in_list(listToGetUniques):
	uniqueItems = []
	iterator = 0
	for item in listToGetUniques:
		iterator+=1
		if item not in listToGetUniques[iterator:] :
			uniqueItems.append(item)
	return uniqueItems


def all_of_this_list_in_all_of_that_list(thisList, thatList) :
	if not len(thisList) == len(thatList):
		return False

	for thisItem in thisList:
		if not thisItem in thatList:
			return False
	return True



def list_of_strs_from_caps_under_to_cap_lower(inListOfstrs):
	return [caps_under_to_cap_lower(strItem) for strItem in inListOfstrs]



def select_events_by_hier_list(hierList, dicHier, newDict={}, tempList=[]) :
	# print("inList: ", inList, "inDict: ", inDict, " newDict: ", newDict)
	# print("upper g.cur: ", g.cur)

	if len(tempList) > 0 :

		hItem = caps_under_to_cap_lower(tempList[0])

		if isinstance(tempList, list) :
			for k in dicHier.keys() :
				print("item: ", hItem, " k: ", k)
				if hItem == caps_under_to_cap_lower(k) :
					newDict[hItem] = {}
					newDict[hItem] = dict(combine_listHierarchy_with_dictHierarchy(tempList[1:], dicHier[hItem], newDict[hItem] ))
					break

	else:
		# complete the dict with the hierarchy that was missing from the file
		if get_children_that_contains_all_specified_hierarchies(newDict, hierList) :
			newDict = merge_dicts(newDict, dicHier)

	# print("lower g.cur: ", g.cur)

	return newDict



def remove_this_list_from_that_list( listToRemove, listToKeep ) :
	return [ itemToKeep for itemToKeep in listToKeep if itemToKeep not in listToRemove]


def remove_this_item_from_list( itemToRemove, listToKeep ) :
	return [ itemToKeep for itemToKeep in listToKeep if not itemToKeep==itemToRemove]


def flatten_list_of_list( listOfLists ) :
	return [ item for sublist in listOfLists for item in sublist ]


def get_smallest_list( listOfLists ) :
	minListLen = 10000
	listToReturn = []
	for innerList in listOfLists :
		if len( innerList ) < minListLen :
			listToReturn = copy.deepcopy(innerList)
			minListLen = len( innerList )
	return listToReturn


def get_largest_list( listOfLists ) :
	maxListLen = 0
	listToReturn = []

	for innerList in listOfLists :
		if len( innerList ) > maxListLen :
			listToReturn = copy.deepcopy(innerList)
			maxListLen = len( innerList )

	return listToReturn


def remove_empty_strs_from_list(inStr):
	return [st for st in inStr if not st == '']
