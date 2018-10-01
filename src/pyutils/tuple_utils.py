import collections
import textwrap
import copy
from copy import deepcopy
from str_utils import *


def insert_into_tuple( tupleToInsert, itemToInsert, pos=0 ):
	tupleToInsert = list(tupleToInsert)
	tupleToInsert.insert(pos, itemToInsert)
	return tuple(tupleToInsert)


def pop_from_tuple( tupleToPop, pos=0 ):
	tupleToPop = list(tupleToPop)
	poppedItem = tupleToPop.pop( pos )
	return poppedItem, tuple(tupleToPop)

def tuple_to_str( tupleToStr, separator="_" ):
	pass
