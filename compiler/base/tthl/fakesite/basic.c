#include <Python.h>
#define DLLEXP export "C" __declspec(DLLEXPORT)

static PyMethodDef Methods[] = {
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init*(void) {
    Py_InitModule("*", Methods);
};
