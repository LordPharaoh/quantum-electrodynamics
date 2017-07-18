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
#define WAVELENGTH 1.23984
#define C_CONST 3e8 
#define FREQUENCY 2.41966e18 
#define PLANCK_CONSTANT 6.62606993e-34
#define REDUCED_PLANCK_CONSTANT 1.054571800e-34
#define MOMENTUM 5.344294457349335e-24

#define EMITTER ((Vector) {0, -16, 0})
#define MIDDLE_Y 1E-20
#define DETECTOR_Y 4

#define ARCS 0
#define INTERSECTIONS 0
#define BLOCKING 0
#define FEYNMAN 0


long double q2cart(long double q) {
	return atan(2 * asin(q * WAVELENGTH / (4 * M_PI))) * DETECTOR_Y;
}


void calc_norm(double middle_grid_x, double middle_grid_y, int num_middles_x, int num_middles_y,
			   double qx_range, double qy_range, int num_detectors_x, int num_detectors_y, 
		       double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, 
			   size_t nlen, Sphere* spheres, size_t spherelen) {

	/* Determine step based on grid size and number of spots */
	double xm_step = ((double) middle_grid_x) / num_middles_x;
	double ym_step = ((double) middle_grid_y) / num_middles_y;

	double qxd_step = ((double) qx_range) / num_detectors_x;
	double qyd_step = ((double) qy_range) / num_middles_y;

	long double det_x = 0;
	long double det_z = 0;

	for(int d = 0; d < num_detectors_x * num_detectors_y; d++) {

		#if FEYNMAN
		long double complex detector_sum = 0;
		#else
		long double complex detector_sum = 0;
		#endif /* FEYNMAN */

		/* generate detector point */
		Vector detector = Vec3(q2cart(det_x), DETECTOR_Y, q2cart(det_z));
		det_z += qyd_step;
		if(det_z >= qy_range) {

			det_z = 0;
			det_x += qxd_step;
		}

		long double mid_x = -middle_grid_x * .5;
		long double mid_z = -middle_grid_y * .5;

		for(int m = 0; m < num_middles_x * num_middles_y; m++) {

			/* Generate middle point */
			Vector middle = Vec3(mid_x, MIDDLE_Y, mid_z);
			mid_z += ym_step;
			if(mid_z >= middle_grid_y) {
				mid_z = 0;
				mid_x += xm_step;
			}

			#if !FEYNMAN

			long double time;	

			#if ARCS

			// calculate straight time from point to another over hte path of a big circle
			if (v_collinear(e_proj, m_proj, d_proj) < 1e-20) {
				//FIXME this line is causing a segfault raise_error(INVALID_ARGUMENT, "Points are collinear");
				continue;
			}
			Circle large = c_from_points(e_proj, m_proj, d_proj);
			time = c_arc_length(large, e_proj, d_proj) / C_CONST;

			#else /* ARCS*/
			#if BLOCKING
			if(v_dist(middle, spheres[0].center) < spheres[0].radius) {

				continue;
			}
			#endif /* BLOCKING */

			long double l1 = v_dist(EMITTER, middle);
			long double l2 = v_dist(middle, detector);
			time = (l1 + l2) / C_CONST;
			#endif /* ARCS */


			#if ARCS || INTERSECTIONS
			// Fit plane to the 3 points then project the points onto the plane
			Plane cart = p_from_points(EMITTER, middle, detector);

			Vector e_proj = p_project(cart, EMITTER);
			Vector m_proj = p_project(cart, middle);
			Vector d_proj = p_project(cart, detector);
			#endif /* ARCS || INTERSECTIONS */

			#if INTERSECTIONS
			/* Loop through spheres */	
			int insphere = 0;
			for(int s = 0; s < spherelen; s++) {

				Sphere sphere = spheres[s];
				Circle slice = s_slice(sphere, cart);
				if(slice.radius != -1) continue;

				#if ARCS /* 2 */
				if (v_collinear(e_proj, m_proj, d_proj) < 1e-20) {
					//FIXME this line is causing a segfault raise_error(INVALID_ARGUMENT, "Points are collinear");
					continue;
				}

				Vector intersections[2];
				Circle large = c_from_points(e_proj, m_proj, d_proj);
				c_intersection(slice, large, intersections);
				long double dist = c_arc_length(large, intersections[0], intersections[1]);
				time -= (dist / C_CONST) - (dist * sphere.refrac_idx / C_CONST);
				#else /* ARCS 2 */
				//sphere intersections
				Vector p1 = p_unproject(cart, c_v_intersection(slice, e_proj, m_proj));
				Vector p2 = p_unproject(cart, c_v_intersection(slice, m_proj, d_proj));

				long double l2 = v_dist(p1, middle) + v_dist(middle, p2);

				time += (l2 / C_CONST) - (l2 * sphere.refrac_idx / C_CONST);
				#endif /* ARCS 2 */ 
			} 
			#endif /* INTERSECTIONS */

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
			#else /* FEYNMAN! */

			#if BLOCKING
			if(v_dist(middle, spheres[0].center) < spheres[0].radius) {
				continue;
			}
			#endif /* BLOCKING */
			Vector unit = v_mult(middle, 1 / v_norm(middle));
			Vector momentum = Vec3(0, MOMENTUM, 0); // v_mult(unit, MOMENTUM);

			Vector dist = v_sub(EMITTER, detector);
			detector_sum += cexp(I * v_dot(dist, momentum) / REDUCED_PLANCK_CONSTANT) / v_norm(dist);

			#endif /* !FEYNMAN */
		}
		double norm = (double) (log(pow(cabs(detector_sum), 2)));
		if(d < qzlen)
			qzs[d] = det_z;
		else fprintf(stderr, "BUFFER TO SMALL TO WRITE QZ");
		if(d < qxlen)
			qxs[d] = det_x;
		else fprintf(stderr, "BUFFER TO SMALL TO WRITE QX");
		if(d < nlen)
			norms[d] = norm;
		else fprintf(stderr, "BUFFER TO SMALL TO WRITE NORM");

		printf("%i out of %i complete.\r", d + 1, num_detectors_x * num_detectors_y);
	}
	printf("\n");
}


