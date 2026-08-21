%{
static void
pivy_so_callback_list_python_cb(void * userdata, void * callbackdata)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *pycallbackdata = callbackdata ? (PyObject *)callbackdata : Py_None;
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (PyTuple_Check(closure)) {
    arglist = Py_BuildValue(
      "(OO)",
      PyTuple_GetItem(closure, 1),
      pycallbackdata);
    if (arglist != NULL) {
      result = PyObject_CallObject(PyTuple_GetItem(closure, 0), arglist);
      if (result == NULL) {
        PyErr_Print();
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  PyGILState_Release(gil);
}
%}

%typemap(in) PyObject * closure {
  $1 = $input;
}

%typemap(typecheck) PyObject * closure {
  $1 = 1;
}

%typemap(in) PyObject * callbackdata {
  $1 = $input;
}

%typemap(typecheck) PyObject * callbackdata {
  $1 = 1;
}

%extend SoCallbackList {
  void _pivy_addCallback(PyObject * closure) {
    self->addCallback(
      pivy_so_callback_list_python_cb,
      (void *)closure);
  }

  void _pivy_removeCallback(PyObject * closure) {
    self->removeCallback(
      pivy_so_callback_list_python_cb,
      (void *)closure);
  }

  void _pivy_clearCallbacks() {
    self->clearCallbacks();
  }

  void _pivy_invokeCallbacks(PyObject * callbackdata) {
    self->invokeCallbacks((void *)callbackdata);
  }
}

%feature("shadow") SoCallbackList::addCallback %{
def addCallback(self, f, userData=None):
    if not callable(f):
        raise TypeError("need a callable object!")

    callback_data = getattr(self, "_pivy_callback_data", None)
    if callback_data is None:
        callback_data = []
    closure = (f, userData)
    result = _coin.SoCallbackList__pivy_addCallback(self, closure)
    callback_data.append(closure)
    self._pivy_callback_data = callback_data
    return result
%}

%feature("shadow") SoCallbackList::removeCallback %{
def removeCallback(self, f, userdata=None):
    callback_data = getattr(self, "_pivy_callback_data", None)
    if callback_data is None:
        return None

    for index, closure in enumerate(callback_data):
        if closure[0] is f and closure[1] is userdata:
            result = _coin.SoCallbackList__pivy_removeCallback(self, closure)
            del callback_data[index]
            return result
    return None
%}

%feature("shadow") SoCallbackList::clearCallbacks %{
def clearCallbacks(self):
    result = _coin.SoCallbackList__pivy_clearCallbacks(self)
    self._pivy_callback_data = []
    return result
%}

%feature("shadow") SoCallbackList::invokeCallbacks %{
def invokeCallbacks(self, callbackdata):
    return _coin.SoCallbackList__pivy_invokeCallbacks(self, callbackdata)
%}
