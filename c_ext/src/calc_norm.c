#include <math.h>
#include <stdlib.h>
#include <float.h>
#include <pthread.h>
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
#define SUNFLOWER 0

#define IMAGE 1


double q2cart(double q) {
	return atan(2 * asin(q * WAVELENGTH / (4 * M_PI))) * DETECTOR_Y;
}

typedef struct {
	double start_x, start_y, end_x, end_y, x_step, y_step;
	int threadno;
	Vector* middles;
	double* middle_distance;
	size_t num_middles;
	double* qx;
	size_t qxlen;
	double* qz;
	size_t qzlen;
	double* norms;
	size_t nlen;
} Args;


void* calculate_detectors(void* args) {
	Args a = (*(Args*) args);
	printf("%e %e %e %e %e %e\n", a.start_x, a.start_y, a.end_x, a.end_y, a.x_step, a.y_step);

	Vector* middles = a.middles;

	double* qzs = a.qz;
	double* qxs = a.qx;
	double* norms = a.norms;
	int d = 0;

	for(double det_x = a.start_x; det_x <= a.end_x; det_x += a.x_step) {
		for(double det_z = a.start_y; det_z <= a.end_y; det_z += a.y_step) {

			Vector detector = Vec3(q2cart(det_x), DETECTOR_Y, q2cart(det_z));
			double complex detector_sum = 0;

			for(int m = 0; m < a.num_middles; m++) {
				Vector middle = middles[m];
				double time;	
				double l2 = v_dist(middle, detector);
				time = (a.middle_distance[m] + l2) / C_CONST;

				double complex wave = cexp(time * FREQUENCY * I);
				detector_sum += wave;
			}

			double norm = (double) (log(pow(cabs(detector_sum), 2)));
			if(d < a.qzlen)
				qzs[d] = det_z;
			else fprintf(stderr, "BUFFER TOO SMALL TO WRITE QZ\n");
			if(d < a.qxlen)
				qxs[d] = det_x;
			else fprintf(stderr, "BUFFER TOO SMALL TO WRITE QX\n");
			if(d < a.nlen)
				norms[d] = norm;
			else fprintf(stderr, "BUFFER TOO SMALL TO WRITE NORM\n");

			//printf("Thread %i: %i complete.\n", a.threadno, d + 1);
			d++;
		}
	}
	return NULL;
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
	double middle_distance[num_middles_x * num_middles_y];

	double gridminx = IMAGE ? -middle_grid_x * .5: 0;
	double gridmaxx = IMAGE ? middle_grid_x * .5: middle_grid_x;
	double gridminy = IMAGE ? -middle_grid_y * .5: 0;
	double gridmaxy = IMAGE ? middle_grid_y * .5: middle_grid_y;
	
	int num_middles = 0;
	int total_middles = 0;

	for(double mid_x = gridminx; mid_x <= gridmaxx; mid_x += xm_step) {
		for(double mid_z = gridminy; mid_z <= gridmaxy; mid_z += ym_step) {
			/* Generate middle point */
			#if RANDOM
			double randx = (rand() / (double) RAND_MAX) * middle_grid_x - .5 * middle_grid_x;
			double randz = (rand() / (double) RAND_MAX) * middle_grid_y - .5 * middle_grid_y;
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
					middle_distance[num_middles] = v_dist(EMITTER, middle);
					num_middles++;
					break;
				}
			}
		}
	}

	Args a1 = (Args) {0, 0,              qx_range, qy_range * .25, qxd_step, qyd_step, 0, &middles, &middle_distance, num_middles, qxs,            qxlen/4, qzs,            qzlen/4, norms,           nlen/4};
	Args a2 = (Args) {0, qy_range * .25, qx_range, qy_range * .5,  qxd_step, qyd_step, 1, &middles, &middle_distance, num_middles, &qxs[qxlen/4],   qxlen/4, &qzs[qzlen/4],   qzlen/4, &norms[nlen/4],   nlen/4};
	Args a3 = (Args) {0, qy_range * .5,  qx_range, qy_range * .75, qxd_step, qyd_step, 2, &middles, &middle_distance, num_middles, &qxs[qxlen/2],   qxlen/4, &qzs[qzlen/2],   qzlen/4, &norms[nlen/2],   nlen/4};
	Args a4 = (Args) {0, qy_range * .75, qx_range, qy_range,       qxd_step, qyd_step, 3, &middles, &middle_distance, num_middles, &qxs[3*qxlen/4], qxlen/4, &qzs[3*qzlen/4], qzlen/4, &norms[3*nlen/4], nlen/4};
	pthread_t p1, p2, p3, p4;
	pthread_create(&p1, NULL, calculate_detectors, &a1);
	pthread_create(&p2, NULL, calculate_detectors, &a2);
	pthread_create(&p3, NULL, calculate_detectors, &a3);
	pthread_create(&p4, NULL, calculate_detectors, &a4);
	pthread_join(p1, NULL);
	pthread_join(p2, NULL);
	pthread_join(p3, NULL);
	pthread_join(p4, NULL);
}
