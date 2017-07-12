#ifndef PLANE_H
#define PLANE_H

#define P_STR_MAX 128

/** 
 * Plane with no axes
 * Pretty much exists so I don't have to bother with allocating memory for pointers inside structs
 */
typedef struct {
	Vector cross_product;
	long double d;
	Vector center;
} Axis;


typedef struct {
	Vector cross_product;
	long double d;
	Vector center;
	Axis x_axis;
	Axis y_axis;
} Plane;

/**
 * @method constructs plane from a cross product vector and a 'd' value
 */
Plane p_new(Vector, long double);

/**
 * @method constructs plane from 3 points in space
 */
Plane p_from_points(Vector, Vector, Vector);

/** 
 * @method constructs plane from a vector and a center point
 */
Plane p_from_cp_cent(Vector, Vector);

Vector p_closest(Plane, Vector);

long double p_dist(Plane, Vector);

Vector p_project(Plane, Vector);

Vector p_unproject(Plane, Vector);

long double p_evaluate(Plane, Vector);

void _p_string(char*, size_t, Plane);

#endif
