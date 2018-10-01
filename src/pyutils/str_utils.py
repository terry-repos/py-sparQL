import sys
import copy
import re
from dict_utils import *
from pyutils.str_utils import *
from pyutils.list_utils import *


def strip_non_alpha_numeric(inText):
    pattern = re.compile('[\W]+')
    # pattern = re.compile('/[A-Za-z0-9 ]/')
    # pattern = re.compile('[^ \w]"')
    return pattern.sub(' ', inText).strip()

def make_mix_str(listOrTuple, sep="_"):
    outStr = ""
    for item in listOrTuple:
        print(type(item))
        if len(outStr) > 0:
            outStr += sep

        if (isinstance(item, dict)):
            print(item)
            outStr+=(dict_to_text_wrapped_str(item))

        elif (isinstance(item, list)):
            outStr += list_as_str(item, sep)

        else:
            outStr+=(str(item))

    return outStr


def append_to_filename(filename, append, withUnderscore=True):
    ext = filename.rsplit('.', 1)[1]
    filenameNoExt = filename.rsplit('.', 1)[0]
    if withUnderscore:
        append = "_" + append
    newFilename = filenameNoExt + str(append) + "." + ext
    return newFilename



def change_extension(filename, newExt):
    return filename.rsplit('.', 1)[0] + "." + newExt


def get_upper_case_indices(s) :
    return [i for i, c in enumerate(s) if c.isupper()]


def get_sub_str_between_strs(inStr, prefaces, suffix) :
	print("prefaces: ", prefaces)
	print("suffaces: ", suffix)

	if isinstance(prefaces, list):
		for prefix in prefaces :
			startLoc = inStr.upper().index(prefix.upper())
			if not ((startLoc==None) or (startLoc==0)) :
				break
		prefaces = prefix
	else:
		startLoc = inStr.upper().index(prefaces.upper())


	endLoc = inStr.upper().index(suffix)
	return (inStr[ ( startLoc + len(prefaces)) : endLoc ])





def find_each_char_in_str(inStr, charVal) :

	return [i for i, letter in enumerate(inStr) if letter == charVal]


def contains_only_upper(inStr) :

	for l in inStr:
		if not l==l.upper() :
			return False
	return True


def contains_only_lower(inStr) :
	for l in inStr:
		if not l==l.lower() :
			return False
	return True


def make_first_letter_lower_case(subjectStr) :
	return subjectStr[0].lower() + subjectStr[1:]



def caps_under_to_cap_lower(inStr, synonymDict=None) :
	underscorePoses = find_each_char_in_str(inStr, '_')
	# print(underscorePoses)
	priorPos = 0
	outStr = ""

	inStr = inStr.replace("*","")

	if len(underscorePoses) > 0 or ((contains_only_upper(inStr) or contains_only_lower(inStr)) and len(inStr) > 0):
		for pos in underscorePoses :
			outStr += inStr[priorPos].upper()
			outStr += inStr[(priorPos+1):(pos)].lower()
			priorPos = pos+1

		outStr += inStr[priorPos].upper()
		outStr += inStr[priorPos+1:].lower()
	else:
		outStr = inStr

	return outStr


def make_lower_case_if_possible(inVal) :

	if isinstance(inVal, str):
		inVal = inVal.lower()

	return inVal



def insert_char_at_pos(strToManip=None, charToInsert ='_' , poses=None, indexI=0) :

	if len(poses) > 0 :

		pos = poses.pop(0)
		if pos > 0:
			outStr = strToManip[:(pos+indexI)] + charToInsert + strToManip[(pos+indexI):]
			indexI+=1
			strToManip = insert_char_at_pos(outStr, charToInsert, poses, indexI)

	return strToManip.upper()



def print_match(inStr, matchStr="") :
	if len(matchStr) > 0:
		if inStr.upper() in matchStr.upper():
			print(" " + inStr)
	else:
		print(" " + inStr)


def add_synonyms(inStr, synonymDict) :
	outStrs = []
	outStrs.append(inStr)

	for key, val in synonymDict.items() :

		manipStr = copy.copy(inStr)
		# print("key: ", key, " val: ", val, " manipStr: ", manipStr)

		if key.upper() in inStr.upper() :

			outStr = copy.copy(manipStr.replace(caps_under_to_cap_lower(key), caps_under_to_cap_lower(val)))
			outStrs.append(outStr)

		manipStr2 = copy.copy(inStr)

		if val.upper() in inStr.upper() :

			outStr2 = copy.copy(manipStr2.replace(caps_under_to_cap_lower(val), caps_under_to_cap_lower(key)))
			outStrs.append(outStr2)

	return outStrs



def replace_synonyms(inStr, synonymDict) :

	for key, val in synonymDict.items():
		inStr = inStr.replace(caps_under_to_cap_lower(key), caps_under_to_cap_lower(val))

	return inStr



def remove_last_chunk_from_str(inStr, separator) :

	if separator in inStr:
		chunkPos = len(inStr) - inStr[::-1].index(separator) - 1
		inStr = inStr[:chunkPos]

	return inStr



def check_if_more_than_two_chunks( inStr, separator ) :

	separatorPoses = find_each_char_in_str(inStr, separator)
	if len(separatorPoses) > 1 :
		return True

	else :
		return False



def get_int_vals_from_str( inputStr, prefix=None ) :
	lenPrefix = len(prefix)
	startPosOfInt = inputStr.upper().index(prefix.upper()) + lenPrefix
	restOfStr = inputStr[ startPosOfInt : ]
	intStr = ""
	# print("inputStr: ", inputStr, " prefix: ", prefix, " restOfStr: ", restOfStr)

	for char in restOfStr :
		if ( char=='-' ) or ( char.isdigit() ) :
			intStr += char

		else :
			break

	return int(intStr)
