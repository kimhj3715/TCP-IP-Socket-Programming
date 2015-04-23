// inet_addr.c
#include <stdio.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]) {

	char *addr1 = "192.168.0.15";
	// char *addr1 = "localhost";   // Occurred error

	unsigned long conv_addr = inet_addr(addr1);
	if(conv_addr == INADDR_NONE) {
		printf("Error occurred! \n");
	} else {
		printf("Network ordered integer addr: %#1x \n", conv_addr);
	}


	return 0;
}