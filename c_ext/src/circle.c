#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "circle.h"
#include "except.h"


void v_perp_bisect(Vector v1, Vector v2, double line[2]) {
	char* chump = malloc(sizeof (*chump) * V_STR_MAX);
	Vector mid = v_mid(v1, v2);
	_v_string(chump, V_STR_MAX, mid);
	double slope = v_slope(v1, v2);
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


Vector l_intersection(double l1[2], double l2[2]) {
	//Don't need to have an error check here because 
	//it should have been caught already if the lines are collinear
	double x = (l2[1] - l1[1]) / (l1[0] - l2[0]);
	double y = x * l1[0] + l1[1];
	return (Vector) {x, y};
}


Circle c_from_points(Vector v1, Vector v2, Vector v3) {
	if (v_collinear(v1, v2, v3)) {
		//TODO python error here
		fprintf(stderr, "Points used to make Circle are collinear. Make this a python error");
	}

	for(int i = 0; i < 6; i++) {

		double line1[2];
		double line2[2];

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
		double radius = v_dist(center, v1);
		return (Circle) {center, radius};
	}	

}


Circle c_new(Vector xy, double radius) {
	return (Circle) {xy, radius};
}


double c_chord_angle(Circle c, double chord_len) {
	return 2 * asin(chord_len / (2 * c.radius));
}


void c_intersection(Circle c, Circle o, Vector vecs[2]) {
	double d = v_dist(c.center, o.center);
	if(d == 0) {
		setflag(INVALID_ARGUMENT);
		return;
	}
	double mid_dst = (pow(c.radius, 2) - pow(o.radius, 2) + pow(d, 2)) / (2 * d);
	Vector relative_pt = v_mult(v_sub(o.center, c.center), (mid_dst / d));
	Vector mid_pt = v_add(c.center, relative_pt);
	double chord_len = 2 * pow(fabs(pow(c.radius, 2) - pow(mid_dst, 2)), .5);
	double slope = chord_len / (2 * d);
	vecs[0] = Vec2(mid_pt.x - slope * (o.center.y - c.center.y), mid_pt.y + slope * (o.center.x - c.center.x));
	vecs[1] = Vec2(mid_pt.x + slope * (o.center.y - c.center.y), mid_pt.y - slope * (o.center.x - c.center.x));
}


double c_arc_length(Circle c, Vector p1, Vector p2) {
	double central_angle = c_chord_angle(c, v_dist(p1, p2));
	return central_angle * c.radius;
}


void _c_string(char* str, size_t size, Circle c) {
	// This is unusable in python because of fundamentally different string handling
	char* vec = malloc(sizeof (*vec) * V_STR_MAX);
	_v_string(vec, V_STR_MAX, c.center);
	snprintf(str, size, "r:%e c:%s", c.radius, vec);
}
