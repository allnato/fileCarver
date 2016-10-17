# init-images.py

import os
import binascii
from sys import platform
from subprocess import check_output

def welcome(**item_opt):
	print("""
##########################
#
#
#
#
##########################

Currently supported file types: jpg, png, doc, xls

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
	else:
		print("Platform not yet supported")
		exit(-1)
		
	for i in range(len(lst_fll)):                                        #display drives and ask the user to select
		print((i+1) + ": " + lst_fll[i] + "\n")
	
	dev_num = 0
	while dev_num < 1 and dev_num > len(lst_fll):
		try:
			dev_num = int(raw_input("\nSelect device number: "))
		except ValueError:
			print("Error: Invalid number\n")
			
	if "debug" in item_opt and item_opt["debug"] != 0:
		print("\n[!] The selected device: " + lst_fll[dev_num-1]+ "\n")
			
	return lst_fll[dev_num-1]

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
		print("The raw image file will be written to " + output_path)
		file_name = raw_input("\nEnter name for the image: ") + ".dd"    #invalid filenames will be checked (in the future) and in the gui version
	
	with open(dev_path,'rb') as dev:
		with open(output_path + file_name, 'wb') as img:
			while True:
				if img.write(dev.read(bs)) == 0:
					break
					
	if "debug" in item_opt and item_opt["debug"] != 0:
		print("\n[!] The image is written to: " + output_path + file_name + "\n")
	
	return file_name

def readImage(file_name, **item_opt):                                     #as of now, all images will be read from generated-images/
	
	with open(file_name, 'rb') as img:
		data = img.read()
	
	hex_data = binascii.hexlify(data)
	
	if "debug" in item_opt and item_opt["debug"] != 0:
		print("================HEX DATA=============================\n %s", hex_data)

	return hex_data

