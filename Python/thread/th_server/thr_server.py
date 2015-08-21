# thr_server.py

# Author: Ben Kim

# Date: Aug 21 2015

# Description: 
# 	Multithreaded server. 

# Improvement:
# 	1. When a client disconnected, the server does not reduce the number of socket client.
# 	meaning, the client socket is not closing correctly.

#	2. How to set the limitation of client sockets (using MAX_CLNT)

# Compile:
#	python thr_server.py 8888

from threading import Thread, Lock
import threading, socket, sys

BUF_SIZE = 100
NAME_SIZE = 20
MAX_CLNT = 256

clnt_num = 0
#clnt_socks = [None] * MAX_CLNT
#!!! = how to set the limitation of sockets
clnt_socks = []
mutex = Lock()
port = 0


def main():
	global clnt_num
	# initialize server address
	serv_addr = ("localhost", int(port))

	# creat a server socket
	serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# bind & listen
	try:
		serv_sock.bind(serv_addr)
		serv_sock.listen(5)
	except socket.error as msg:
		serv_sock.close()

	# accept
	while 1:
		clnt_sock, clnt_addr = serv_sock.accept()
		
		mutex.acquire()
		print "mutext acquired() -- 1 \n"
		clnt_socks.append(clnt_sock)
		clnt_num = clnt_num + 1
		print "Total number of socket client: %d" % clnt_num
		mutex.release()
		print "mutext released() -- 1 \n"

		thread = Thread(target = handle_clnt, args = (clnt_sock, clnt_addr))
		thread.start()
		
	serv_sock.close()

	return 0



def handle_clnt(sock, sock_addr):
	global clnt_num
	clnt_sock = sock
	clnt_addr = sock_addr

	try:
		print >> sys.stderr, 'connection from', clnt_addr
		while 1:
			recv_data = clnt_sock.recv(BUF_SIZE)
			print >> sys.stderr, '%s: %s' % (clnt_addr[0], recv_data)
			if (not recv_data):
				print >> sys.stderr, 'no more data from', clnt_addr
				print >> sys.stderr, 'thread finished... exiting'
				break
			send_msg(recv_data)
				
		# remove disconnected client
		mutex.acquire()
		print "mutext acquired() -- 2 \n"
		for i in range(0, clnt_num):
			if(clnt_sock==clnt_socks[i]):
				while(i< clnt_num-1):
					clnt_socks[i] = clnt_socks[i+1]
					i=i+1
				break
		mutex.release()
		print "mutext released() -- 2 \n"

		clnt_sock.close()
	finally:
		print "final"
	return None

def send_msg(recv_data):
	global clnt_num
	mutex.acquire()
	print "mutext acquired() -- 3 \n"
	for i in range(0, clnt_num):
		clnt_socks[i].send(recv_data)
	mutex.release()
	print "mutext released() -- 3 \n"


if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, "Usage : %s <port>" % sys.argv[0]
	else:
		port = sys.argv[1]
		main()














