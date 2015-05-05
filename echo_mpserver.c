#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <signal.h>

#define BUF_SIZE 1024

void error_handling(char *message);
void read_childproc(int sig);


int main (int argc, char *argv[]) {
	// variables
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_addr, clnt_addr;

	pid_t pid;
	struct sigaction act;
	socklen_t adr_sz;
	int str_len, state;
	char buf[BUF_SIZE];


	// get server ip address and port information
	if(argc != 2) {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	// dealing with zombie processors
	act.sa_handler = read_childproc;
	sigemptyset(&act.sa_mask);
	act.sa_flags = 0;
	state = sigaction(SIGCHLD, &act, 0);

	// create a server socket
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
	if(serv_sock == -1) {
		error_handling("socket() error");
	}
	
	// initialize server address and port
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(atoi(argv[1]));

	// bind with the address
	if(bind(serv_sock, (struct sockaddr*) &serv_addr, sizeof(serv_addr)) == -1) {
		error_handling("bind() error");
	}

	// listen()
	if(listen(serv_sock, 5) == -1) {
		error_handling("listen() error");
	}
	
	// accept()
	while(1) {
		adr_sz = sizeof(clnt_addr);
		clnt_sock = accept(serv_sock, (struct sockaddr*) &clnt_addr, sizeof(clnt_addr));
		if(clnt_sock == -1) {
			continue;
		} else {
			puts("new client connected...");
		}
		pid = fork();
		if(pid == -1) {
			close(clnt_sock);
			continue;
		}
		if(pid == 0) { // if pid is child processor
			close(serv_sock);
			while((str_len = read(clnt_sock, buf, BUF_SIZE)) != 0) {
				write(clnt_sock, buf, str_len);  // echo back to client socket
			}
			close(clnt_sock);
			puts("client disconnected...");
			return 0;
		} else { // if pid is parent processor
			close(clnt_sock);
		}
	}

	close(serv_sock);
	return 0;
}

void read_childproc(int sig) {
	pid_t pid;
	int status;
	pid = waitpid(-1, &status, WNOHANG);
	printf("removed proc id: %d \n", pid);
}

void error_handling(char *message) {
	fputs(message, stderr);
	fputs('\n', stderr);
	exit(1);
}