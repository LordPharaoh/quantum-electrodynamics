#include "vector.h"
#include "except.h"
#include "plane.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

Axis x_axis(Plane);
Axis y_axis(Plane);


Plane wrap_axis(Axis a) {
	Plane p;
	p.cross_product = a.cross_product;
	p.d = a.d;
	p.center = a.center;
	return p;
}


Plane p_new(Vector cp, long double d) {
	Plane p;
	p.cross_product = cp;
	p.d = d;
	p.center = p_closest(p, Vec3(0, 0, 0));
	p.x_axis = x_axis(p);
	p.y_axis = y_axis(p);
	return p;
}


Axis p_from_cp_cent_noaxes(Vector cp, Vector point) {

	long double d = -1.0 * (v_dot(cp, point));
	Axis p;
	p.cross_product = cp;
	p.d = d;
	p.center = p_closest(wrap_axis(p), Vec3(0, 0, 0));
	return p;
}


Axis x_axis(Plane p) {
	/// Constructs an orthogonal x-axis for a plane
	Vector cp = v_sub(p_closest(p, Vec3(1, 0, 0)), p.center);
	return p_from_cp_cent_noaxes(cp, p.center);
}


Axis y_axis(Plane p) {
	/// Constructs a y-axis orthogonal to a plane and its x axis
	Vector cp = v_cross(p.x_axis.cross_product, p.cross_product);
	return p_from_cp_cent_noaxes(cp, p.center);
}


Plane p_from_cp_cent(Vector cp, Vector point) {
	long double d = -1.0 * (v_dot(cp, point));
	return p_new(cp, d);
}


Plane p_from_points(Vector v1, Vector v2, Vector v3) {
	Vector vs1 = v_sub(v1, v2);
	Vector vs2 = v_sub(v2, v3);
	Vector cross = v_cross(vs1, vs2);
	long double scalar = sqrt(pow(cross.x, 2) + pow(cross.y, 2) + pow(cross.z, 2));
	cross = v_mult(cross, scalar);
	return p_from_cp_cent(cross, v1);
}


Vector p_closest(Plane p, Vector point) {
	long double t = - p_dist(p, point) / v_norm(p.cross_product);
	return v_add(v_mult(p.cross_product, t), point);
}
	

long double p_evaluate(Plane p, Vector v) {
	return v_dot(p.cross_product, v) + p.d;
}


long double p_dist(Plane p, Vector point) {
	return p_evaluate(p, point) / v_norm(p.cross_product);
}
	

Vector p_project(Plane p, Vector point) {
	Vector pt_on_plane = p_closest(p, point);
	long double y = p_dist(wrap_axis(p.y_axis), pt_on_plane);
	long double x = p_dist(wrap_axis(p.x_axis), pt_on_plane);
	return Vec2(x, y);
}


Vector p_unproject(Plane p, Vector point) {
	/* Just a giant formula, if you have to debug this, you might be better off rewriting
	 I worked it all out at one point and then wrote it down
	 There's not much to comment because most of the variables aren't meaningful, they're just intermediate steps
	 in the solution. */
	
	Plane xax = wrap_axis(p.x_axis);
	Plane yax = wrap_axis(p.y_axis);
	
	long double x_offset = (point.x * v_norm(xax.cross_product) - xax.d) / xax.cross_product.x;

	long double y_divisor =  yax.cross_product.y * xax.cross_product.x 
					  - yax.cross_product.x * xax.cross_product.y;

	long double y_term_1 = point.y * xax.cross_product.x * v_norm(yax.cross_product);
	long double y_term_2 = yax.d * xax.cross_product.x;
	long double y_term_3 = yax.cross_product.x * xax.cross_product.x * x_offset;

	long double y_offset = (y_term_1 - y_term_2 - y_term_3) / y_divisor;
	long double y_coefficient = (yax.cross_product.x * xax.cross_product.z 
	                      - xax.cross_product.x * yax.cross_product.z) 
						  / y_divisor;

	long double z_offset = - p.cross_product.x * x_offset 
					  + ((p.cross_product.x * xax.cross_product.y * y_offset) / xax.cross_product.x) 
					  - p.cross_product.y * y_offset;
	long double z_divisor = - ((p.cross_product.x * xax.cross_product.y * y_coefficient) / xax.cross_product.x)
					   - ((p.cross_product.x * xax.cross_product.z) / xax.cross_product.x)
					   + p.cross_product.y * y_coefficient
					   + p.cross_product.z;

	long double z = z_offset / z_divisor;
	long double y = y_offset + y_coefficient * z;
	long double x = x_offset + ((-xax.cross_product.y * y - xax.cross_product.z * z) 
						   / xax.cross_product.x);

	return v_add(Vec3(x, y, z), p.center);
}


void _p_string(char* c, size_t n, Plane p) {
	snprintf(c, n, "%Lfx + %Lfy + %Lfc + %Lf = 0", p.cross_product.x, p.cross_product.y, p.cross_product.z, p.d);
}
