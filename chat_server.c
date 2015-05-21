#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>

#define BUF_SIZE 100
#define MAX_CLNT 256

// function definition
void error_handling(char* message);
void* handle_clnt(void* arg);
void send_msg(char* msg, int len);

// global variables
pthread_mutex_t mutex;
int clnt_cnt = 0;
int clnt_socks[MAX_CLNT];

int main(int argc, char* argv[]) {
	// variables
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_addr, clnt_addr;
	pthread_t t_id;
	int clnt_addr_sz;

	// input validation
	if(argc != 2) {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	// initialize the mutex
	pthread_mutex_init(&mutex, NULL);

	// create a socket
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
	
	while(1) {
		// accept
		clnt_addr_sz = sizeof(clnt_addr);
		clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_sz);

		pthread_mutex_lock(&mutex);
		clnt_socks[clnt_cnt++] = clnt_sock;
		pthread_mutex_unlock(&mutex);

		pthread_create(&t_id, NULL, handle_clnt, (void*)&clnt_sock);
		pthread_detach(t_id);
		printf("Connected client IP: %s\n", inet_ntoa(clnt_addr.sin_addr));
	}
	

	pthread_mutex_destroy(&mutex);

	return 0;
}

// read and send to all clnts
void* handle_clnt(void* arg) {
	int clnt_sock = *((int*)arg);
	int str_len = 0, i;
	char msg[BUF_SIZE];

	// if str_len returns 0, EOF (file reaches the end of the file)
	// if str_len returns not-0, (positive) successed bytes (negative) failed
	// In socket, EOF means socket is disconnected (ctrl+c)
	while((str_len = read(clnt_sock, msg, sizeof(msg))) != 0) {
		fputs(msg, stdout);
		send_msg(msg, str_len);
	}

	// remove disconnected clinets
	pthread_mutex_lock(&mutex);
	for(i=0; i<clnt_cnt; i++) {
		if(clnt_sock == clnt_socks[i]) {
			while(i++<clnt_cnt-1) {
				clnt_socks[i] = clnt_socks[i+1];
			}
			break;	
		}
	}
	clnt_cnt--;
	pthread_mutex_unlock(&mutex);
	close(clnt_sock);
	return NULL;
}

// send message to all
void send_msg(char* msg, int len) {
	int i;
	pthread_mutex_lock(&mutex);
	for(i=0; i<clnt_cnt; i++) {
		write(clnt_socks[i], msg, len);
	}
	pthread_mutex_unlock(&mutex);
}

void error_handling(char* message) {
	fputs(message, stderr);
	fputs("\n", stderr);
	exit(1);
}