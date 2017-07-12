#include <math.h>
#include <stdlib.h>
#include <float.h>
#include "except.h"
#include "vector.h"
#include "circle.h"
#include "plane.h"
#include "calc_norm.h"

#define DELTA 7.7018
#define WAVELENGTH .123984
#define C_CONST 3e8
#define FREQUENCY 2.41966e18

#define ARCS 0
#define INTERSECTIONS 0

void calc_norm(Vector* emitters, size_t elen, Vector* middles, size_t mlen, Vector* detectors, size_t dlen, double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen, double sphere_radius, double ref_index) {

	for(int d = 0; d < dlen; d++) {
		long double complex detector_sum = 0;
		for(int m = 0; m < mlen; m++) {
			for(int e = 0; e < elen; e++) {

				long double time;	

				#if ARCS || INTERSECTIONS
				// Fit plane to the 3 points then project the points onto the plane
				Plane cart = p_from_points(emitters[e], middles[m], detectors[d]);

				Vector e_proj = p_project(cart, emitters[e]);
				Vector m_proj = p_project(cart, middles[m]);
				Vector d_proj = p_project(cart, detectors[d]);
				#endif /* ARCS || INTERSECTIONS */

				
				#if INTERSECTIONS
				if(v_norm(middles[m]) > sphere_radius) {
					#if ARCS /* 1 */
					// calculate straight time from point to another over hte path of a big circle
					Circle large = c_from_points(e_proj, m_proj, d_proj);
					time = c_arc_length(large, e_proj, d_proj) / C_CONST;
					#else /* ARCS 1 */
					long double l1 = v_dist(e_proj, m_proj);
					long double l2 = v_dist(m_proj, d_proj);
					time = (l1 + l2) / C_CONST;
					#endif /* ARCS 1 */ 
				}
				else {

					long double dist = p_dist(cart, Vec3(0, 0, 0));
					long double angle = acos(dist / sphere_radius);
					// Center of new cart plane
					Circle small = c_new(Vec2(0, 0), sphere_radius * sin(angle));

					#if ARCS /* 2 */
					Vector intersections[2];
					// This should be done somewhere else
					if (v_collinear(e_proj, m_proj, d_proj) < 1e-20) {
						//FIXME this line is causing a segfault raise_error(INVALID_ARGUMENT, "Points are collinear");
						continue;
					}

					Circle large = c_from_points(e_proj, m_proj, d_proj);
					c_intersection(small, large, intersections);
					time =   (c_arc_length(large, e_proj, intersections[0]) 
							+ (c_arc_length(large, intersections[0], intersections[1]) * ref_index)
							+ c_arc_length(large, intersections[1], detectors[d])) 
							/ C_CONST;
					#else /* ARCS 2 */
					//sphere intersections
					Vector p1 = p_unproject(cart, c_v_intersection(small, e_proj, m_proj));
					Vector p2 = p_unproject(cart, c_v_intersection(small, m_proj, d_proj));

					long double l1 = v_dist(emitters[e], p1);
					long double l2 = v_dist(p1, middles[m]) + v_dist(middles[m], p2);
					long double l3 = v_dist(p2, detectors[d]);

					time = (l1/C_CONST) + ((l2 * ref_index) / C_CONST) + (l3 / C_CONST);

					#endif /* ARCS 2 */ } 
				#elif ARCS /* INTERSECTIONS */
				// calculate straight time from point to another over hte path of a big circle
				if (v_collinear(e_proj, m_proj, d_proj) < 1e-20) {
					//FIXME this line is causing a segfault raise_error(INVALID_ARGUMENT, "Points are collinear");
					continue;
				}
				Circle large = c_from_points(e_proj, m_proj, d_proj);
				time = c_arc_length(large, e_proj, d_proj) / C_CONST;
				#else /* INTERSECTIONS */
					long double l1 = v_dist(emitters[e], middles[m]);
					long double l2 = v_dist(middles[m], detectors[d]);
					time = (l1 + l2) / C_CONST;
				#endif /* INTERSECTIONS */

				#ifdef NAN
				if(isnan(time)) {
					printf("Threw out nan\n");
					continue;
				}
				#elif defined(INFINITY)
				if(isinf(time)) {
					continue;
					printf("Threw out nan\n");
				}
				#endif /* INFINITY */
				long double complex wave = cexp(time * FREQUENCY * I);
				detector_sum += wave;
			}
		}
		long double z = tan(detectors[d].z / detectors[d].y) / 2;
		long double x = tan(detectors[d].x / detectors[d].y) / 2;
		double qz = (double) (4 * M_PI * sin(z) / WAVELENGTH);
		double qx = (double) (4 * M_PI * sin(x) / WAVELENGTH);
		double norm = (double) (log(pow(cabs(detector_sum), 2)));
		printf("NORM: %.17e\n", norm);
		if(d < qzlen)
			qzs[d] = qz;
		else fprintf(stderr, "BUFFER TO SMALL TO WRITE QZ");
		if(d < qxlen)
			qxs[d] = qx;
		else fprintf(stderr, "BUFFER TO SMALL TO WRITE QX");
		if(d < nlen)
			norms[d] = norm;
		else fprintf(stderr, "BUFFER TO SMALL TO WRITE NORM");
	}
}


