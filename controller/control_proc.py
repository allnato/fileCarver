# control_proc.py

from init_drive import *
from model_app import *
from head_file import *
from man_time import *
from burn_drive import *
from timeit import default_timer as timer
import os

def initDrive(**item_opt):
	drives = listDrive()
	print(drives)

	selected_drive = getDrive(drives, 4)
	print(selected_drive)

	#toRawImage("transcend1", "../generated-images/", selected_drive)        # Image file detected! Do you want to use or overwrite the image file?

def modelApp(**item_opt):
	(lst_srt, lst_end, lst_buf) = compileRegs(["doc", "jpg", "png", "xls"])
	print(lst_srt)
	print(lst_end)
	print(lst_buf)

	str_choice = getScanChoice(2)
	print(str_choice)

	full_prefix = namingFile("output\\testData", "dog")
	print(full_prefix)

def headFile(**item_opt):

	(lst_srt, lst_end, lst_buf) = compileRegs(["doc", "jpg", "pdf", "png", "xls"])
	print(lst_srt)
	print(lst_end)
	print(lst_buf)
	if platform == "linux" or platform == "linux2":
		fastReadImage("/dev/sdb1", "../output/test[", lst_srt, lst_end, ["doc", "jpg", "pdf", "png", "xls"], lst_buf)
	elif platform == "win32":
		fastReadImage("../generated-images/image.dd", "../output/test[", lst_srt, lst_end, ["doc", "jpg", "pdf", "png", "xls"], lst_buf)
	else:
		exit(0)

def manTime(**item_opt):
	
	start_time = timer()
	total_size = 100000
	
	for i in range(0, total_size):
		prog, rem_time = getPercentAndRemainProgress(i, total_size, start_time)
		print(str(prog) + "%\nTime remaining: " + str(rem_time))

def burnDrive(**item_opt):
	block_size = 8192
	start_time = timer()
	raw_total = getDriveTotal("\\\\.\\H:")
	print(raw_total)
	
	rand_cont = setContents(block_size, "0")
	#print(rand_cont)
	#print(len(rand_cont))
	
	block_total = int(math.ceil(raw_total / block_size))
	
	#cleanDrive("\\\\.\\H:", block_total, block_size, "0")
	#buildDrive("\\\\.\\H:")
	
	passDrive(0, "\\\\.\\H:", raw_total, block_size)
	buildDrive("\\\\.\\H:")

#modelApp()
#initDrive()
#headFile()
#manTime()
burnDrive()
