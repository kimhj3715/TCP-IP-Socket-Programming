from multiprocessing import Process
import os

gval = 10


def main():
	global gval		# needed to modify global copy of gval
	lval = 20

	pid = os.fork()
	if(pid == 0):	# child
		print "child"
		gval+=2
		lval+=2
	else:
		print "parent"
		gval-=2
		lval-=2

	if(pid == 0):
		print "Child Proc: [%d, %d]" % (gval, lval)
	else:
		print "Parent Proc: [%d, %d]" % (gval, lval)

if __name__ == "__main__":
	main()