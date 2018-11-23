#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define RANDOM 8
#define PERIOD 1

void hello_world(int i) {
	printf("Random %d: Hello World!\n", i);
}

int main(int argc, char **argv) {
	int i;

	while (1) {
		i = rand() % RANDOM;
		hello_world(i);
		sleep(PERIOD);
	}

	return 0;
}