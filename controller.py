#controller.py

# 764 images in transcend1.dd
# 2 images in usbimage.dd

from init_images import *
from file_headers2 import *
import os

if __name__ == '__main__':
	file_name = 'generated-images/transcend1.dd' ############################# DEBUG
	output_path = 'output/'
	
	welcome()
	
	if not os.path.isdir(output_path):
		try:
			os.makedirs(output_path)
		except OSError:
			print("Error: " + output_path + " directory cannot be created\n")
			exit(-1)
	
	while not file_name:
		inpt = input("Do you have a raw image for analysis? [y/n] ")
		if inpt == "n":
			dev = selectDrive(debug=0)
			file_name = toRawImage("", dev, debug=0)
		elif inpt == "y":
			while True:
				file_name = input("Enter full path and file name of the raw image: ")
				
				if os.path.isfile(file_name):
					break
				else:
					print("Error: " + file_name + " cannot be found.\n")
				
		else:
			print("Error: Invalid input")
	
	(lst_srt, lst_end, lst_types, lst_buf) = compileRegs()
	readImage(file_name, lst_srt, lst_end, lst_types, lst_buf)
	
	# cleanFiles()
	
	exit(0)
