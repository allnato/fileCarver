#file_headers2.py

# rename all of the files to [num] in controller.py
# fix scanning in the same block (after a successful search and find) for another file_type
# make this a stable version!! and create file_headers3

import binascii, time, re, os, math, hashlib

IMG_CTR = 0

# def cleanFiles()

def compileRegs(**item_opt):
	lst_types = []
	lst_srt = []
	lst_end = []
	lst_cat = []
	lst_buf = []
	file_name = 'model/mod_signatures.txt'
	
	try:
		with open(file_name, 'r') as sig_in:
			lst_sig = sig_in.readlines()
			
		for inst in lst_sig:
			lst_cont = inst.strip().lower().split(',')
			lst_types.append(lst_cont[0])
			lst_srt.append(re.compile(lst_cont[1].replace(" ", "")))
			lst_end.append(re.compile(lst_cont[2].replace(" ", "")))
			lst_cat.append(lst_cont[3].upper())
			lst_buf.append(int(lst_cont[4]) * 1048576)                        # multiply by 1 MB

	except (OSError, IOError) as e:
		print("Error: " + file_name + " cannot be read.")
		exit(-1)
	
	return(lst_srt, lst_end, lst_types, lst_buf)

def readImage(file_name, lst_srt, lst_end, lst_types, lst_buf, **item_opt):
	global IMG_CTR
	block_size = 131072 #16 # 4096 # 16384 #0.25 GB #131072 # 4096 is really optimal and is for complete scan # 131072 for fast scan
	block_num = 0
	
	try:
		file_hndle = open(file_name, 'rb')
	except (OSError, IOError) as e:
		print("Error: " + file_name + " cannot be read.")
		exit(-1)
	
	block_total = int(math.ceil(os.path.getsize(file_name) / block_size))
	unparsed = file_hndle.read(block_size)
	hex_data = binascii.hexlify(unparsed).decode('utf-8')

	srt_pos = 0
	end_pos = 0
	type_ctr = len(lst_types)
	lst_dump = []

	while block_num <= block_total:
		print("Examining Block: ", block_num, " out of ", block_total)
		
		for i in range(0, type_ctr):
			#print("Scanning: " + lst_types[i].upper())
			match = lst_srt[i].search(hex_data)
			if match:
				srt_pos = match.start()
				match = lst_end[i].search(hex_data[srt_pos:])
				
				if match:
					end_pos = match.end()
					file_data = hex_data[srt_pos:end_pos]
					if file_data:
						lst_dump.append(file_data)
				else:
					file_data = hex_data[srt_pos:]
					
					while hex_data and not match:                                     # go to the next block
						if block_num == block_total:
							return
						block_num = block_num + 1
						file_hndle.seek((block_size) * block_num)        # (block size) is valid!
						unparsed = file_hndle.read(block_size)
						hex_data = binascii.hexlify(unparsed).decode('utf-8')
						
						match = lst_end[i].search(hex_data)
						if match:
							end_pos = match.end()
							file_data = file_data + hex_data[:end_pos]
							if file_data:
								lst_dump.append(file_data)
						elif len(file_data) > lst_buf[i]:
							end_pos = 0
							match = True
							
							file_data = file_data + hex_data + str(lst_end[i]).replace("re.compile('", "").replace("')", "")      # add replacing regex chars here soon
							lst_dump.append(file_data)
						else:
							file_data = file_data + hex_data
				
				end_pos = end_pos - (end_pos % 2)                        # subtract for safety
				hex_data = hex_data[end_pos:]
						
				if not hex_data and block_num < block_total:
					block_num = block_num + 1
					file_hndle.seek((block_size) * block_num)                # (block size) is valid!
					unparsed = file_hndle.read(block_size)
					hex_data = binascii.hexlify(unparsed).decode('utf-8')
				
				#continue                                                 # check if this is even needed
				
			IMG_CTR = IMG_CTR + len(lst_dump)
			
			for item in lst_dump:
				if len(item.encode('utf-8')) % 2 != 0:
					item = item + '0'
				writeImage(item, lst_types[i])
		
			lst_dump = []
		
		block_num = block_num + 1
		file_hndle.seek((block_size) * block_num)                        # (block size) is valid!
		unparsed = file_hndle.read(block_size)
		hex_data = binascii.hexlify(unparsed).decode('utf-8')
	
	print("[+] Recovered ", IMG_CTR, " files.")
	print("Program completed successfully.")
	file_hndle.close()
	
def writeImage(item, file_type):
	
	item = item.encode('utf-8')
	file_name = 'output/' + hashlib.sha512(item).hexdigest() + '.' + file_type
		
	item = binascii.unhexlify(item)
	with open(file_name, 'wb') as f_out:
		f_out.write(item)
