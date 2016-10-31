# control_proc.py

from init_drive import *
from model_app import *
from head_file import *
import os

def initDrive(**item_opt):
	drives = listDrive()
	print(drives)

	selected_drive = getDrive(drives, 4)
	print(selected_drive)

	prog = getDrivePercentProgress(33, 1000)
	print(str(prog) + "%")

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
	prog, file_ctr = getReadProgress(333, 10000, 56)
	print(prog)
	print(file_ctr)

	(lst_srt, lst_end, lst_buf) = compileRegs(["doc", "jpg", "pdf", "png", "xls"])
	print(lst_srt)
	print(lst_end)
	print(lst_buf)
	if platform == "linux" or platform == "linux2":
		fastReadImage("/dev/sdb1", "../output/test[", lst_srt, lst_end, ["doc", "jpg", "pdf", "png", "xls"], lst_buf)
	elif platform == "win32":
		fastReadImage("\\\\.\\H:", "../output/test[", lst_srt, lst_end, ["doc", "jpg", "pdf", "png", "xls"], lst_buf)
	else:
		exit(0)

modelApp()
initDrive()
headFile()
