# thr_server.py

from threading import Thread, Lock
import threading, socket, sys

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
	snd_thread = Thread(target = send_msg, args = sock)
	rcv_thread = Thread(target = recv_msg, args = sock)

	snd_thread.start()
	rcv_thread.start()
		


	return 0

def send_msg(sock):
	while 1:
		send_data = raw_input("Input a message('Q' or 'q' to quit): ")
		if(send_data is 'q' or send_data is 'Q'):
			print >> sys.stderr, 'Request for disconnecting... closing socket... '
			sock.close()
			break
		print >> sys.stderr, '[%s] %s' % name, send_data
		sock.send(send_data)
	return 0

def recv_msg(sock):
	while 1:
		# Look for the response
		amount_received = 0
		amount_expected = len(send_data)

		while amount_received < amount_expected:
			recv_data = sock.recv(16)
			amount_received += len(recv_data)
			print >> sys.stderr, '[Recv] %s' % recv_data
	return 0

if __name__ == "__main__":
	if(len(sys.argv) != 4):
		print >> sys.stderr, "Usage : %s <IP> <port> <name> \n" % sys.argv[0]
	else:
		ip = sys.argv[1]
		port = sys.argv[2]
		name = sys.argv[3]
		main()