#include <math.h>
#include <stdlib.h>
#include <float.h>
#include <assert.h>
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
#define MIDDLE_X 1E-20
#define DETECTOR_Y 4

#define RANDOM 0
#define SUNFLOWER 0
#define ON_SPHERE 1

#define ARC_INTERSECTIONS 0
#define INTERSECTIONS 0

#define IMAGE 1

#define NUM_THREADS 20


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
	Sphere* spheres;
	size_t spherelen;
} Args;


void* calculate_detectors(void* args) {
	Args a = (*(Args*) args);

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

				#if INTERSECTIONS || ARC_INTERSECTIONS
				// fit plane onto three point
				Plane cart = p_from_points(EMITTER, middle, detector);
				//project points onto plane
				Vector e_proj = p_project(cart, EMITTER);
				Vector m_proj = p_project(cart, middle);
				Vector d_proj = p_project(cart, detector);
				#endif /* INTERSECTIONS */

				//iter through spheres looking for intersections
				for(int s = 0; s < a.spherelen; s++) {
					Sphere sphere = a.spheres[s];
					#if INTERSECTIONS || ARC_INTERSECTIONS
					Circle slice = s_slice(sphere, cart);
					// We are outside the sphere if this is true
					if(slice.radius == -1) {
						clear_exception();
						printf("Skipped at slice\n");
						continue;
					}
					#else /* INTERSECTIONS */
					if(v_dist(middle, sphere.center) > sphere.radius) {
						continue;
					}
					#endif /* INTERSECTIONS */


					#if INTERSECTIONS
					Vector intersections[2];
					intersections[0] = c_v_intersection(slice, e_proj, m_proj);
					intersections[1] = c_v_intersection(slice, m_proj, d_proj);

					long double l2 = v_dist(intersections[0], intersections[1]);
					double l1 = v_dist(e_proj, intersections[0]) + v_dist(intersections[1], d_proj);
					
					// printf("Projected %Le Unprojected %Le\n", v_dist(EMITTER, middle), v_dist(e_proj, m_proj));
					// double l1 = v_dist(EMITTER, intersections[0]) + v_dist(intersections[1], detector);

					double time = (l1 / C_CONST) + (l2 / (C_CONST / sphere.refrac_idx));
					#elif ARC_INTERSECTIONS
					double dist = p_dist(cart, sphere.center);
					double angle = acos(dist / sphere.radius);
					Circle small = c_new(Vec2(0, 0), sphere.radius * sin(angle));
					Circle large = c_from_points(e_proj, m_proj, d_proj);

					Vector intersections[2];
					c_intersection(small, large, intersections);
					double time =  (c_arc_length(large, e_proj, intersections[0]) / C_CONST)
								 + (c_arc_length(large, intersections[0], intersections[1]) / (C_CONST / sphere.refrac_idx))
								 + (c_arc_length(large, intersections[1], d_proj) / C_CONST);
					
					#else /* INTERSECTIONS */
					double dist = v_dist(EMITTER, middle) + v_dist(middle, detector);
					double time = dist / C_CONST;
					#endif /* INTERSECTIONS */

					if(!isnormal(time)) {
						continue;
					}

					double complex wave = cexp(time * FREQUENCY * I);
					detector_sum += wave;
				}
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

			if ((d % 100) == 0) {
				printf("Thread %i: %i complete.\n", a.threadno, d + 1);
			}
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
			Vector middle = Vec3(randx != 0 ? randx : MIDDLE_X, MIDDLE_Y, randz);
			#elif SUNFLOWER
			double r = (sqrt(total_middles + .5) / sqrt(num_middles_x * num_middles_y - .5)) * (gridmaxy);
			double theta = 2 * M_PI * (total_middles + 1) / pow(PHI, 2);
			Vector middle = Vec3(r * cos(theta), MIDDLE_Y, r * sin(theta));
			total_middles++;
			#else /* RANDOM */
			Vector middle = Vec3(mid_x != 0 ? mid_x : MIDDLE_X, MIDDLE_Y, mid_z);
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

	pthread_t threads[NUM_THREADS];
	double step = pow((double) NUM_THREADS, -1);
	Args a[NUM_THREADS];

	for(int t = 0; t < NUM_THREADS; t++) {
		int qxidx = (int) qxlen * t * step;
		int qzidx = (int) qzlen * t * step;
		int nidx = (int) nlen * t * step;
		a[t] = (Args) { 0, qy_range * step * t, qx_range, qy_range * step * (t + 1), qxd_step, qyd_step, t, 
						middles, middle_distance, num_middles, &(qxs[qxidx]), qxlen * step, &(qzs[qzidx]), 
						qzlen * step, &(norms[nidx]), nlen * step, spheres, spherelen };
		pthread_create(&threads[t], NULL, calculate_detectors, &a[t]);
	}

	for(int t = 0; t < NUM_THREADS; t++) {
		pthread_join(threads[t], NULL);
	}
}
