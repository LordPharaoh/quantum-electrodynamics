#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "circle.h"
#include "except.h"


void v_perp_bisect(Vector v1, Vector v2, long double line[2]) {
	char* chump = malloc(sizeof (*chump) * V_STR_MAX);
	Vector mid = v_mid(v1, v2);
	_v_string(chump, V_STR_MAX, mid);
	long double slope = v_slope(v1, v2);
	int exc;
	if((exc = check_exception()) == CLEAR) {
		if(slope == 0) {
			line[0] = 0;
			line[1] = 0;
			raise_error(ZERO_DIVISION, "Warning: Zero Division in v_perp_bisect in src/Circle.c");
			return;
		}	
		else { 
			line[0] = -1 / slope; 
			line[1] = line[0] * -mid.x + mid.y;
			return;
		}
	}
	else if (exc == ZERO_DIVISION) {
		// Line was vertical
		line[0] = 0;
		line[1] = line[0] * -mid.x + mid.y;
		clear_exception();
		return;
	}
	raise_error(GENERIC_ERROR, "Weird errors in perp_bisect");
	exit(EXIT_FAILURE);
}


Vector l_intersection(long double l1[2], long double l2[2]) {
	//Don't need to have an error check here because 
	//it should have been caught already if the lines are collinear
	long double x = (l2[1] - l1[1]) / (l1[0] - l2[0]);
	long double y = x * l1[0] + l1[1];
	return (Vector) {x, y};
}


Circle c_from_points(Vector v1, Vector v2, Vector v3) {
	if (v_slope(v1, v2) == v_slope(v3, v2)) {
		//TODO python error here
		fprintf(stderr, "Points used to make Circle are collinear. Make this a python error\n");
		return c_new(Vec3(-1, -1, -1), -1);
	}

	for(int i = 0; i < 6; i++) {

		long double line1[2];
		long double line2[2];

		v_perp_bisect(v1, v2, line1);
		v_perp_bisect(v2, v3, line2);

		if(check_exception() == ZERO_DIVISION) {
			Vector vtemp = v1;
			v1 = v2;
			v2 = v3;
			v3 = vtemp;
			continue;
		}

		Vector center = l_intersection(line1, line2);
		long double radius = v_dist(center, v1);
		return (Circle) {center, radius};
	}	

}


Circle c_new(Vector xy, long double radius) {
	return (Circle) {xy, radius};
}


long double c_chord_angle(Circle c, long double chord_len) {
	return 2 * asin(chord_len / (2 * c.radius));
}


void c_intersection(Circle c, Circle o, Vector vecs[2]) {
	long double d = v_dist(c.center, o.center);
	if(d == 0) {
		setflag(INVALID_ARGUMENT);
		return;
	}
	long double mid_dst = (pow(c.radius, 2) - pow(o.radius, 2) + pow(d, 2)) / (2 * d);
	Vector relative_pt = v_mult(v_sub(o.center, c.center), (mid_dst / d));
	Vector mid_pt = v_add(c.center, relative_pt);
	long double chord_len = 2 * pow(fabs(pow(c.radius, 2) - pow(mid_dst, 2)), .5);
	long double slope = chord_len / (2 * d);
	Vector vec0 = Vec2(mid_pt.x - slope * (o.center.y - c.center.y), mid_pt.y + slope * (o.center.x - c.center.x));
	Vector vec1 = Vec2(mid_pt.x + slope * (o.center.y - c.center.y), mid_pt.y - slope * (o.center.x - c.center.x));
	if(vec0.x < vec1.x) {
		vecs[0] = vec0;
		vecs[1] = vec1;
	}
	else {
		vecs[1] = vec0;
		vecs[0] = vec1;
	}
}


Vector c_v_intersection(Circle c, Vector p1, Vector p2) {
	long double dx = p2.x - p1.x;
	long double dy = p2.y - p1.y;
	long double dr = sqrt(dx * dx + dy * dy);
	long double determinant = p1.x * p2.y - p2.x * p1.y;
	long double discriminant = sqrt(pow(c.radius, 2) * pow(dr, 2) - pow(determinant, 2));

	long double sign = (dy < 0) ? -1.0 : 1.0;
	// add if less than midpoint and subtract if greater to get the right intersection
	long double plusminus = (-determinant * dx < v_mid(p1, p2).y) ? 1.0 : -1.0;
	long double x = determinant * dy + plusminus * sign * dx * discriminant;
	x = x / pow(dr, 2);
	long double y = -determinant * dx + plusminus * abs(dy) * discriminant;
	y = y / pow(dr, 2);
	Vector solution = Vec2(x, y);
	return solution;
}


long double c_arc_length(Circle c, Vector p1, Vector p2) {
	long double central_angle = c_chord_angle(c, v_dist(p1, p2));
	return central_angle * c.radius;
}


void _c_string(char* str, size_t size, Circle c) {
	// This is unusable in python because of fundamentally different string handling
	char* vec = malloc(sizeof (*vec) * V_STR_MAX);
	_v_string(vec, V_STR_MAX, c.center);
	snprintf(str, size, "r:%Lf c:%s", c.radius, vec);
}


long double c_evaluate(Circle c, Vector v) {
	Vector offset = v_sub(v, c.center);
	long double r2 = pow(offset.x, 2) + pow(offset.y, 2);
	return abs(r2 - pow(c.radius, 2));
}
