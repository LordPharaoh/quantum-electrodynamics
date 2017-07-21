#include <math.h>
#include <stdlib.h>
#include <float.h>
#include "except.h"
#include "vector.h"
#include "circle.h"
#include "plane.h"
#include "sphere.h"
#include "calc_norm.h"

#define DELTA 7.7018
#define WAVELENGTH .123984
#define C_CONST 3e8 
#define FREQUENCY 2.41966e18 
#define PLANCK_CONSTANT 6.62606993e-34
#define REDUCED_PLANCK_CONSTANT 1.054571800e-34
#define MOMENTUM 5.344294457349335e-24
#define PHI 1.618033988749894

#define EMITTER ((Vector) {0, -16, 0})
#define MIDDLE_Y 1E-20
#define DETECTOR_Y 4
#define RANDOM 0
#define SUNFLOWER 1

#define IMAGE 1


long double q2cart(long double q) {
	return atan(2 * asin(q * WAVELENGTH / (4 * M_PI))) * DETECTOR_Y;
}


void calc_norm(double middle_grid_x, double middle_grid_y, int num_middles_x, int num_middles_y,
			   double qx_range, double qy_range, int num_detectors_x, int num_detectors_y, 
		       double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, 
			   size_t nlen, Sphere* spheres, size_t spherelen) {

	/* Determine step based on grid size and number of spots */
	int dim_subtract = 1;
	double xm_step = middle_grid_x == 0 ? 0.1 : ((double) middle_grid_x) / (num_middles_x - dim_subtract);
	double ym_step = ((double) middle_grid_y) / (num_middles_y - dim_subtract);

	double qxd_step = qx_range == 0 ? 0.1 : ((double) qx_range) / (num_detectors_x - dim_subtract);
	double qyd_step = ((double) qy_range) / (num_detectors_y - dim_subtract);

	Vector middles[num_middles_x * num_middles_y];

	long double gridminx = IMAGE ? -middle_grid_x * .5: 0;
	long double gridmaxx = IMAGE ? middle_grid_x * .5: middle_grid_x;
	long double gridminy = IMAGE ? -middle_grid_y * .5: 0;
	long double gridmaxy = IMAGE ? middle_grid_y * .5: middle_grid_y;
	
	int num_middles = 0;
	int total_middles = 0;

	for(double mid_x = gridminx; mid_x <= gridmaxx; mid_x += xm_step) {
		for(double mid_z = gridminy; mid_z <= gridmaxy; mid_z += ym_step) {
			/* Generate middle point */
			#if RANDOM
			long double randx = (rand() / (double) RAND_MAX) * middle_grid_x - .5 * middle_grid_x;
			long double randz = (rand() / (double) RAND_MAX) * middle_grid_y - .5 * middle_grid_y;
			Vector middle = Vec3(randx, MIDDLE_Y, randz);
			#elif SUNFLOWER
			double r = (sqrt(total_middles + .5) / sqrt(num_middles_x * num_middles_y - .5)) * (gridmaxy);
			double theta = 2 * M_PI * (total_middles + 1) / pow(PHI, 2);
			Vector middle = Vec3(r * cos(theta), MIDDLE_Y, r * sin(theta));
			total_middles++;
			#else /* RANDOM */
			Vector middle = Vec3(mid_x, MIDDLE_Y, mid_z);
			# endif /* RANDOM */
			for(int s = 0; s < spherelen; s++) {
				if(v_dist(middle, spheres[s].center) < spheres[s].radius) {
					middles[num_middles] = middle;
					num_middles++;
					break;
				}
			}
		}
	}

	int d = 0;

	for(double det_x = 0; det_x <= qx_range; det_x += qxd_step) {
		for(double det_z = 0; det_z <= qy_range; det_z += qyd_step) {

			Vector detector = Vec3(q2cart(det_x), DETECTOR_Y, q2cart(det_z));
			long double complex detector_sum = 0;

			for(int m = 0; m < num_middles; m++) {
				Vector middle = middles[m];
				long double time;	

				long double l1 = v_dist(EMITTER, middle);
				long double l2 = v_dist(middle, detector);
				time = (l1 + l2) / C_CONST;

				#ifdef NAN
				if(isnan(time)) {
					printf("Threw out nan\n");
					continue;
				}
				#elif defined(INFINITY)
				if(isinf(time)) {
					continue;
					printf("Threw out infinity\n");
				}
				#endif /* INFINITY */
				long double complex wave = cexp(time * FREQUENCY * I);
				detector_sum += wave;
			}

			double norm = (double) (log(pow(cabs(detector_sum), 2)));
			if(d < qzlen)
				qzs[d] = det_z;
			else fprintf(stderr, "BUFFER TOO SMALL TO WRITE QZ\n");
			if(d < qxlen)
				qxs[d] = det_x;
			else fprintf(stderr, "BUFFER TOO SMALL TO WRITE QX\n");
			if(d < nlen)
				norms[d] = norm;
			else fprintf(stderr, "BUFFER TOO SMALL TO WRITE NORM\n");

			printf("%i out of %i complete.\r", d + 1, num_detectors_x * num_detectors_y);
			d++;
		}
	}
	printf("\n");
}
