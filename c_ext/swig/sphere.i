
%module sphere 
%include "typemaps.i"
%{
    #include "vector.h"
    #include "circle.h"
    #include "sphere.h"

%}
typedef struct {
    Vector center;
    long double radius;
    long double refrac_idx;
} Sphere;

extern Circle s_slice(Sphere, Plane);
extern Sphere s_new(Vector, double, double);
