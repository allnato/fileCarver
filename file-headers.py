# file-headers.py
# goal get all hex data of supported filetypes and place them in an array

FILEMAP_DCT = {}
SIG_LST = []
SIG_MAX = 0

import StringIO
import csv
import inspect
import os
# TODO: faster string search
# TODO: detecting binary is easy, detecting ASCII is hard
import binascii

def loadSig(**item_opt):
	global FILEMAP_DCT
	global SIG_LST
	global SIG_MAX
	sig_file = "model/signatures.txt"

	with open(sig_file, "r") as f_inst:
		unparsed = csv.reader(f_inst, delimiter=',')
		for item in unparsed:
			parsed_head = "".join(item[1].split()).lower()
			FILEMAP_DCT[parsed_head] = item[0]
	SIG_LST = FILEMAP_DCT.keys()
	SIG_MAX = max((len(sig_inst) for sig_inst in SIG_LST)) * 2           # why multiply by 2? Why not remove it?

	# if this would not work, try to do the class solution

def identifySig(file_ptr, **item_opt):
	#identify signature, get hex data from head to trailer then return signature and hex data
	parsed_head = 

def parseFiles(**item_opt):
	# get start and end checkpoints and save them
	# continue to next checkpoint and identify signature
	# try saving all data to json to prevent memory degradation

def cur_file_dir():
    return os.path.dirname(inspect.getfile(inspect.currentframe()))

class Magician(object):
    def __init__(self,signatures_file=None):
        if not signatures_file:
            signatures_file = os.path.join(cur_file_dir(), 'signatures_GCK.txt')
        self.file_mapping = {}
        with open(signatures_file, "r") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                processed_header = "".join(row[1].split()).lower()
                self.file_mapping[processed_header] = row[0]
        self.signatures = self.file_mapping.keys()
        self.max_read = max((len(signature) for signature in self.signatures)
        ) * 2

    def identify(self, file_obj):                                        # this gets a freaking file object
        header_data = file_obj.read(self.max_read)
        hexified_header_data = binascii.hexlify(header_data)
        for signature in self.signatures:
            if hexified_header_data.startswith(signature):
                return self.file_mapping[signature]
        raise Exception("can't find file. Could it be a text file?")


def identify_file(filename):
    """
    Convenience function that takes in a filename
    """
    mage = Magician()
    with open(filename, 'rb') as f:
        return mage.identify(f)

def identify_str(string):
    """
    Convenience function that takes in a string buffer
    """
    f = StringIO.StringIO(string)
    mage = Magician()
    return mage.identify(f)
    
