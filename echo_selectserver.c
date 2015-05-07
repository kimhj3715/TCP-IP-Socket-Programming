#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/select.h>

#define BUF_SIZE 100

void error_handling(char *message);

int main(int argc, char *argv[]) {
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_addr, clnt_addr;
	struct timeval timeout;
	fd_set reads, copy_reads;
	socklen_t addr_sz;
	int fd_max, str_len, fd_num, i;
	char buf[BUF_SIZE];

	if(argc != 2) {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	// create a server socket
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);

	// initialize server address
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(atoi(argv[1]));

	// bind
	if(bind(serv_sock, (struct sockaddr*) &serv_addr, sizeof(serv_addr)) == -1) {
		error_handling("bind() error!");
	}

	// listen
	if(listen(serv_sock, 5) == -1) {
		error_handling("listen() error!");
	}

	// configure fd
	FD_ZERO(&reads);
	FD_SET(serv_sock, &reads);
	fd_max = serv_sock;		// serv_sock == 3 (don't know why);

	
	while(1) {
		copy_reads = reads;
		timeout.tv_sec = 5;
		timeout.tv_usec = 5000;

		if((fd_num = select(fd_max+1, &copy_reads, 0, 0, &timeout)) < 0) {
			break;
		} else if(fd_num == 0) {	// no event detected
			continue;
		}

		for(i=0; i<fd_max+1; i++) {
			if(FD_ISSET(i, &copy_reads)) {
				if(i == serv_sock) {	// connection requested
					//accept
					addr_sz = sizeof(clnt_addr);
					clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &addr_sz);
					FD_SET(clnt_sock, &reads);
					//fd_max += 1;
					if(fd_max < clnt_sock) {
						fd_max = clnt_sock;
					}
					printf("connected client: %d\n", clnt_sock);
				} else {	// deal with the existing clients
					// read messages
					str_len = read(i, buf, BUF_SIZE);
					if(str_len == 0) {	// close request!!
						FD_CLR(i, &reads);
						close(i);
						printf("closed client: %d \n", i);
					} else {
						write(i, buf, BUF_SIZE);	// echo !
					}
				}
			}
		}
	}
	close(serv_sock);
	return 0;
}

void error_handling(char *message) {
	fputs(message, stderr);
	fputs('\n', stderr);
	exit(1);
}