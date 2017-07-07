
%module calc_norm 
%include "typemaps.i"
%{
    #include "except.h"
    #include "vector.h"
    #include "circle.h"
    #include "plane.h"
    #include "calc_norm.h"

%}

%typemap(in) (Vector* list_in, size_t size_in) {
    if (PyList_Check($input)) {
        int sizet = PyList_Size($input);
        $2 = PyList_Size($input);
        int i = 0;
        $1 = (Vector*) malloc(sizeof(Vector) * sizet);
        for(i = 0; i < sizet; i++) {
            PyObject *o = PyList_GetItem($input, i);
            // Since Vector overrides class this might work
            $1[i] = Vec3(PyFloat_AsDouble(PyList_GetItem(o, 0)), PyFloat_AsDouble(PyList_GetItem(o, 1)), PyFloat_AsDouble(PyList_GetItem(o, 2)));
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError, "not a list");
    }
}

%typemap(in) (Vector* list_innout, size_t size_innout, double* qs, size_t qlen, double* norms, size_t nlen) {
    if (PyList_Check($input)) {

        int sizet = PyList_Size($input);
        $2 = PyList_Size($input);

        $3 = (double*) malloc(sizeof(double) * sizet);
        $4 = sizet;
        $5 = (double*) malloc(sizeof(double) * sizet);
        $6 = sizet;
        $1 = (Vector*) malloc(sizeof(Vector) * sizet);

        int i = 0;
        for(i = 0; i < sizet; i++) {
            PyObject *o = PyList_GetItem($input, i);
            $1[i] = Vec3(PyFloat_AsDouble(PyList_GetItem(o, 0)), PyFloat_AsDouble(PyList_GetItem(o, 1)), PyFloat_AsDouble(PyList_GetItem(o, 2)));
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError, "not a list");
    }
}

%typemap(freearg) (Vector* list_in, size_t size_in){
    free((Vector*) $1);
}

%typemap(freearg) (Vector* list_innout, size_t size_innout, double* qs, size_t qlen, double* norms, size_t nlen){
    free($1);
    free($3);
    free($5);
}

%typemap(argout) (double* qs, size_t qlen, double* norms, size_t nlen) {

    PyObject* q = PyList_New($2);
    PyObject* norm = PyList_New($4);

    for(int i = 0; i < $2; i++) {
        PyList_SetItem(q, i, PyFloat_FromDouble($1[i]));
        PyList_SetItem(norm, i, PyFloat_FromDouble($3[i]));
    }
    $result = PyTuple_New(2);
    PyTuple_SetItem($result, 1, q);
    PyTuple_SetItem($result, 0, norm);
}

void calc_norm(Vector* list_in, size_t size_in, Vector* list_in, size_t size_in, Vector* list_innout, size_t size_innout, double* qs, size_t qlen, double* norms, size_t nlen, double sphere_radius, double ref_index);

