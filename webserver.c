#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <pthread.h>

#define BUF_SIZE 1024
#define SMALL_BUF 100

// function definition
void* error_handling(char* message);
void* request_handler(void* arg);

int main(int argc, char *argv[]) {
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_addr, clnt_addr;
	int clnt_addr_sz;
	char buf[BUF_SIZE];
	pthread_t t_id;
	
	if(argc != 2) {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	// create a socket
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);

	// initialize server address
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(atoi(argv[1]));

	// bind
	if(bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1) {
		error_handling("bind() error!");
	}
	// listen
	if(listen(serv_sock, 20) == -1) {
		error_handling("listen() error!");
	}

	while(1) {
		clnt_addr_sz = sizeof(clnt_addr);
		clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_sz);
		printf("Connection Request : %s:%d\n", inet_ntoa(clnt_addr.sin_addr), ntohs(clnt_addr.sin_port));
		pthread_create(&t_id, NULL, request_handler, &clnt_sock);
		pthread_detach(t_id);
	}	

	return 0;
}

void* request_handler(void* arg) {
	int clnt_sock = *((int*)arg);
	char req_line[SMALL_BUF];
	FILE* clnt_read;
	FILE* clnt_write;

	char method[10];
	char file_name[30];
	char ct[15];

	clnt_read = fdopen(clnt_sock, "r");
	clnt_write = fdopen(dup(clnt_sock), "w");
	fgets(req_line, SMALL_BUF, clnt_read);
	if(strstr(req_line, "HTTP/") == NULL) {
		send_error(clnt_write);
		fclose(clnt_read);
		fclose(clnt_write);
		return;
	}

	strcpy(method, strtok(req_line, " /"));
	strcpy(file_name, strtok(NULL, ));


}

void send_error(FILE* fp) {
	char protocol[] = "HTTP/1.0 400 Bad Request\r\n";
	char server[] = "Server:Linux Web Server \r\n";
	char clnt_len[] = "Content-length: 2048 \r\n";
	char clnt_type[] = "Content-type:text/html \r\n\r\n";
	char content[] = "<html><head><title>NETWORK</title></head>"
						"<body><font size=+5><br> Error Occurred!!! File name or request type error!!!"
						"</font></body></html>";
	fputs(protocol, fp);
	fputs(server, fp);
	fputs(clnt_len, fp);
	fputs(clnt_type, fp);
	fflush(fp);
}

void* error_handling(char* message) {
	fputs(message, stderr);
	fputs("\n", stderr);
	exit(1);
}