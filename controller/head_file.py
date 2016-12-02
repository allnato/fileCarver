import sys, binascii, re, os, math
# head_file.py

# fix scanning in the same block (after a successful search and find) for another file_type
# make this a stable version
# research fastest way to read a file in hex

import binascii, re, os, math
from init_drive import getDriveTotal
from timeit import default_timer as timer
from man_time import getPercentAndRemainProgress

test_met = False ###DEBUG ONLY

def fastReadImage(file_name, output_path, lst_srt, lst_end, lst_types, lst_buf, **item_opt):   # improve this by recovering recently deleted files
	file_ctr = 0
	block_size = 131072
	block_num = 0
	output_path = os.path.normcase(output_path)
	start_time = timer()

	try:
		file_hndle = open(file_name, 'rb')
	except (OSError, IOError) as e:
		print("Error: " + file_name + " cannot be read.", file=sys.stderr)               ################## DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)

	if re.match(r'/dev/s', file_name) or re.match(r'\\\\.\\',file_name):
		raw_total = getDriveTotal(file_name)
	else:
		raw_total = os.path.getsize(file_name)

	block_total = int(math.ceil(raw_total / block_size))
	unparsed = file_hndle.read(block_size)
	hex_data = binascii.hexlify(unparsed).decode('utf-8')

	srt_pos = 0
	end_pos = 0
	type_ctr = len(lst_types)
	lst_dump = []

	while block_num <= block_total:
		prog, rem_time = getPercentAndRemainProgress(block_num, block_total, start_time)     # @to_GUI
		yield "data:" + str(prog) + " " + str(file_ctr) + " " + str(rem_time) + "\n\n"
		for i in range(0, type_ctr):
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

					while hex_data and not match:
						if block_num == block_total:
							return
						block_num = block_num + 1
						file_hndle.seek((block_size) * block_num)
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

				end_pos = end_pos - (end_pos % 2)
				hex_data = hex_data[end_pos:]

				if not hex_data and block_num < block_total:
					block_num = block_num + 1
					file_hndle.seek((block_size) * block_num)
					unparsed = file_hndle.read(block_size)
					hex_data = binascii.hexlify(unparsed).decode('utf-8')

				#continue                                                 # check if this is even needed

			for item in lst_dump:
				if len(item.encode('utf-8')) % 2 != 0:
					item = item + '0'
				file_ctr = file_ctr + 1
				writeImage(item, output_path, lst_types[i], file_ctr)

			lst_dump = []

		block_num = block_num + 1
		file_hndle.seek((block_size) * block_num)
		unparsed = file_hndle.read(block_size)
		hex_data = binascii.hexlify(unparsed).decode('utf-8')

	file_hndle.close()

# if there is time, try to debug if there are repeating patterns since block_endmark here is not tracked which results to end_pos being repeated in the original block

def standardReadImage(file_name, output_path, lst_srt, lst_end, lst_types, lst_buf, **item_opt):
	file_ctr = 0
	block_size = 16384
	block_num = 0
	block_mark = 0
	output_path = os.path.normcase(output_path)
	start_time = timer()

	try:
		file_hndle = open(file_name, 'rb')
	except (OSError, IOError) as e:
		print("Error: " + file_name + " cannot be read.", file=sys.stderr)               ################## DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)

	if re.match(r'/dev/s', file_name) or re.match(r'\\\\.\\',file_name):
		raw_total = getDriveTotal(file_name)
	else:
		raw_total = os.path.getsize(file_name)

	block_total = int(math.ceil(raw_total / block_size))
	unparsed = file_hndle.read(block_size)
	hex_data = binascii.hexlify(unparsed).decode('utf-8')

	srt_pos = 0
	end_pos = 0
	type_ctr = len(lst_types)
	lst_dump = []

	while block_num <= block_total:
		for i in range(0, type_ctr):
			prog, rem_time = getPercentAndRemainProgress(block_num, block_total, start_time)     # @to_GUI
			yield "data:" + str(prog) + " " + str(file_ctr) + " " + str(rem_time) + "\n\n"
			
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

					while hex_data and not match:        # while hex_data or file_data? hex_data since you might want to append the data from srt_pos
						if block_num == block_total:     # true since you are checking on the final block and it failed to find the footer
							return
						block_num = block_num + 1
						file_hndle.seek((block_size) * block_num)
						unparsed = file_hndle.read(block_size)
						hex_data = binascii.hexlify(unparsed).decode('utf-8')

						match = lst_end[i].search(hex_data)
						if match:
							end_pos = match.end()
							file_data = file_data + hex_data[:end_pos]
							if file_data:
								lst_dump.append(file_data)
						elif len(file_data) > lst_buf[i]:
							hex_head = str(lst_end[i]).replace("re.compile('", "").replace("')", "")
							end_pos = srt_pos + len(hex_head)
							match = True
		
							file_data = file_data + hex_data + hex_head     # add replacing regex chars here soon
							if file_data:
								lst_dump.append(file_data)
						else:
							file_data = file_data + hex_data

					# in the future, add feature to exlude "exhausted" middle blocks since you already know that they are fully occupied
					block_num = block_mark
					file_hndle.seek((block_size) * block_num)
					unparsed = file_hndle.read(block_size)
					hex_data = binascii.hexlify(unparsed).decode('utf-8')
					
				end_pos = end_pos - (end_pos % 2)
				print(end_pos)
				hex_data = hex_data[end_pos:]
				
				for item in lst_dump:
					if len(item.encode('utf-8')) % 2 != 0:
						item = item + '0'
					file_ctr = file_ctr + 1
					writeImage(item, output_path, lst_types[i], file_ctr)

				lst_dump = []
				
				if not hex_data:
					break

		block_mark = block_mark + 1
		block_num = block_mark
		file_hndle.seek((block_size) * block_num)
		unparsed = file_hndle.read(block_size)
		hex_data = binascii.hexlify(unparsed).decode('utf-8')

	file_hndle.close()

def deepReadImage(file_name, output_path, lst_srt, lst_end, lst_types, lst_buf, **item_opt):
	file_ctr = 0
	block_size = 16384
	block_num = 0
	block_mark = 0
	block_endmark = 0
	output_path = os.path.normcase(output_path)
	start_time = timer()

	try:
		file_hndle = open(file_name, 'rb')
	except (OSError, IOError) as e:
		print("Error: " + file_name + " cannot be read.", file=sys.stderr)               ################## DISPLAY ERROR MESSAGE @to_GUI
		exit(-1)

	if re.match(r'/dev/s', file_name) or re.match(r'\\\\.\\',file_name):
		raw_total = getDriveTotal(file_name)
	else:
		raw_total = os.path.getsize(file_name)

	block_total = int(math.ceil(raw_total / block_size))
	unparsed = file_hndle.read(block_size)
	hex_data = binascii.hexlify(unparsed).decode('utf-8')

	srt_pos = 0
	end_pos = 0
	type_ctr = len(lst_types)
	lst_dump = []

	while block_num <= block_total:
		for i in range(0, type_ctr):
			limit_reached = False
			while True:
				prog, rem_time = getPercentAndRemainProgress(block_num, block_total, start_time)     # @to_GUI
				yield "data:" + str(prog) + " " + str(file_ctr) + " " + str(rem_time) + "\n\n"
				
				match = lst_srt[i].search(hex_data)
				if match:
					srt_pos = match.start()
					match = lst_end[i].search(hex_data[srt_pos:])

					if match:
						end_pos = match.end()
						file_data = hex_data[srt_pos:end_pos]
						block_endmark = end_pos
						if file_data:
							lst_dump.append(file_data)
					else:
						file_data = hex_data[srt_pos:]

						while hex_data and not match:
							if block_num == block_total:
								return
							block_num = block_num + 1
							file_hndle.seek((block_size) * block_num)
							unparsed = file_hndle.read(block_size)
							hex_data = binascii.hexlify(unparsed).decode('utf-8')

							match = lst_end[i].search(hex_data)
							if match:
								end_pos = match.end()
								file_data = file_data + hex_data[:end_pos]
								if file_data:
									lst_dump.append(file_data)
							elif len(file_data) > lst_buf[i] * 2:
								hex_head = str(lst_end[i]).replace("re.compile('", "").replace("')", "")
								end_pos = srt_pos + len(hex_head)
								match = True

								file_data = file_data + hex_data + hex_head     # add replacing regex chars here soon
								if file_data:
									lst_dump.append(file_data)
							else:
								file_data = file_data + hex_data

						block_num = block_mark
						end_pos = 0
						limit_reached = True
						file_hndle.seek((block_size) * block_num)
						unparsed = file_hndle.read(block_size)
						hex_data = binascii.hexlify(unparsed).decode('utf-8')
						
					end_pos = end_pos - (end_pos % 2)
					hex_data = hex_data[end_pos:]
					
					for item in lst_dump:
						if len(item.encode('utf-8')) % 2 != 0:
							item = item + '0'
						file_ctr = file_ctr + 1
						writeImage(item, output_path, lst_types[i], file_ctr)

					lst_dump = []
					
					if not hex_data or limit_reached:
						break
				else:
					break
		block_endmark = 0
		block_mark = block_mark + 1
		block_num = block_mark
		file_hndle.seek((block_size) * block_num)
		unparsed = file_hndle.read(block_size)
		hex_data = binascii.hexlify(unparsed).decode('utf-8')

	file_hndle.close()

def writeImage(item, output_path, file_type, file_ctr):
	item = item.encode('utf-8')
	file_name = output_path + str(file_ctr) + '].' + file_type

	item = binascii.unhexlify(item)
	with open(file_name, 'wb') as f_out:
		f_out.write(item)
