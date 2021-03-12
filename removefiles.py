import os
import time
from multiprocessing import Pool, freeze_support

def condition(file):
	# return file.endswith(".pdf") and not file.endswith("compressed.pdf")


def get_list():
	for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
		for file in files:
			if condition(file):
				yield os.path.join(root, file)


def do_clean(file):
	if condition(file):
		os.remove(file)
		print(file)


def without_multipro():
	for file in get_list():
		do_clean(file)


if __name__ == '__main__':
	# freeze_support()
	start = time.time()
	# print([i for i in get_list()])
	# with Pool(10) as p:
	# 	p.map(do_clean, get_list())

	without_multipro() #Time: 0.05684661865234375s
	# map(do_clean, [i for i in get_list()])
	print(f"Finished at: {time.time() - start}s")