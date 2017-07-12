
%module calc_norm 
%include "typemaps.i"
%{
    #include "except.h"
    #include "vector.h"
    #include "circle.h"
    #include "plane.h"
    #include "sphere.h"
    #include "calc_norm.h"

%}

%typemap(in, numinputs = 1) (Sphere* spheres, size_t spherelen) {
    if (PyList_Check($input)) {
        int sizet = PyList_Size($input);
        $2 = PyList_Size($input);
        int i = 0;
        $1 = (Sphere*) malloc(sizeof(Sphere) * sizet);
        for(i = 0; i < sizet; i++) {
            PyObject *o = PyList_GetItem($input, i);
            // Since Vector overrides class this might work
            PyObject *tuple = PyList_GetItem(o, 0);
            $1[i] = s_new(Vec3(PyFloat_AsDouble(PyList_GetItem(tuple, 0)), PyFloat_AsDouble(PyList_GetItem(tuple, 1)), PyFloat_AsDouble(PyList_GetItem(tuple, 2))), PyFloat_AsDouble(PyList_GetItem(o, 1)), PyFloat_AsDouble(PyList_GetItem(o, 2)));
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError, "not a list");
    }
}

%typemap(in, numinputs = 1) (int num_detectors_x, int num_detectors_y, double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen) {
    PyObject* siz = $input;
    
    int lenth = (int) (PyInt_AsLong(PyTuple_GetItem(siz, 0)) * PyInt_AsLong(PyTuple_GetItem(siz, 1)));
    $5 = (double*) malloc(sizeof(double) * lenth);
    $6 = lenth;
    $7 = (double*) malloc(sizeof(double) * lenth);
    $8 = lenth;
    $3 = (double*) malloc(sizeof(double) * lenth);
    $4 = lenth;
    $1 = (int) PyInt_AsLong(PyTuple_GetItem(siz, 0));
    $2 = (int) PyInt_AsLong(PyTuple_GetItem(siz, 1));
}

%typemap(in, numinputs=1) (int num_middles_x, int num_middles_y) {
    $1 = (int) PyInt_AsLong(PyTuple_GetItem($input, 0));
    $2 = (int) PyInt_AsLong(PyTuple_GetItem($input, 1));
}

%typemap(in, numinputs=1) (double grid_x, double grid_y) {
    $1 = PyFloat_AsDouble(PyTuple_GetItem($input, 0));
    $2 = PyFloat_AsDouble(PyTuple_GetItem($input, 1));
}

%typemap(freearg) (Sphere* spheres, size_t spherelen){
    free((Sphere*) $1);
}

%typemap(freearg) (double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen){
    free($1);
    free($3);
    free($5);
}

%typemap(argout) (double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen) {

    PyObject* qz = PyList_New($2);
    PyObject* qx = PyList_New($4);
    PyObject* norms = PyList_New($6);

    for(int i = 0; i < $2; i++) {
        PyList_SetItem(qz, i, PyFloat_FromDouble($1[i]));
        PyList_SetItem(qx, i, PyFloat_FromDouble($3[i]));
        PyList_SetItem(norms, i, PyFloat_FromDouble($5[i]));
    }
    $result = PyTuple_New(3);
    PyTuple_SetItem($result, 0, norms);
    PyTuple_SetItem($result, 1, qz);
    PyTuple_SetItem($result, 2, qx);
}

void calc_norm(double grid_x, double grid_y, int num_middles_x, int num_middles_y, double grid_x, double grid_y, int num_detectors_x, int num_detectors_y, double* qzs, size_t qzlen, double* qxs, size_t qxlen, double* norms, size_t nlen, Sphere* spheres, size_t spherelen);

