%{
static void
SoGLRenderPassPythonCB(void * userdata)
{
  PyObject *func, *arglist;
  PyObject *result;

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("O", PyTuple_GetItem((PyObject *)userdata, 1));

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);
}

static SoGLRenderAction::AbortCode
SoGLRenderAbortPythonCB(void * userdata)
{
  PyObject *func, *arglist;
  PyObject *result;
  SoGLRenderAction::AbortCode res;

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("O", PyTuple_GetItem((PyObject *)userdata, 1));

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  res = (SoGLRenderAction::AbortCode)PyInt_AsLong(result);

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return res;
}

static void
SoGLPreRenderPythonCB(void * userdata, class SoGLRenderAction * action)
{
  PyObject *func, *arglist;
  PyObject *result, *acCB;

  acCB = SWIG_NewPointerObj((void *) action, SWIGTYPE_p_SoGLRenderAction, 1);

  /* the first item in the userdata sequence is the python callback
   * function; the second is the supplied userdata python object */
  func = PyTuple_GetItem((PyObject *)userdata, 0);
  arglist = Py_BuildValue("(OO)", PyTuple_GetItem((PyObject *)userdata, 1), acCB);

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_DECREF(acCB);
  Py_XDECREF(result);
}

static float
SoGLSortedObjectOrderPythonCB(void * userdata,
                              class SoGLRenderAction * action)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *pyaction = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;
  float order = 0.0f;

  if (PyTuple_Check(closure)) {
    pyaction = SWIG_NewPointerObj(
      (void *)action,
      SWIGTYPE_p_SoGLRenderAction,
      0);
    if (pyaction != NULL) {
      arglist = Py_BuildValue(
        "(OO)",
        PyTuple_GetItem(closure, 0),
        pyaction);
      if (arglist != NULL) {
        result = PyObject_CallObject(
          PyTuple_GetItem(closure, 1),
          arglist);
        if (result == NULL) {
          PyErr_Print();
        } else {
          order = (float)PyFloat_AsDouble(result);
          if (PyErr_Occurred()) {
            PyErr_Print();
            order = 0.0f;
          }
        }
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pyaction);
  PyGILState_Release(gil);
  return order;
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

%typemap(in) PyObject * callbackdata {
  $1 = $input;
}

%typemap(typecheck) PyObject * callbackdata {
  $1 = 1;
}

/* add python specific callback functions */
%extend SoGLRenderAction {
  void setPassCallback(PyObject *pyfunc, PyObject * userdata){
    self->setPassCallback(SoGLRenderPassPythonCB,
                          (void *)Py_BuildValue("(OO)",
                                                pyfunc,
                                                userdata ? userdata : Py_None));
  }

  void setAbortCallback(PyObject *pyfunc, PyObject * userdata){
    self->setAbortCallback(SoGLRenderAbortPythonCB,
                           (void *)Py_BuildValue("(OO)",
                                                 pyfunc,
                                                 userdata ? userdata : Py_None));
  }
  
  void addPreRenderCallback(PyObject *pyfunc, PyObject * userdata) {
    self->addPreRenderCallback(SoGLPreRenderPythonCB,
                               (void *)Py_BuildValue("(OO)",
                                                     pyfunc,
                                                     userdata ? userdata : Py_None));
  }

  void removePreRenderCallback(PyObject *pyfunc, PyObject * userdata) {
    self->removePreRenderCallback(SoGLPreRenderPythonCB,
                                  (void *)Py_BuildValue("(OO)",
                                                        pyfunc,
                                                        userdata ? userdata : Py_None));
  }

  void _pivy_setSortedObjectOrderStrategy(
      int strategy,
      PyObject * callbackdata = NULL) {
    SoGLSortedObjectOrderCB *callback = NULL;
    void *closure = NULL;
    if (callbackdata != NULL && callbackdata != Py_None) {
      callback = SoGLSortedObjectOrderPythonCB;
      closure = (void *)callbackdata;
    }
    self->setSortedObjectOrderStrategy(
      (SoGLRenderAction::SortedObjectOrderStrategy)strategy,
      callback,
      closure);
  }
}

%feature("shadow") SoGLRenderAction::setSortedObjectOrderStrategy %{
def setSortedObjectOrderStrategy(self, strategy, cb=None, closure=None):
    if cb is not None and not callable(cb):
        raise TypeError("need a callable object!")

    callback_data = None if cb is None else (closure, cb)
    result = _coin.SoGLRenderAction__pivy_setSortedObjectOrderStrategy(
        self,
        strategy,
        callback_data,
    )
    self._pivy_sorted_object_order_callback_data = callback_data
    return result
%}

%extend SoGLRenderAction{
  static SoGLRenderAction* constructFromAction(SoAction* action)
  {
    return (SoGLRenderAction*) action;
  }
}
