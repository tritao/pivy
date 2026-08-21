%{
static void
pivy_so_shader_program_enable_python_cb(void *userdata,
                                        SoState *state,
                                        SbBool enable)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *pystate = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (PyTuple_Check(closure) && PyTuple_GET_SIZE(closure) == 2) {
    pystate = SWIG_NewPointerObj((void *)state, SWIGTYPE_p_SoState, 0);
    if (pystate != NULL) {
      arglist = Py_BuildValue(
        "(OOO)",
        PyTuple_GET_ITEM(closure, 0),
        pystate,
        enable ? Py_True : Py_False);
      if (arglist != NULL) {
        result = PyObject_CallObject(
          PyTuple_GET_ITEM(closure, 1),
          arglist);
        if (result == NULL) {
          PyErr_Print();
        }
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pystate);
  PyGILState_Release(gil);
}
%}

%typemap(in) PyObject * shader_callbackdata {
  $1 = $input;
}

%typemap(typecheck) PyObject * shader_callbackdata {
  $1 = 1;
}

%rename(_pivy_setEnableCallback) SoShaderProgram::_pivy_setEnableCallback;

%extend SoShaderProgram {
  void _pivy_setEnableCallback(PyObject * shader_callbackdata = NULL) {
    SoShaderProgramEnableCB *callback = NULL;
    void *closure = NULL;
    if (shader_callbackdata != NULL && shader_callbackdata != Py_None) {
      callback = pivy_so_shader_program_enable_python_cb;
      closure = (void *)shader_callbackdata;
    }
    self->setEnableCallback(callback, closure);
  }
}

%feature("shadow") SoShaderProgram::setEnableCallback %{
def setEnableCallback(self, cb=None, closure=None):
    if cb is not None and not callable(cb):
        raise TypeError("need a callable object!")

    callback_data = None if cb is None else (closure, cb)
    result = _coin.SoShaderProgram__pivy_setEnableCallback(
        self,
        callback_data,
    )
    self._pivy_enable_callback_data = callback_data
    return result
%}
