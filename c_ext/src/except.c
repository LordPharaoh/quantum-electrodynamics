#include "except.h"

static int exception;

void error(const char *msg) {
	fprintf(stderr, "\x1b[31;1m %s \x1b[0m\n", msg);
}

void setflag(int except) {
	if(exception != CLEAR) {
		fprintf(stderr, "\x1b[33;1m WARNING: Previously uncleared exception %i erased. \x1b[0m\n", except);
	}
	exception = except;
}

void raise_error(int except, const char *msg) {
	setflag(except);
	error(msg);
}

int check_exception() {
	int temp = exception;
	clear_exception();
	return temp;
}

void clear_exception() {
	exception = CLEAR;
}
