# waitpid.py

from multiprocessing import Process
import os, time, sys


def main():
	pid = os.fork()

	if(pid == 0): 
		time.sleep(7)
		return 24		# return value 
	else:
		while 1:
			pid, status = os.waitpid(-1, 0)
			print "wait returned, pid = %d, status = %d" % (pid, status)
			if(pid == 0):	# child proc hasn't finished yet
				print "sleep for 3 seconds..."
				time.sleep(3)
			else:
				break

			if(os.WIFEXITED(status) != 0):
				print "Child send %d" % os.WEXITSTATUS(status)

if __name__ == "__main__":
	main()