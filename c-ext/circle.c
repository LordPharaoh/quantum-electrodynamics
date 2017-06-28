#include <math.h>
#include "circle.h"

line v_perp_bisect(vector v1, vector v2) {
	vector mid = v_mid(v1, v2)
	double slope = v_slope(v1, v2)
	return (line) {mid, slope};
}

