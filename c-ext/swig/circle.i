
%module circle 
%include "typemaps.i"
%{
    #include "vector.h"
    #include "circle.h"

%}
typedef struct {
    Vector center;
    double radius;
} Circle;

extern Circle c_from_points(Vector, Vector, Vector);
extern void _c_string(char*, size_t, Circle);
extern void c_intersection(Circle, Circle, Vector* OUTPUT);
extern double c_arc_length(Circle, Vector, Vector);
