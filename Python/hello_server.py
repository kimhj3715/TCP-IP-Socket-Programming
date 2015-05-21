# hello_server.py
import socket
import sys


# create a server socket
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
serv_addr = ('localhost', 8005)
print >> sys.stderr, 'starting up on %s port %s' % serv_addr
serv_sock.bind(serv_addr)

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, 'Usage : %s <port>' % sys.argv[0]
	else:
		main(sys.argv[1])