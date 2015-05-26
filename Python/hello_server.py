# hello_server.py
import socket
import sys

def main(port):
	message = "hello world"

	# create a server socket
	serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind the socket to the port
	serv_addr = ('localhost', int(port))
	print >> sys.stderr, 'starting up on %s port %s' % serv_addr
	
	try:
		serv_sock.bind(serv_addr)
		serv_sock.listen(5)
	except socket.error as msg:
		serv_sock.close()

	clnt_sock, clnt_addr = serv_sock.accept()
	print 'Connected by', clnt_addr

	clnt_sock.send(message)
	
	clnt_sock.close()
	serv_sock.close()

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, 'Usage : %s <port>' % sys.argv[0]
	else:
		main(sys.argv[1])