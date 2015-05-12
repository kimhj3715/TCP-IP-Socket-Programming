#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

// function def
void* read(void* arg);
void* summ(void* arg);

// global variables
static sem_t sem_one;
static sem_t sem_two;
static int num;

int main(int argc, char* argv[]) {
	// variables
	pthread_t id_t1, id_t2;
	
	// initialize semaphore variables
	sem_init(&sem_one, 0, 0);
	sem_init(&sem_two, 0, 1);

	pthread_create(&id_t1, NULL, read, NULL);
	pthread_create(&id_t2, NULL, summ, NULL);

	pthread_join(id_t1, NULL);
	pthread_join(id_t2, NULL);

	// destory semaphore variables
	sem_destroy(&sem_one);
	sem_destroy(&sem_two);
	
	return 0;
}

void* read(void* arg) {
	int i;
	for(i=0; i<5; i++) {
		fputs("Input num: ", stdout);
		sem_wait(&sem_two);
		scanf("%d", &num);
		sem_post(&sem_one);
	}
	return NULL;
}

void* summ(void* arg) {
	int sum=0, i;
	for(i=0; i<5; i++) {
		sem_wait(&sem_one);
		sum+=num;
		sem_post(&sem_two);
	}
	printf("Result: %d\n", sum);
	return NULL;
}