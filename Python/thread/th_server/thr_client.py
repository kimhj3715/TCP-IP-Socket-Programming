# thr_server.py

import threading, socket, sys

ip = 0
port = 0


def main():
	# initialize server address
	sock_addr = (ip, int(port))

	# creat a server socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print >> sys.stderr, 'Connecting to %s port %s' % sock_addr
	sock.connect(sock_addr)

	while 1:
		send_data = raw_input("Input a message('Q' or 'q' to quit): ")
		print >> sys.stderr, '[Send] %s' % send_data
		sock.sendall(send_data)

		# Look for the response
		amount_received = 0
		amount_expected = len(send_data)

		while amount_received < amount_expected:
			recv_data = sock.recv(16)
			amount_received += len(recv_data)
			print >> sys.stderr, '[Recv] %s' % recv_data


		if(send_data is 'q' or send_data is 'Q'):
			print >> sys.stderr, 'Request for disconnecting... closing socket... '
			sock.close()
			break
	return 0

if __name__ == "__main__":
	if(len(sys.argv) != 3):
		print >> sys.stderr, "Usage : %s <IP> <port>" % sys.argv[0]
	else:
		ip = sys.argv[1]
		port = sys.argv[2]
		main()