#ifndef CIRCLE_H
#define CIRCLE_H

#include "vector.h"

typedef struct {
	vector center;
	double radius;
} circle;

typedef struct {
	vector point;
	double slope;
} line;


#endif

