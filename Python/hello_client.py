import socket
import sys


def main(ip, port):

	addr = (ip, int(port))

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as msg:
		sock = None

	try:
		sock.connect(addr)
	except socket.error as msg:
		sock.close()
		sock = None

	if sock is None:
		print 'could not open socket'
		sys.exit(1)

	data = sock.recv(1024)
	print 'Received', repr(data) 	# prints--> Received 'hello world'

	sock.close()
if __name__ == "__main__":
	if(len(sys.argv) != 3):
		print >> sys.stderr, 'Usage : %s <ip> <port>' % sys.argv[0]
	else:
		main(sys.argv[1], sys.argv[2])