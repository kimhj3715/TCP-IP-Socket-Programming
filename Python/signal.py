# signal.py

from multiprocessing import Process
import os, sys, time, signal



def main():
	signal.signal(signal.SIGALRM, timeout)
	signal.signal(signal.SIGINT, keycontrol)
	signal.alarm(2)
	
	for i in range(0, 3):
		print "wait..."
		time.sleep(100)
	return 0

def timeout(sig, frame):
	print 'Signal handler called with signal', sig
	if(sig == signal.SIGALRM):
		print "Time out!"
	signal.alarm(2)

def keycontrol(sig, frame):
	if(sig == signal.SIGINT):
		print "CTRL + C pressed"

if __name__ == "__main__":
	main()