#mutex.py
from threading import Thread, Lock
import threading, socket, sys

sema1 = threading.BoundedSemaphore(value=1)
sema2 = threading.BoundedSemaphore(value=1)
num = 0

def main():
	num = 0
	sema1.acquire()

	thr1 = threading.Thread(target = read)
	thr2 = threading.Thread(target = accu)

	thr1.start()
	thr2.start()


	return 0


def read():
	global num
	for i in range(1, 5):
		sema2.acquire() # decrements the counter
		print "read() - sema2 acquire()\n"
		num = int(raw_input("Input a number: "))
		print "read() - sema1 release()\n"
		sema1.release() # increments the counter

	return 0

def accu():
	global num
	sum = 0
	for i in range(1, 5):
		sema1.acquire()
		print "accu() - sema1 acquire()\n"
		sum += num
		print >> sys.stderr, 'The value of sum: %d' % sum
		print "accu() - sema2 release()\n"
		sema2.release()

	print >> sys.stderr, 'Result: %d' % sum

	return 0


if __name__ == "__main__":
	main()