#include <math.h>
#include "vector.h"

//A lot of these functions could probably be optimized with preprocessor macros but that might be a bit much
vector v_sub(vector v1, vector v2) {
	return (vector) {v1.x - v2.x, v1.y - v2.y, v1.z - v2.z};
}


vector v_add(vector v1, vector v2) {
	return (vector) {v1.x + v2.x, v1.y + v2.y, v1.z + v2.z};
}


double v_dot(vector v1, vector v2) {
	return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
}


vector v_mult(vector v, double s) {
	return (vector) {v.x * s, v.y * s, v.z * s};
}


double v_norm(vector v) {
	return sqrt(v_dot(v, v));
}


double v_slope(vector v1, vector v2) {
	sub = v_sub(v1, v2);
	return sub.y / sub.x;
}


vector v_mid(vector v1, vector v2) {
	return v_mult(v_sub(v1, v2), .5);
}


vector v_dist(vector v1, vector v2) {
	return v_norm(v_sub(v1, v2));
}


int v_collinear(vector v1, vector v2, vector v3){
	double slope1 = v_slope(v1, v2);
	double slope2 = v_slope(v2, v3);
	return slope1 == slope2;
}


vector v_cross(vector v1, vector v2) {
	double x = v1.y * v2.z - v1.z * v2.y;
	double y = v1.z * v2.x - v1.x * v2.z;
	double z = v1.x * v2.y - v1.y * v2.x;
	return (vector) {x, y, z};
}
