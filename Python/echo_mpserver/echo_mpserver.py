# echo_mpserver.py
from multiprocessing import Process
import os, sys, time, socket, signal

# GLOBAL VARIABLES
BUF_SIZE = 1024

port = 0


def read_childproc(sig, frame):
	pid = os.waitpid(-1, 0)
	print "removed proc id: %d", pid

def main():
	# signal setting
	signal.signal(signal.SIGCHLD, read_childproc)

	# create a server socket
	serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# initialize server address
	serv_addr = ('localhost', int(port))

	# bind & listen
	try:
		serv_sock.bind(serv_addr)
		serv_sock.listen(5)
	except socket.error as msg:
		serv_sock.close()

	# accept
	while 1:
		clnt_sock, clnt_addr = serv_sock.accept()
		print 'Clinet socket value:', clnt_sock
		print 'Connected by', clnt_addr

		pid = os.fork()

		if(pid == 0):
			serv_sock.close()
			while 1:
				data = clnt_sock.recv(BUF_SIZE)
				print clnt_addr, ": ", data
				if (not data):
					print "Client disconnected...", clnt_addr
					break
				clnt_sock.send(data)
			
		else:
			clnt_sock.close()

	clnt_sock.close()
	serv_sock.close()
	return 0
			

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, "Usage : %s <port> " % sys.argv[0]
	else:
		port = sys.argv[1]
		main()