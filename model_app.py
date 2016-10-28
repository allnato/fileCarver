# model_app.py

def getScanChoice(scan_num, **item_opt):
	scan_num = str(scan_num)
	scan_types = { "1": "fast", "2": "standard", "3": "deep" }
	
	return scan_types[scan_num]
	
def compileRegs(lst_ext, **item_opt):
	lst_types = []
	lst_srt = []
	lst_end = []
	lst_cat = []
	lst_buf = []
	file_name = 'model/mod_signatures.txt'
	
	# sort lst_ext
	
	try:
		with open(file_name, 'r') as sig_in:
			lst_sig = sig_in.readlines()
			
		for inst in lst_sig:
			lst_cont = inst.strip().lower().split(',')
			for ext in lst_ext:                                                  # do binary search here
				if ext == lst_cont[0]:
					lst_srt.append(re.compile(lst_cont[1].replace(" ", "")))
					lst_end.append(re.compile(lst_cont[2].replace(" ", "")))
					#lst_cat.append(lst_cont[3].upper())
					lst_buf.append(int(lst_cont[4]) * 2097152)                   # multiply by 2 MB

	except (OSError, IOError) as e:
		#print("Error: " + file_name + " cannot be read.")                ################## DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)
	
	return(lst_srt, lst_end, lst_buf)

def namingFile(extract_path, prefix, **item_opt):
	full_prefix = extract_path + prefix + "["
	return full_prefix
