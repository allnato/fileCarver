# model_app.py

import re, os

def getScanChoice(scan_num, **item_opt):
	scan_num = str(scan_num)
	scan_types = { "1": "fast", "2": "standard", "3": "deep" }
	
	return scan_types[scan_num]
	
def compileRegs(lst_ext, **item_opt):
	lst_srt = []
	lst_end = []
	lst_buf = []
	file_name = os.path.join("..", "model", "mod_signatures.txt")
	
	try:
		with open(file_name, 'r') as sig_in:
			lst_sig = sig_in.readlines()
			
		lst_sig = _quicksort(lst_sig, 0, len(lst_sig)-1)
		
		if len(lst_ext) == len(lst_sig):
			for inst in lst_sig:
				lst_cont = inst.strip().lower().split(',')
				lst_srt.append(re.compile(lst_cont[1].replace(" ", "")))
				lst_end.append(re.compile(lst_cont[2].replace(" ", "")))
				lst_buf.append(int(lst_cont[4]) * 2097152)
		else:
			for inst in lst_ext:
				if not lst_sig:
					#print("Error: file type " + inst + " is not found")  ################## DISPLAY ERROR MESSAGE @to_GUI
					exit(-1)
				while lst_sig:
					if re.match(inst + ',', lst_sig[0].lower()):
						lst_cont = lst_sig[0].strip().lower().split(',')
						lst_srt.append(re.compile(lst_cont[1].replace(" ", "")))
						lst_end.append(re.compile(lst_cont[2].replace(" ", "")))
						lst_buf.append(int(lst_cont[4]) * 2097152)
						lst_sig.pop(0)
						break
					else:
						lst_sig.pop(0)

	except (OSError, IOError) as e:
		#print("Error: " + file_name + " cannot be read.")                ################## DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)
	
	return(lst_srt, lst_end, lst_buf)

def namingFile(extract_path, prefix, **item_opt):
	full_prefix = os.path.join(extract_path, prefix) + "["
	return full_prefix

def _quicksort(myList, start, end):
    if start < end:
        pivot = _partition(myList, start, end)
        _quicksort(myList, start, pivot-1)
        _quicksort(myList, pivot+1, end)
    return myList
	
def _partition(myList, start, end):
    pivot = myList[start]
    left = start+1
    right = end
    done = False
    
    while not done:
        while left <= right and myList[left] <= pivot:
            left = left + 1
        while myList[right] >= pivot and right >=left:
            right = right -1
        if right < left:
            done= True
        else:
            temp=myList[left]
            myList[left]=myList[right]
            myList[right]=temp
            
    temp=myList[start]
    myList[start]=myList[right]
    myList[right]=temp
    return right
