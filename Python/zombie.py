from multiprocessing import process
import os
import time


def main():
	pid = os.fork()

	if(pid == 0):
		print "CHILD"
	else:
		print "Child process ID: %d" % pid
		time.sleep(30)

	if(pid == 0):
		print "End child process"
	else:
		print "End parent process"

if __name__ == "__main__":
	main()