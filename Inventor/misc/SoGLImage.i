%{
static void
pivy_so_gl_image_end_frame_python_cb(void *userdata)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (PyTuple_Check(closure) && PyTuple_GET_SIZE(closure) == 2) {
    arglist = Py_BuildValue("(O)", PyTuple_GET_ITEM(closure, 0));
    if (arglist != NULL) {
      result = PyObject_CallObject(PyTuple_GET_ITEM(closure, 1), arglist);
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

%typemap(in) PyObject * image_callbackdata {
  $1 = $input;
}

%typemap(typecheck) PyObject * image_callbackdata {
  $1 = 1;
}

%rename(_pivy_setEndFrameCallback) SoGLImage::_pivy_setEndFrameCallback;

%extend SoGLImage {
  void _pivy_setEndFrameCallback(PyObject * image_callbackdata = NULL) {
    void (*callback)(void *) = NULL;
    void *closure = NULL;
    if (image_callbackdata != NULL && image_callbackdata != Py_None) {
      callback = pivy_so_gl_image_end_frame_python_cb;
      closure = (void *)image_callbackdata;
    }
    self->setEndFrameCallback(callback, closure);
  }
}

%feature("shadow") SoGLImage::setEndFrameCallback %{
def setEndFrameCallback(self, cb=None, closure=None):
    if cb is not None and not callable(cb):
        raise TypeError("need a callable object!")

    callback_data = None if cb is None else (closure, cb)
    result = _coin.SoGLImage__pivy_setEndFrameCallback(
        self,
        callback_data,
    )
    self._pivy_end_frame_callback_data = callback_data
    return result
%}
