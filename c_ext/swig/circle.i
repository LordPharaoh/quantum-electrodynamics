
%module circle 
%include "typemaps.i"
%{
    #include "vector.h"
    #include "circle.h"

%}
typedef struct {
    Vector center;
    long double radius;
} Circle;

extern Circle c_new(Vector, long double);
extern Circle c_from_points(Vector, Vector, Vector);
extern void _c_string(char*, size_t, Circle);
extern void c_intersection(Circle, Circle, Vector* OUTPUT);
extern long double c_chord_angle(Circle, long double);
extern long double c_arc_length(Circle, Vector, Vector);
