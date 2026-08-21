%{
static PyObject *pivy_so_error_closures[4] = {NULL, NULL, NULL, NULL};

static void
pivy_so_error_python_cb(const SoError *error, void *data)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)data;
  PyObject *pyerror = SWIG_NewPointerObj((void *)error, SWIGTYPE_p_SoError, 0);
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (pyerror != NULL && PyTuple_Check(closure)) {
    arglist = Py_BuildValue("(OO)", PyTuple_GetItem(closure, 1), pyerror);
    if (arglist != NULL) {
      result = PyObject_CallObject(PyTuple_GetItem(closure, 0), arglist);
      if (result == NULL) {
        PyErr_Print();
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pyerror);
  PyGILState_Release(gil);
}

static void
pivy_set_so_error_callback(void (*setter)(SoErrorCB * const,
                                           void * const),
                           PyObject **closure_slot,
                           PyObject *pyfunc,
                           PyObject *data)
{
  PyObject *closure = Py_BuildValue("(OO)", pyfunc, data ? data : Py_None);
  if (closure == NULL) {
    return;
  }

  setter(pivy_so_error_python_cb, (void *)closure);
  Py_XDECREF(*closure_slot);
  *closure_slot = closure;
}
%}

%typemap(in) PyObject *pyfunc {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject *pyfunc {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%ignore SoError::setHandlerCallback(SoErrorCB * const func, void * const data);
%ignore SoDebugError::setHandlerCallback(SoErrorCB * const function, void * const data);
%ignore SoMemoryError::setHandlerCallback(SoErrorCB * const callback, void * const data);
%ignore SoReadError::setHandlerCallback(SoErrorCB * const function, void * const data);

%extend SoError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoError::setHandlerCallback,
                                &pivy_so_error_closures[0],
                                pyfunc, data);
  }
}

%extend SoDebugError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoDebugError::setHandlerCallback,
                                &pivy_so_error_closures[1],
                                pyfunc, data);
  }
}

%extend SoMemoryError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoMemoryError::setHandlerCallback,
                                &pivy_so_error_closures[2],
                                pyfunc, data);
  }
}

%extend SoReadError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoReadError::setHandlerCallback,
                                &pivy_so_error_closures[3],
                                pyfunc, data);
  }
}
