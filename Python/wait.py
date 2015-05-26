# wait.py
from multiprocessing import Process
import os
import time



def main():
	pid = os.fork()

	if(pid == 0):	# child proc
		exit(2)
	else:
		print "Child PID: %d " % pid
		pid = os.fork()
		if(pid == 0):
			exit(7)
		else:
			print "Child PID: %d " % pid
			pid, status = os.wait()
			if(os.WIFEXITED(status)):
				print "Child send one: %d" % os.WEXITSTATUS(status)
			pid, status = os.wait()
			if(os.WIFEXITED(status)):
				print "Child send two: %d" % os.WEXITSTATUS(status)
			time.sleep(10)

if __name__ == "__main__":
	main()