#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
//#include <string.h>

void error_handling(char *message);


int main(int argc, char *argv[]) {
	int sock;
	struct sockaddr_in serv_adr;


	// get input IP and port from a user
	if(argc != 3) {
		printf("Usage: %s <IP> <port>\n", argv[0]);
		exit(1);
	}

	// create socket
	sock = socket(PF_INET, SOCK_STREAM, 0);
	if(sock == -1) {
		error_handling("socket() error");
	}
	// initialize IP address and port
	memset(&serv_adr, 0, sizeof(serv_adr));
	serv_adr.sin_family = AF_INET;
	serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
	serv_adr.sin_port = htons(atoi(argv[2]));



	// connect to the server 


	return 0;
}

void error_handling(char *message) {
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}