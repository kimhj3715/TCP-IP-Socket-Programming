# thr_server.py

from threading import Thread, Lock
import threading, socket, sys

BUF_SIZE = 100
NAME_SIZE = 20

ip = 0
port = 0
name = ""

def main():
	# initialize server address
	sock_addr = (ip, int(port))

	# creat a server socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print >> sys.stderr, 'Connecting to %s port %s' % sock_addr
	sock.connect(sock_addr)

	# create threads
	snd_thread = Thread(target = send_msg, args = (sock,))
	rcv_thread = Thread(target = recv_msg, args = (sock,))

	snd_thread.start()
	rcv_thread.start()
	
	print "Start"

	return 0

def send_msg(sock):
	while 1:
		send_data = raw_input("Input a message('Q' or 'q' to quit): ")
		if(send_data == 'q' or send_data == 'Q'):
			print >> sys.stderr, 'Request for disconnecting... closing socket... '
			sock.close()
			return None
		#print >> sys.stderr, '[%s] %s' % (name, send_data)
		send_data = '[' + name + '] ' + send_data
		sock.send(send_data)
	return None

def recv_msg(sock):
	while 1:
		# Look for the response
		amount_received = 0
		amount_expected = BUF_SIZE + NAME_SIZE

		while amount_received < amount_expected:
			recv_data = sock.recv(NAME_SIZE + BUF_SIZE -1)
			amount_received += len(recv_data)
			print >> sys.stderr, '\n%s' % recv_data
	return None

if __name__ == "__main__":
	if(len(sys.argv) != 4):
		print >> sys.stderr, "Usage : %s <IP> <port> <name> \n" % sys.argv[0]
	else:
		ip = sys.argv[1]
		port = sys.argv[2]
		name = sys.argv[3]
		main()