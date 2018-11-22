#include <stdio.h>
#include <unistd.h>
#include <sys/sdt.h>

#define TIMES 10000
#define PERIOD 1

void hello_world(int i) {
	printf("Time %d: Hello World!\n", i);
}

int main(int argc, char **argv) {
	int i;

	for(i = 0; i < TIMES; i++) {
		hello_world(i);
		DTRACE_PROBE1(hello_app, hello_probe, i);
		sleep(PERIOD);
	}

	return 0;
}