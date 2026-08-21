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

static PyObject *
pivy_get_so_error_python_callback(SoErrorCB *callback, PyObject *closure)
{
  if (callback == pivy_so_error_python_cb &&
      closure != NULL &&
      PyTuple_Check(closure) &&
      PyTuple_GET_SIZE(closure) == 2) {
    PyObject *pyfunc = PyTuple_GET_ITEM(closure, 0);
    Py_INCREF(pyfunc);
    return pyfunc;
  }
  Py_RETURN_NONE;
}

static PyObject *
pivy_get_so_error_python_data(void *data, PyObject *closure)
{
  if (closure != NULL && data == (void *)closure &&
      PyTuple_Check(closure) &&
      PyTuple_GET_SIZE(closure) == 2) {
    PyObject *pydata = PyTuple_GET_ITEM(closure, 1);
    Py_INCREF(pydata);
    return pydata;
  }
  Py_RETURN_NONE;
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

%ignore SoError::getHandlerCallback();
%ignore SoError::getHandlerData();
%ignore SoDebugError::getHandlerCallback();
%ignore SoDebugError::getHandlerData();
%ignore SoMemoryError::getHandlerCallback();
%ignore SoMemoryError::getHandlerData();
%ignore SoReadError::getHandlerCallback();
%ignore SoReadError::getHandlerData();

%rename(getHandlerCallback) SoError::_pivy_getHandlerCallback;
%rename(getHandlerData) SoError::_pivy_getHandlerData;
%rename(getHandlerCallback) SoDebugError::_pivy_getHandlerCallback;
%rename(getHandlerData) SoDebugError::_pivy_getHandlerData;
%rename(getHandlerCallback) SoMemoryError::_pivy_getHandlerCallback;
%rename(getHandlerData) SoMemoryError::_pivy_getHandlerData;
%rename(getHandlerCallback) SoReadError::_pivy_getHandlerCallback;
%rename(getHandlerData) SoReadError::_pivy_getHandlerData;

%extend SoError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoError::setHandlerCallback,
                                &pivy_so_error_closures[0],
                                pyfunc, data);
  }

  static PyObject *_pivy_getHandlerCallback() {
    return pivy_get_so_error_python_callback(
      SoError::getHandlerCallback(), pivy_so_error_closures[0]);
  }

  static PyObject *_pivy_getHandlerData() {
    return pivy_get_so_error_python_data(
      SoError::getHandlerData(), pivy_so_error_closures[0]);
  }
}

%extend SoDebugError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoDebugError::setHandlerCallback,
                                &pivy_so_error_closures[1],
                                pyfunc, data);
  }

  static PyObject *_pivy_getHandlerCallback() {
    return pivy_get_so_error_python_callback(
      SoDebugError::getHandlerCallback(), pivy_so_error_closures[1]);
  }

  static PyObject *_pivy_getHandlerData() {
    return pivy_get_so_error_python_data(
      SoDebugError::getHandlerData(), pivy_so_error_closures[1]);
  }
}

%extend SoMemoryError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoMemoryError::setHandlerCallback,
                                &pivy_so_error_closures[2],
                                pyfunc, data);
  }

  static PyObject *_pivy_getHandlerCallback() {
    return pivy_get_so_error_python_callback(
      SoMemoryError::getHandlerCallback(), pivy_so_error_closures[2]);
  }

  static PyObject *_pivy_getHandlerData() {
    return pivy_get_so_error_python_data(
      SoMemoryError::getHandlerData(), pivy_so_error_closures[2]);
  }
}

%extend SoReadError {
  static void setHandlerCallback(PyObject *pyfunc, PyObject *data) {
    pivy_set_so_error_callback(SoReadError::setHandlerCallback,
                                &pivy_so_error_closures[3],
                                pyfunc, data);
  }

  static PyObject *_pivy_getHandlerCallback() {
    return pivy_get_so_error_python_callback(
      SoReadError::getHandlerCallback(), pivy_so_error_closures[3]);
  }

  static PyObject *_pivy_getHandlerData() {
    return pivy_get_so_error_python_data(
      SoReadError::getHandlerData(), pivy_so_error_closures[3]);
  }
}
