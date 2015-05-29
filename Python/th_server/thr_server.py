# thr_server.py
from threading import Thread, Lock
import threading, socket, sys

MAX_CLNT = 256

clnt_socks = [MAX_CLNT]
mutex = Lock()
port = 0


def main():
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
		mutex.release()

		thread = Thread(target = handle_clnt, args = (clnt_sock, clnt_addr))
		thread.start()
		#thread.join()
		

	return 0



def handle_clnt(sock, sock_addr):
	clnt_sock = sock
	clnt_addr = sock_addr

	try:
		print >> sys.stderr, 'connection from', clnt_addr
		while 1:
			recv_data = clnt_sock.recv(16)
			print >> sys.stderr, '%s: %s' % (clnt_addr[0], recv_data)
			if recv_data:
				# print >> sys.stderr, 'sending recv_data back to the client'
				clnt_sock.sendall(recv_data)
			else:
				print >> sys.stderr, 'no more data from', clnt_addr
				print >> sys.stderr, 'thread finished... exiting'
				break
	finally:
		clnt_sock.close()

	return 0


if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, "Usage : %s <port>" % sys.argv[0]
	else:
		port = sys.argv[1]
		main()