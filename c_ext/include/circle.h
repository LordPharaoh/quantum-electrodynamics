#ifndef CIRCLE_H
#define CIRCLE_H

#define C_STR_MAX 128

#include "vector.h"
#include <stdio.h>

typedef struct {
	Vector center;
	long double radius;
} Circle;

Circle c_from_points(Vector, Vector, Vector);

Circle c_new(Vector, long double);

void _c_string(char*, size_t, Circle);

long double c_chord_angle(Circle, long double);

Circle c_new(Vector, long double);

void c_intersection(Circle, Circle, Vector*);

long double c_arc_length(Circle, Vector, Vector);

Vector c_v_intersection(Circle, Vector, Vector);

long double c_evaluate(Circle, Vector);

#ifdef C_TEST
void v_perp_bisect(Vector, Vector, long double*);
Vector l_intersection(long double*, long double*);
#endif

#endif

