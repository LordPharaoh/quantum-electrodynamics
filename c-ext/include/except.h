#ifndef EXCEPT_H
#define EXCEPT_H

#include <stdio.h>

void error(const char*);
void setflag(int);
int check_exception();
void clear_exception();
void raise_error(int, const char*);

#define CLEAR 0
#define ZERO_DIVISION 1
#define INVALID_ARGUMENT 2
#define GENERIC_ERROR 3

#endif
