#ifndef CALC_NORM_H
#define CALC_NORM_H
#include <complex.h>
void calc_norm(Vector* emitter, size_t elen, Vector* middle, size_t mlen, Vector* detector, size_t dlen, double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen, double sphere_radius, double ref_index);
#endif 
