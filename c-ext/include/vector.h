#ifndef VECTOR_H
#define VECTOR_H
#include <stdio.h>

//what are the odds
#define TERMINAL_VECTOR Vec3(1242646.23423, 1094756.304897, 3485289.4444444)
#define V_STR_MAX 64

typedef struct {
	double x;
	double y;
	double z;
} Vector;

Vector Vec3(double, double, double);

Vector Vec2(double, double);

Vector v_sub(Vector, Vector);

Vector v_add(Vector, Vector);

double v_dot(Vector, Vector);

Vector v_mult(Vector, double);

double v_norm(Vector);

double v_slope(Vector, Vector);

Vector v_mid(Vector, Vector);

double v_dist(Vector, Vector);

int v_collinear(Vector, Vector, Vector);

Vector v_cross(Vector, Vector);

int v_equal(Vector, Vector);

void _v_string(char*, size_t, Vector);

#endif
