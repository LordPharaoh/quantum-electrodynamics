#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "plane.h"
#include "circle.h"
#include "calc_norm.h"

int main() {

	Plane p = p_from_points(Vec3(0, 0, 1), Vec3(0, 1, 0), Vec3(1, 0, 0));

	printf("Projected %Le, Unprojected %Le\n", v_dist(Vec2(1, 1), Vec2(0, 3)), v_dist(p_unproject(p, Vec2(1, 1)), p_unproject(p, Vec2(0, 3))));

	return 0;
}
