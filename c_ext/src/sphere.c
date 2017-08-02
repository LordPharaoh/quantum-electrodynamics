#include <math.h>
#include <assert.h>
#include "sphere.h"


Sphere s_new(Vector center, double radius, double refrac_idx) {
	return (Sphere) {center, (long double) radius, (long double) refrac_idx};
}


Circle s_slice(Sphere s, Plane p) {
	/* returns the circle created by slicing a sphere with a plane */
	long double dist = p_dist(p, s.center);
	if(dist >= s.radius) {
		return c_new(Vec3(-1, -1, -1), -1);
	}

	long double angle = acos(dist / s.radius);
	assert(v_isnormal(p.cross_product));
	assert(v_isnormal(s.center));
	Vector circle_center = p_project(p, s.center);

	assert(v_isnormal(circle_center));
	assert(isnormal(s.radius));
	return c_new(circle_center, s.radius * sin(angle));
}


