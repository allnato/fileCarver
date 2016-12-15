#burn_drive.py

#reformat drive

import win32api, os, binascii, random, math
from init_drive import setStructure
from subprocess import Popen, PIPE
from man_time import getPercentAndRemainProgress
from timeit import default_timer as timer

start_time = 0
cur_pass = 0
max_pass = 1

def setContents(block_size, val_pool, **item_opt):
	rand_cont = ""
	
	if len(val_pool) > 1:
		for i in range(0, block_size):
			encrypt_val = random.choice(val_pool)
			rand_cont = rand_cont + encrypt_val
	else:		
		for i in range(0, block_size):
			rand_cont = rand_cont + val_pool
			
	rand_cont = rand_cont.encode('utf-8')
	rand_cont = binascii.unhexlify(rand_cont)
	return rand_cont

def cleanDrive(dev_path, block_total, block_size, chr_item): # should only be called by passDrive
	global cur_pass
	
	block_num = 0
	block_mark = 0

	dev = open(dev_path, 'r+b')
	dev.close()

	item = setContents(block_size, chr_item)
	
	init_total = int(block_total / 10)
	
	try:
		with open(dev_path, 'r+b') as dev:
			for i in range(0, init_total):
				try:
					dev.seek(block_size * block_num)
					block_num = block_num + 1
					block_mark = block_mark + 1
					
					item = setContents(block_size, chr_item)
					dev.write(item)
				except:
					block_num = block_num + 1
	except:
		pass

	#block_num = 0 # if the drive is not really shredded even after multiple passes, uncomment this statement to start shredding from block 0
	block_num = block_mark
	block_size = block_size * 2

	try:
		with open(dev_path, 'r+b') as dev:
			for j in range(block_mark, block_total):
				try:
					prog, rem_time = getPercentAndRemainProgress(block_num * (cur_pass + 1), block_total * max_pass, start_time)     # @to_GUI
					yield "data:" + str(prog) + " " + str(rem_time) + " " + str(cur_pass) + " " + str(max_pass) "\n\n"
					
					dev.seek(block_size * block_num)
					block_num = block_num + 1
					
					item = setContents(block_size, chr_item)
					dev.write(item)
				except:
					block_num = block_num + 1
	except:
		pass
		
	#print("cur_pass: " + str(cur_pass))
	cur_pass = cur_pass + 1

def passDrive(scan_opt, dev_path, raw_total, block_size, **item_opt): # only for hard drives - if flash drive, just execute the clean drive directly
	#pass_map = {"0": "Zero Flash", "1": "PseudoRandom Flash", "2": "BinZero Passes", 
	#"3": "U.S. Navy NAVSO P-5239-26", "4": "U.S. Air Force System Security 5020", "5": "Gutmann's Algorithm"}
	
	global start_time, cur_pass, max_pass

	rand_data = "0123456789ABCDEF"
	rand_char = "ABCDEF"
	rand_numb = "1234567890"
	
	block_total = int(math.ceil(raw_total / block_size))
	start_time = timer()
	cur_pass = 0        # reset when passDrive is called again
	
	if scan_opt == 0:
		cleanDrive(dev_path, block_total, block_size, "0")
	elif scan_opt == 1:
		cleanDrive(dev_path, block_total, block_size, rand_data)
	elif scan_opt == 2:
		max_pass = 3
		
		for i in range(0, max_pass):
			cleanDrive(dev_path, block_total, block_size, "0")
	elif scan_opt == 3:
		max_pass = 3
		en_key = random.choice(rand_char)
		
		cleanDrive(dev_path, block_total, block_size, en_key)
		cleanDrive(dev_path, block_total, block_size, hex(ord(en_key) ^ 0xFF))
		cleanDrive(dev_path, block_total, block_size, rand_data)
	elif scan_opt == 4:
		max_pass = 3
		en_key = random.choice(rand_char)
		
		cleanDrive(dev_path, block_total, block_size, "0")
		cleanDrive(dev_path, block_total, block_size, "1")
		cleanDrive(dev_path, block_total, block_size, en_key)
	elif scan_opt == 5:
		max_pass = 5
		
		for i in range(0, max_pass):
			cleanDrive(dev_path, block_total, block_size, rand_data)

def buildDrive(dev_path):
	drive_lttr = dev_path[4:]
	
	p = Popen(['format', drive_lttr, '/q'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
	p.communicate(bytes('', 'utf-8'))
