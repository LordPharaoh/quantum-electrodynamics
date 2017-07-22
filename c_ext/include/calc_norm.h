#ifndef CALC_NORM_H
#define CALC_NORM_H
#include <pthread.h>
#include <complex.h>
#include "sphere.h"
void calc_norm(double middle_grid_x, double middle_grid_y, int num_middles_x, int num_middles_y, double detector_grid_x, double detector_grid_y, int num_detectors_x, int num_detectors_y, double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen, Sphere* spheres, size_t spherelen);
#endif 
