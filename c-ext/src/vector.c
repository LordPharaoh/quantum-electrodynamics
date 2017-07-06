#include "vector.h"
#include "except.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

//A lot of these functions could probably be optimized with preprocessor macros but that might be a bit much
Vector Vec3(double x, double y, double z) {
	return (Vector) {x, y, z};
}

Vector Vec2(double x, double y) {
	return Vec3(x, y, 0);
}

Vector v_sub(Vector v1, Vector v2) {
	return Vec3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);
}


Vector v_add(Vector v1, Vector v2) {
	return Vec3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);
}


double v_dot(Vector v1, Vector v2) {
	return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
}


Vector v_mult(Vector v, double s) {
	return Vec3(v.x * s, v.y * s, v.z * s);
}


double v_norm(Vector v) {
	return sqrt(v_dot(v, v));
}


double v_slope(Vector v1, Vector v2) {
	Vector sub = v_sub(v1, v2);
	if(sub.x == 0) {
		setflag(ZERO_DIVISION);
		return 0;
	}
	char* chump = (char*) malloc(sizeof (*chump) * V_STR_MAX);
	_v_string(chump, V_STR_MAX, sub);
	return sub.y / sub.x;
}


Vector v_mid(Vector v1, Vector v2) {
	return v_mult(v_add(v1, v2), .5);
}


double v_dist(Vector v1, Vector v2) {
	return v_norm(v_sub(v1, v2));
}


int v_collinear(Vector v1, Vector v2, Vector v3){
	for(int i = 0; i < 6; i++) {
		int success1, success2;
		double slope1 = v_slope(v1, v2);
		double slope2 = v_slope(v2, v3);
		if(check_exception() == ZERO_DIVISION) {
			Vector vtemp = v1;
			v1 = v2;
			v2 = v3;
			v3 = vtemp;
			continue;
		}
		else if(slope1 == slope2) {
			return 1;
		}
		else {
			break;
		}
	}
	return 0;
}


Vector v_cross(Vector v1, Vector v2) {
	double x = v1.y * v2.z - v1.z * v2.y;
	double y = v1.z * v2.x - v1.x * v2.z;
	double z = v1.x * v2.y - v1.y * v2.x;
	return Vec3(x, y, z);
}


int v_equal(Vector v1, Vector v2) {
	return v1.x == v2.x && v1.y == v2.y && v1.z == v2.z;
}


void _v_string(char* str, size_t size, Vector v) {
	// This is unusable in python because of fundamentally different string handling
	snprintf(str, size, "<%e, %e, %e>", v.x, v.y, v.z);
}
