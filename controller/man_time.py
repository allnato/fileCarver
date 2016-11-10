#man_time.py

from timeit import default_timer as timer
import math

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def _displayTime(seconds, granularity=2):
    result = []
    seconds = int(math.ceil(seconds))

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def getPercentAndRemainProgress(written_size, total_size, start_time):
	if not written_size:
		written_size = 1
	if not total_size:
		total_size = 1
	
	cur_size = written_size * 1.0 / total_size * 100
	
	elapsed_time = timer() - start_time
	rem_time = (elapsed_time / written_size) * (total_size - written_size)
	rem_time = _displayTime(rem_time, 3)
	
	return("%.2f" % cur_size, rem_time)
