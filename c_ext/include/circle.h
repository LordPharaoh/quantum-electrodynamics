#ifndef CIRCLE_H
#define CIRCLE_H

#define C_STR_MAX 128

#include "vector.h"
#include <stdio.h>

typedef struct {
	Vector center;
	double radius;
} Circle;

Circle c_from_points(Vector, Vector, Vector);

void _c_string(char*, size_t, Circle);

double c_chord_angle(Circle, double);

Circle c_new(Vector, double);

void c_intersection(Circle, Circle, Vector*);

double c_arc_length(Circle, Vector, Vector);

#ifdef C_TEST
void v_perp_bisect(Vector, Vector, double*);
Vector l_intersection(double*, double*);
#endif

#endif

