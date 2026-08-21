%{
static void
SoDraggerPythonCB(void * data, SoDragger * dragger)
{
  PyObject *func, *arglist;
  PyObject *result, *dragCB;

  dragCB = SWIG_NewPointerObj((void *) dragger, SWIGTYPE_p_SoDragger, 0);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("(OO)", PyTuple_GetItem((PyObject *)data, 1), dragCB);

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_DECREF(dragCB);
  Py_XDECREF(result);
}
%}

%typemap(in) PyObject *callback_data {
  if (!PyTuple_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "expected an internal callback tuple");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject *callback_data {
  $1 = PyTuple_Check($input) ? 1 : 0;
}

%rename(_pivy_addStartCallback) SoDragger::_pivy_addStartCallback;
%rename(_pivy_removeStartCallback) SoDragger::_pivy_removeStartCallback;
%rename(_pivy_addMotionCallback) SoDragger::_pivy_addMotionCallback;
%rename(_pivy_removeMotionCallback) SoDragger::_pivy_removeMotionCallback;
%rename(_pivy_addFinishCallback) SoDragger::_pivy_addFinishCallback;
%rename(_pivy_removeFinishCallback) SoDragger::_pivy_removeFinishCallback;
%rename(_pivy_addValueChangedCallback) SoDragger::_pivy_addValueChangedCallback;
%rename(_pivy_removeValueChangedCallback) SoDragger::_pivy_removeValueChangedCallback;
%rename(_pivy_addOtherEventCallback) SoDragger::_pivy_addOtherEventCallback;
%rename(_pivy_removeOtherEventCallback) SoDragger::_pivy_removeOtherEventCallback;

/* add private native adapters; Python shadows retain their callback tuples */
%extend SoDragger {
  void _pivy_addStartCallback(PyObject *callback_data) {
    self->addStartCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_removeStartCallback(PyObject *callback_data) {
    self->removeStartCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_addMotionCallback(PyObject *callback_data) {
    self->addMotionCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_removeMotionCallback(PyObject *callback_data) {
    self->removeMotionCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_addFinishCallback(PyObject *callback_data) {
    self->addFinishCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_removeFinishCallback(PyObject *callback_data) {
    self->removeFinishCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_addValueChangedCallback(PyObject *callback_data) {
    self->addValueChangedCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_removeValueChangedCallback(PyObject *callback_data) {
    self->removeValueChangedCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_addOtherEventCallback(PyObject *callback_data) {
    self->addOtherEventCallback(SoDraggerPythonCB, (void *)callback_data);
  }

  void _pivy_removeOtherEventCallback(PyObject *callback_data) {
    self->removeOtherEventCallback(SoDraggerPythonCB, (void *)callback_data);
  }
}

%feature("shadow") SoDragger::addStartCallback %{
def addStartCallback(self, pyfunc, data=None):
    if not callable(pyfunc):
        raise TypeError("need a callable object!")
    closure = (pyfunc, data)
    result = _coin.SoDragger__pivy_addStartCallback(self, closure)
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        callback_data = []
    callback_data.append(("start", closure))
    self._pivy_dragger_callback_data = callback_data
    return result
%}

%feature("shadow") SoDragger::removeStartCallback %{
def removeStartCallback(self, pyfunc, data=None):
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        return None
    for index, (kind, closure) in enumerate(callback_data):
        if kind == "start" and closure[0] is pyfunc and closure[1] is data:
            result = _coin.SoDragger__pivy_removeStartCallback(self, closure)
            del callback_data[index]
            return result
    return None
%}

%feature("shadow") SoDragger::addMotionCallback %{
def addMotionCallback(self, pyfunc, data=None):
    if not callable(pyfunc):
        raise TypeError("need a callable object!")
    closure = (pyfunc, data)
    result = _coin.SoDragger__pivy_addMotionCallback(self, closure)
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        callback_data = []
    callback_data.append(("motion", closure))
    self._pivy_dragger_callback_data = callback_data
    return result
%}

%feature("shadow") SoDragger::removeMotionCallback %{
def removeMotionCallback(self, pyfunc, data=None):
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        return None
    for index, (kind, closure) in enumerate(callback_data):
        if kind == "motion" and closure[0] is pyfunc and closure[1] is data:
            result = _coin.SoDragger__pivy_removeMotionCallback(self, closure)
            del callback_data[index]
            return result
    return None
%}

%feature("shadow") SoDragger::addFinishCallback %{
def addFinishCallback(self, pyfunc, data=None):
    if not callable(pyfunc):
        raise TypeError("need a callable object!")
    closure = (pyfunc, data)
    result = _coin.SoDragger__pivy_addFinishCallback(self, closure)
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        callback_data = []
    callback_data.append(("finish", closure))
    self._pivy_dragger_callback_data = callback_data
    return result
%}

%feature("shadow") SoDragger::removeFinishCallback %{
def removeFinishCallback(self, pyfunc, data=None):
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        return None
    for index, (kind, closure) in enumerate(callback_data):
        if kind == "finish" and closure[0] is pyfunc and closure[1] is data:
            result = _coin.SoDragger__pivy_removeFinishCallback(self, closure)
            del callback_data[index]
            return result
    return None
%}

%feature("shadow") SoDragger::addValueChangedCallback %{
def addValueChangedCallback(self, pyfunc, data=None):
    if not callable(pyfunc):
        raise TypeError("need a callable object!")
    closure = (pyfunc, data)
    result = _coin.SoDragger__pivy_addValueChangedCallback(self, closure)
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        callback_data = []
    callback_data.append(("value_changed", closure))
    self._pivy_dragger_callback_data = callback_data
    return result
%}

%feature("shadow") SoDragger::removeValueChangedCallback %{
def removeValueChangedCallback(self, pyfunc, data=None):
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        return None
    for index, (kind, closure) in enumerate(callback_data):
        if kind == "value_changed" and closure[0] is pyfunc and closure[1] is data:
            result = _coin.SoDragger__pivy_removeValueChangedCallback(self, closure)
            del callback_data[index]
            return result
    return None
%}

%feature("shadow") SoDragger::addOtherEventCallback %{
def addOtherEventCallback(self, pyfunc, data=None):
    if not callable(pyfunc):
        raise TypeError("need a callable object!")
    closure = (pyfunc, data)
    result = _coin.SoDragger__pivy_addOtherEventCallback(self, closure)
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        callback_data = []
    callback_data.append(("other_event", closure))
    self._pivy_dragger_callback_data = callback_data
    return result
%}

%feature("shadow") SoDragger::removeOtherEventCallback %{
def removeOtherEventCallback(self, pyfunc, data=None):
    callback_data = getattr(self, "_pivy_dragger_callback_data", None)
    if callback_data is None:
        return None
    for index, (kind, closure) in enumerate(callback_data):
        if kind == "other_event" and closure[0] is pyfunc and closure[1] is data:
            result = _coin.SoDragger__pivy_removeOtherEventCallback(self, closure)
            del callback_data[index]
            return result
    return None
%}
