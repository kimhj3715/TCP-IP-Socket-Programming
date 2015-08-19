#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <pthread.h>

#define SMALL_BUF 100
#define BUF_SIZE 1024

void* request_handler(void* arg);
char* content_type(char* file);
void send_error(FILE* fp);
void send_data(FILE* fp, char* ct, char* file_name);
void error_handling(char* message);


int main(int argc, char *argv[]) {
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_addr, clnt_addr;
	int clnt_addr_size;
	pthread_t t_id;

	// input validation
	if(argc != 2) {
		printf("Usage %s [port]\n", argv[0]);
		exit(1);
	}
	// create a socket
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
	// initialize the server address
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(atoi(argv[1]));

	// bind
	if(bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr))==-1) {
		error_handling("bind() error");
	}
	// listen
	if(listen(serv_sock, 20)==-1) {
		error_handling("listen() error");
	}
	// accept
	while(1){
		clnt_addr_size = sizeof(clnt_addr);
		clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, (socklen_t *)&clnt_addr_size);
		printf("Connection Request : %s:%d\n", 
			inet_ntoa(clnt_addr.sin_addr), ntohs(clnt_addr.sin_port));
		pthread_create(&t_id, NULL, request_handler, &clnt_sock);
		pthread_detach(t_id);
	}
	close(serv_sock);
	return 0;
}

void* request_handler(void* arg) {
	// variables
	int clnt_sock = *((int*)arg);
	char req_line[SMALL_BUF];
	FILE* clnt_read;
	FILE* clnt_write;

	char method[10];
	char ct[15];
	char file_name[30];

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
	strcpy(file_name, strtok(NULL, " /"));
	strcpy(ct, content_type(file_name));
	if(strcmp(method, "GET")!=0) {		// SHOULD BE GET ??
		send_error(clnt_write);
		fclose(clnt_read);
		fclose(clnt_write);
		return;
	}
	fclose(clnt_read);
	send_data(clnt_write, ct, file_name);
}

void send_data(FILE* fp, char* ct, char* file_name) {
	char protocol[] = "HTTP/1.0 200 OK\r\n";
	char server[] = "Server: Linux Web Server honghong \r\n";
	char clnt_len[] = "Content-length:2048\r\n";
	char clnt_type[SMALL_BUF];
	char buf[BUF_SIZE];
	FILE* send_file;


	printf("PASSED FILE NAME:::::: %s\n", file_name);
	sprintf(clnt_type, "Content-type:%s\r\n\r\n", ct);
	send_file = fopen(file_name, "r");
	if(send_file == NULL) {
		send_error(fp);
		return;
	}

	fputs(protocol, fp);
	fputs(server, fp);
	fputs(clnt_len, fp);
	fputs(clnt_type, fp);

	while(fgets(buf, BUF_SIZE, send_file) != NULL) {
		fputs(buf, fp);
		fflush(fp);
	}
	fflush(fp);
	fclose(fp);
}

char* content_type(char* file){
	char extension[SMALL_BUF];
	char file_name[SMALL_BUF];
	strcpy(file_name, file);
	strtok(file_name, ".");
	strcpy(extension, strtok(NULL, "."));
	if(!strcmp(extension, "html") || !strcmp(extension, "htm")) {
		return "text/html";
	} else {
		return "text/plain";
	}
}


void send_error(FILE* fp) {
	char protocol[] = "HTTP/1.0 400 Bad Request\r\n";
	char server[] = "Server:Linux Web Server \r\n";
	char clnt_len[] = "Content-length:2048\r\n";
	char clnt_type[] = "Content-type:text/html\r\n\r\n";
	char content[] = "<html><head><title>NETWORK</title></head>"
						"<body><font size=+5><br> Error Occurred!!! File name or request type error!!!"
						"</font></body></html>";
	fputs(protocol, fp);
	fputs(server, fp);
	fputs(clnt_len, fp);
	fputs(clnt_type, fp);
	fputs(content, fp);
	fflush(fp);
}



void error_handling(char* message) {
	fputs(message, stderr);
	fputs("\n", stderr);
	exit(1);
}