#include <math.h>


typedef struct {
	float x;
	float y;
	float z;
} vector;
typedef vector point;

//A lot of these functions could probably be optimized with preprocessor macros
vector v_sub(vector v1, vector v2) {
	return (vector) {v1.x - v2.x, v1.y - v2.y, v1.z - v2.z};
}


vector v_add(vector v1, vector v2) {
	return (vector) {v1.x + v2.x, v1.y + v2.y, v1.z + v2.z};
}


float v_dot(vector v1, vector v2) {
	return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
}


vector v_mult(vector v, float s) {
	return (vector) {v.x * s, v.y * s, v.z * s};
}


float v_norm(vector v) {
	return sqrt(v_dot(v, v));
}


float v_slope(vector v1, vector v2) {
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
	slope1 = v_slope(v1, v2);
	slope2 = v_slope(v2, v3);
	return slope1 == slope2;
}


vector v_cross(vector v1, vector v2) {
	x = v1.y * v2.z - v1.z * v2.y;
	y = v1.z * v2.x - v1.x * v2.z;
	z = v1.x * v2.y - v1.y * v2.x;
	return (vector) {x, y, z};
}


int main() {
	return 0;
}
