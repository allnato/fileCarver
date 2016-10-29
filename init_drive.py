# init_drive.py
# attempt to do os.open() and pip install here

import sys, os, binascii, math, string
from sys import platform
from subprocess import check_output

def listDrive(**item_opt):
	lst_devs = []
	lst_fll = []

	if platform == "linux" or platform == "linux2":
		unparsed = check_output(['ls -l /dev/disk/by-id/usb*'])

		lst_devs = unparsed.split("\n")

		for dev_inst in lst_devs:
			if dev_inst:
				dev_inst = dev_inst[:dev_inst.find('../../')+6]          #output should be /dev/<dev name>
				lst_fll.append(dev_inst)
	elif platform == "win32":
		try:
			import win32file
		except:
			print("Error: There are incomplete dependencies on this computer. Please install pypiwin32.")
			exit(-1)

		drive_types = { "0": "Unknown", "1": "No Root Directory", "2": "Removable Disk", "3": "Local Disk",
		                "4": "Network Drive", "5": "Compact Disc", "6": "RAM Disk" }

		for c_inst in string.ascii_lowercase:
			if (win32file.GetLogicalDrives() >> (ord(c_inst.upper()) - 65) & 1) != 0:
				c_inst = c_inst.upper() + ":\\"
				drive_name = drive_types[str(win32file.GetDriveType(c_inst))]
				lst_fll.append(c_inst + "   " + drive_name)
	else:
		print("Platform not yet supported")
		exit(-1)

	return lst_fll

def getDrive(lst_drive, selected_num, **item_opt):                       # selected_num from GUI; lst_drive from backend
	drive = lst_drive[selected_num]
	return("\\\\.\\" + drive[:2])

def getDrivePercentProgress(written_size, total_size):                   # give value to view
	cur_size = written_size*1.0 / total_size * 100
	return("%.2f" % cur_size)

def toRawImage(file_name, output_path, dev_path, **item_opt):            # returns full path to generated image
	written_size = 0

	total_size = 100000000#os.path.getsize(dev_path)

	if "bs" in item_opt:
		bs = item_opt["bs"]
	else:
		bs = 1048576

	if not os.path.isdir(output_path):
		try:
			os.makedirs(output_path)
		except OSError:
			#print("Error: " + output_path + " directory cannot be created\n") ################## DISPLAY ERROR MESSAGE @to_GUI
			exit(-1)

		print("\n[+] Writing to raw image file. This may take a while...")  # @to_GUI

	file_loc = output_path + file_name

	with open(dev_path,'rb') as dev:
		with open(file_loc, 'wb') as img:
			while True:
				if img.write(dev.read(bs)) == 0:
					break
				written_size = written_size + bs
				prog = getDrivePercentProgress(written_size, total_size)           # @to_GUI

	return file_loc
