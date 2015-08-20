# echo_select_server.py
import select
import socket
import sys
import Queue

BUF_SIZE = 1024

port = 0

def main():
	# create a server socket
	try:
		serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error as msg:
		print >> sys.stderr, '%s' % msg

	serv_addr = ('localhost', int(port))
	print >> sys.stderr, 'starting up on %s:%d' % serv_addr

	# bind & listen
	try:
		serv_sock.bind(serv_addr)
		serv_sock.setblocking(0)
		serv_sock.listen(5)
	except socket.error as msg:
		serv_sock.close()

	# select_handling
	clients = [serv_sock]
	max_clients = 0

	while (1):
		readList, writeList, exceptions = select.select(clients, [], [])
		for sockets in readList:
			if(sockets == serv_sock):
				# new connection coming
				conn, address = serv_sock.accept()
				clients.append(conn)
				max_clients+=1
			else:
				# get a data from the socket
				data = sockets.recv(BUF_SIZE)
				print >> sys.stderr, '%s: %s' % sockets.getpeername(), data
				if (not data):
					print >> sys.stderr, 'Disconnected by %s %s' % sockets.getpeername()
					sockets.close()
					break
				sockets.send(data)

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, 'Usage : %s <port> ' % sys.argv[0]
	else:
		port = sys.argv[1]
		print >> sys.stderr, 'Starts Server'
		main()