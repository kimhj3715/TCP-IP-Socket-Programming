# thr_server.py
from threading import Thread, Lock
import threading, socket, sys

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
		clnt_socks.append(clnt_sock)
		clnt_num = clnt_num + 1
		mutex.release()

		thread = Thread(target = handle_clnt, args = (clnt_sock, clnt_addr))
		thread.start()
		#thread.join()
		

	return 0



def handle_clnt(sock, sock_addr):
	global clnt_num
	clnt_sock = sock
	clnt_addr = sock_addr

	try:
		print >> sys.stderr, 'connection from', clnt_addr
		while 1:
			recv_data = clnt_sock.recv(16)
			print >> sys.stderr, '%s: %s' % (clnt_addr[0], recv_data)
			if recv_data:
				send_msg(recv_data)
				# print >> sys.stderr, 'sending recv_data back to the client'
				#clnt_sock.sendall(recv_data)
			else:
				print >> sys.stderr, 'no more data from', clnt_addr
				print >> sys.stderr, 'thread finished... exiting'
				break
		# remove disconnected client
		mutex.acquire()
		for i in len(clnt_socks):
			if(clnt_sock==clnt_socks[i]):
				while(i< clnt_num-1):
					clnt_socks[i] = clnt_socks[i+1]
					i=i+1
				break
		mutex.release()

	finally:
		clnt_sock.close()

	return 0

def send_msg(recv_data):
	global clnt_num
	mutex.acquire()
	for i in range(0, clnt_num):
		print >> sys.stderr, 'Number of i: %d' % i
		print clnt_socks[i]
		clnt_socks[i].send(recv_data)
	mutex.release()
	return 0

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, "Usage : %s <port>" % sys.argv[0]
	else:
		port = sys.argv[1]
		main()














