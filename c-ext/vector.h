#ifndef VECTOR_H
#define VECTOR_H
typdef struct {
	double x;
	double y;
	double z;
} vector;

vector v_sub(vector, vector);

vector v_add(vector, vector);

double v_dot(vector, vector);

vector v_mult(vector, vector);

double v_norm(vector);

double v_slope(vector, vector);

vector v_mid(vector, vector);

vector v_dist(vector, vector);

int v_collinear(vector, vector);

vector v_cross(vector, vector);
#endif
