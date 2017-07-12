#ifndef SPHERE_H
#define SPHERE_H

#include "vector.h"
#include "circle.h"
#include "plane.h"
#include <stdio.h>

typedef struct {
	Vector center;
	long double radius;
	long double refrac_idx;
} Sphere;

Sphere s_new(Vector, double, double);

Circle s_slice(Sphere, Plane);

#endif

