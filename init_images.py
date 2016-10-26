# init-images.py

import os
import binascii
from sys import platform
from subprocess import check_output
import string

def welcome(**item_opt):
	print("""
  ______ ____  _____  ______ _   _  _____ _____ _____  _____   __  ___ __             
 |  ____/ __ \|  __ \|  ____| \ | |/ ____|_   _/ ____|/ ____| /_ |/ _ /_ |            
 | |__ | |  | | |__) | |__  |  \| | (___   | || |    | (___    | | | | | |            
 |  __|| |  | |  _  /|  __| | . ` |\___ \  | || |     \___ \   | | | | | |            
 | |   | |__| | | \ \| |____| |\  |____) |_| || |____ ____) |  | | |_| | |            
 |_|____\____/|_|  \_|______|_|_\_|_____/|_____\_____|_____/   |_|\___/|_|_____     __
 |  ____|_   _| |    |  ____| |  __ \|  ____/ ____/ __ \ \    / |  ____|  __ \ \   / /
 | |__    | | | |    | |__    | |__) | |__ | |   | |  | \ \  / /| |__  | |__) \ \_/ / 
 |  __|   | | | |    |  __|   |  _  /|  __|| |   | |  | |\ \/ / |  __| |  _  / \   /  
 | |     _| |_| |____| |____  | | \ \| |___| |___| |__| | \  /  | |____| | \ \  | |   
 |_|    |_____|______|______| |_|  \_|______\_____\____/   \/   |______|_|  \_\ |_|   
                                                                                      
========================================================================================

Currently supported file types: jpg, png, doc, xls, pdf
""")

#def argHandler(**item_opt)                                              #add soon

#def help(**item_opt)                                                    #add soon

def selectDrive(**item_opt):
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
		import win32file
		
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
		
	for i in range(len(lst_fll)):                                        #display drives and ask the user to select
		print((i+1), ": ", lst_fll[i])
	print("")
	
	dev_num = 0
	while dev_num < 1 or dev_num > len(lst_fll):
		try:
			dev_num = int(input("Select device number: "))
		except ValueError:
			print("Error: Invalid number\n")
	
	drive = lst_fll[dev_num-1]
			
	if "debug" in item_opt and item_opt["debug"] != 0:
		print("\n[~] The selected device: " + drive[:2] + "\n")
		exit(0)
	
	return("\\\\.\\" + drive[:2])

def toRawImage(file_name, dev_path, **item_opt):
	output_path = "generated-images/"
	
	if "bs" in item_opt:
		bs = item_opt["bs"]
	else:
		bs = 65536                                                       #optimal bytes per sector for large images
	
	if not os.path.isdir(output_path):
		try:
			os.makedirs(output_path)
		except OSError:
			print("Error: " + output_path + " directory cannot be created\n")
			exit(-1)
	
	while not file_name:
		print("The raw image file will be written to: " + output_path)
		file_name = input("\nEnter name for the image: ") + ".dd"    #invalid filenames will be checked (in the future) and in the gui version
		print("\n[+] Writing to raw image file. This may take a while...")
	
	file_loc = output_path + file_name
	
	with open(dev_path,'rb') as dev:
		with open(file_loc, 'wb') as img:
			while True:
				if img.write(dev.read(bs)) == 0:
					break
					
	if "debug" in item_opt and item_opt["debug"] != 0:
		print("\n[~] The image is written to: " + file_loc + "\n")
	
	return file_loc
