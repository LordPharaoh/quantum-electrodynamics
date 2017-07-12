%module vector 
%{

    #include "except.h"
    #include "vector.h"

%}

typedef struct {
    long double x;
    long double y;
    long double z;
} Vector;

extern Vector Vec3(long double, long double, long double);

extern Vector Vec2(long double, long double);

extern Vector v_sub(Vector, Vector);

extern Vector v_add(Vector, Vector);

extern long double v_dot(Vector, Vector);

extern Vector v_mult(Vector, long double);

extern long double v_norm(Vector);

extern long double v_slope(Vector, Vector);

extern Vector v_mid(Vector, Vector);

extern long double v_dist(Vector, Vector);

extern int v_collinear(Vector, Vector, Vector);

extern Vector v_cross(Vector, Vector);
