#ifndef VECTOR_H
#define VECTOR_H
#include <stdio.h>
#include <math.h>

//what are the odds
#define TERMINAL_VECTOR Vec3(1242646.23423, 1094756.304897, 3485289.4444444)
#define V_STR_MAX 64
// assertion is a macro so you get the correct line number
typedef struct {
	long double x;
	long double y;
	long double z;
} Vector;

Vector Vec3(long double, long double, long double);

Vector Vec2(long double, long double);

Vector v_sub(Vector, Vector);

Vector v_add(Vector, Vector);

long double v_dot(Vector, Vector);

Vector v_mult(Vector, long double);

long double v_norm(Vector);

long double v_slope(Vector, Vector);

Vector v_mid(Vector, Vector);

long double v_dist(Vector, Vector);

long double v_collinear(Vector, Vector, Vector);

Vector v_cross(Vector, Vector);

int v_equal(Vector, Vector);

int v_isnormal(Vector);

Vector v_normalize(Vector);

void _v_string(char*, size_t, Vector);

#endif
