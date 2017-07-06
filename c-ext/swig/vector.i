%module vector 
%{

    #include "except.h"
    #include "vector.h"

%}

typedef struct {
    double x;
    double y;
    double z;
} Vector;

extern Vector Vec3(double, double, double);

extern Vector Vec2(double, double);

extern Vector v_sub(Vector, Vector);

extern Vector v_add(Vector, Vector);

extern double v_dot(Vector, Vector);

extern Vector v_mult(Vector, double);

extern double v_norm(Vector);

extern double v_slope(Vector, Vector);

extern Vector v_mid(Vector, Vector);

extern double v_dist(Vector, Vector);

extern int v_collinear(Vector, Vector, Vector);

extern Vector v_cross(Vector, Vector);
