# init_drive.py
# attempt to do os.open() and pip install here

import sys, os, binascii, math, string, subprocess
from sys import platform
from timeit import default_timer as timer
from man_time import getPercentAndRemainProgress

def listDrive(**item_opt):
	lst_fll = []

	if platform == "linux" or platform == "linux2":
		lst_temp = []
		lst_devs = []

		proc = subprocess.Popen("df | grep ^/dev/", stdout=subprocess.PIPE, shell=True)
		(unparsed, err) = proc.communicate()

		lst_devs = unparsed.decode('utf-8').split("\n")

		for dev_inst in lst_devs:
			lst_temp = dev_inst.split()    #output should be /dev/<dev name>
			if lst_temp:
				lst_fll.append(lst_temp[0] + "   " + lst_temp[5])

	elif platform == "win32":
		try:
			import win32file
		except:
			#print("Error: There are incomplete dependencies on this computer. Pypiwin32 will be installed.") ######## DISPLAY ERROR MESSAGE @to_GUI
			try:
				subprocess.Popen("pip install pypiwin32", shell=True)
			except:
				#print("Error: Pypiwin32 cannot be installed.")
				exit(-1)

		drive_types = { "0": "Unknown", "1": "No Root Directory", "2": "Removable Disk", "3": "Local Disk",
		                "4": "Network Drive", "5": "Compact Disc", "6": "RAM Disk" }

		for c_inst in string.ascii_lowercase:
			if (win32file.GetLogicalDrives() >> (ord(c_inst.upper()) - 65) & 1) != 0:
				c_inst = c_inst.upper() + ":\\"
				drive_name = drive_types[str(win32file.GetDriveType(c_inst))]
				lst_fll.append(c_inst + "   " + drive_name)
	else:
		#print("Platform not yet supported")                             ########### DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)

	return lst_fll

def getDrive(lst_drive, selected_num, **item_opt):                       # selected_num from GUI; lst_drive from backend
	drive = lst_drive[selected_num]
	if platform == "linux" or platform == "linux2":
		return drive.split()[0]
	elif platform == "win32":
		return("\\\\.\\" + drive[:2])
	else:
		#print("Platform not yet supported")                             ########### DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)

def toRawImage(file_name, output_path, dev_path, **item_opt):            # returns full path to generated image
	file_name = file_name + ".dd"                                        # assume that the file_name has no file extension
	written_size = 0
	total_size = getDriveTotal(dev_path)
	output_path = os.path.normcase(output_path)
	start_time = timer()

	if "bs" in item_opt:
		bs = item_opt["bs"]
	else:
		bs = 1048576

	if not os.path.isdir(output_path):
		try:
			os.makedirs(output_path)
		except OSError:
			print("Error: " + output_path + " directory cannot be created\n", file=sys.stderr) ################## DISPLAY ERROR MESSAGE @to_GUI
			exit(-1)

	#print("\n[+] Writing to raw image file. This may take a while...")  # @to_GUI

	file_loc = output_path + file_name

	with open(dev_path,'rb') as dev:
		with open(file_loc, 'wb') as img:
			while True:
				if img.write(dev.read(bs)) == 0:
					break
				written_size = written_size + bs
				prog, rem_time = getPercentAndRemainProgress(written_size, total_size, start_time)           # @to_GUI
				yield "data:" + str(prog) + " " + str(rem_time) + "\n\n"

	return file_loc

# Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
# License: MIT

def getDriveTotal(dev_path):
	import collections

	_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

	if platform == "linux" or platform == "linux2":
		import shutil

		def disk_usage(path):
			st = shutil.disk_usage(path)
			free = st.free * 15.1898
			total = st.total * 15.1898
			used = st.used * 15.1898
			return _ntuple_diskusage(total, used, free)

	elif platform == "win32":
		import ctypes
		import sys

		def disk_usage(path):
			path = path[4:]
			_, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
							   ctypes.c_ulonglong()
			if sys.version_info >= (3,) or isinstance(path, unicode):
				fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
			else:
				fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
			ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
			if ret == 0:
				raise ctypes.WinError()
			used = total.value - free.value
			return _ntuple_diskusage(total.value, used, free.value)
	else:
		#raise NotImplementedError("Error: Platform not supported.") ################## DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)

	disk_usage.__doc__ = __doc__

	usage = disk_usage(dev_path)
	return usage.total
