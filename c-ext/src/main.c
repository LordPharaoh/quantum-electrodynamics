#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "plane.h"
#include "circle.h"

int main() {

#define TEST_PLANE

#ifdef TEST_PLANE
	Plane p1 = p_from_points(Vec3(1, 3, 12), Vec3(2, 4, 8), Vec3(19, 27, 33));
	Vector projected = p_project(p1, Vec3(12, 45, 34));
	Vector unprojected = p_unproject(p1, projected);

	char* printy = (char*) malloc(sizeof (*printy) * V_STR_MAX);	
	_v_string(printy, V_STR_MAX, projected);
	printf("PROJECTED %s\n", printy);

	char* printy2 = (char*) malloc(sizeof (*printy2) * V_STR_MAX);	
	_v_string(printy2, V_STR_MAX, unprojected);
	printf("UNPROJECTED %s\n", printy2);
#endif

#ifdef TEST_CIRCLE
	Circle c1 = c_new(Vec2(34, 23), 12);
	Circle c2 = c_new(Vec2(22, 12), 10);
	Vector vecs[2];
	c_intersection(c1, c2, vecs);

	for(int v = 0; v < 2; v++) {
		char* chump = (char*) malloc(sizeof (*chump) * V_STR_MAX);
		_v_string(chump, V_STR_MAX, vecs[v]);
		printf("VEC %i: %s\n", v, chump);
		free(chump);
	}
#endif

	return 0;
}
