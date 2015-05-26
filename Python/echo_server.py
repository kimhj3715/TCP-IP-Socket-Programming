# echo_server.py
import socket
import sys

BUF_SIZE = 1024

port = 0

def main():
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
	clnt_sock, clnt_addr = serv_sock.accept()
	print 'Connected by', clnt_addr

	while (1):
		data = clnt_sock.recv(BUF_SIZE)
		print clnt_addr, ": ", data
		if (not data):
			print "Disconnected", clnt_addr
			break
		clnt_sock.send(data)

	clnt_sock.close()
	serv_sock.close()
	

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, 'Usage : %s <port> ' % sys.argv[0]
	else:
		port = sys.argv[1]
		main()