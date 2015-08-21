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
		serv_sock.setblocking(0)
		serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	except socket.error as msg:
		print >> sys.stderr, '%s' % msg

	# bind the socket to the port	
	try:
		serv_addr = ('localhost', int(port))
		print >> sys.stderr, 'starting up on %s:%d' % serv_addr
		serv_sock.bind(serv_addr)
		serv_sock.listen(5)
	except socket.error as msg:
		serv_sock.close()

	# select_handling
	clients = [serv_sock]
	outputs = [ ]
	max_clients = 0
	message_queues = {}		# outgoing message queues (socket:Queue)

	while (1):
		# Wait for at least one of the sockets to be ready for processing
		#print >> sys.stderr, '\nwaiting for the next event'
		readList, writeList, exceptions = select.select(clients, outputs, [])
		for sockets in readList:
			if(sockets == serv_sock):
				# new connection coming
				conn, address = serv_sock.accept()
				conn.setblocking(0)
				clients.append(conn)
				print >> sys.stderr, '[%s: %s] connection established' % conn.getpeername()
				message_queues[conn] = Queue.Queue()
				max_clients+=1
				print >> sys.stderr, 'The number of client is %d' % max_clients
			else:
				# get a data from the socket
				data = sockets.recv(BUF_SIZE)
				if data:
					# a readable client socket has data
					print >> sys.stderr, '[%s: %s]' % sockets.getpeername(), data
					sockets.send(data)
					message_queues[sockets].put(data)
					# add output channel for response
					if sockets not in outputs:
						outputs.append(sockets)
				else:
					# Interpret empty result as closed connection
					print >> sys.stderr, '[%s: %s] disconnected' % sockets.getpeername()
					# stop listening for input on the connection
					if sockets in outputs:
						outputs.remove(sockets)
					clients.remove(sockets)
					max_clients-=1
					print >> sys.stderr, 'The number of client is %d' % max_clients
					sockets.close()
					# remove message queue
					del message_queues[sockets]
				

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print >> sys.stderr, 'Usage : %s <port> ' % sys.argv[0]
	else:
		port = sys.argv[1]
		main()