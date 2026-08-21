%{
static void
SoSelectionPathPythonCB(void * data, SoPath * path)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *func, *arglist;
  PyObject *result, *pathCB;

  pathCB = SWIG_NewPointerObj((void *) path, SWIGTYPE_p_SoPath, 0);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("(OO)", PyTuple_GetItem((PyObject *)data, 1), pathCB);

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_DECREF(pathCB);
  Py_XDECREF(result);
  PyGILState_Release(gil);
}

static void
SoSelectionClassPythonCB(void * data, SoSelection * sel)
{
  PyObject *func, *arglist;
  PyObject *result, *selCB;

  selCB = SWIG_NewPointerObj((void *) sel, SWIGTYPE_p_SoSelection, 0);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), selCB);

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_DECREF(selCB);
  Py_XDECREF(result);
}

static SoPath *
SoSelectionPickPythonCB(void * data, const SoPickedPoint * pick)
{
  PyObject *func, *arglist;
  PyObject *result, *pickCB;
  SoPath *resultobj;

  pickCB = SWIG_NewPointerObj((void *) pick, SWIGTYPE_p_SoPickedPoint, 0);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), pickCB);

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }
  else {
    SWIG_ConvertPtr(result, (void **) &resultobj, SWIGTYPE_p_SoPath, 1);
  }

  Py_DECREF(arglist);
  Py_DECREF(pickCB);
  Py_XDECREF(result);

  return resultobj;
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

%rename(_pivy_addSelectionCallback) SoSelection::_pivy_addSelectionCallback;
%rename(_pivy_removeSelectionCallback) SoSelection::_pivy_removeSelectionCallback;
%rename(_pivy_addDeselectionCallback) SoSelection::_pivy_addDeselectionCallback;
%rename(_pivy_removeDeselectionCallback) SoSelection::_pivy_removeDeselectionCallback;
%rename(_pivy_addStartCallback) SoSelection::_pivy_addStartCallback;
%rename(_pivy_removeStartCallback) SoSelection::_pivy_removeStartCallback;
%rename(_pivy_addFinishCallback) SoSelection::_pivy_addFinishCallback;
%rename(_pivy_removeFinishCallback) SoSelection::_pivy_removeFinishCallback;
%rename(_pivy_setPickFilterCallback) SoSelection::_pivy_setPickFilterCallback;
%rename(_pivy_addChangeCallback) SoSelection::_pivy_addChangeCallback;
%rename(_pivy_removeChangeCallback) SoSelection::_pivy_removeChangeCallback;

/* add private native adapters; Python shadows retain their callback tuples */
%extend SoSelection {
  void _pivy_addSelectionCallback(PyObject *callback_data) {
    self->addSelectionCallback(SoSelectionPathPythonCB, (void *)callback_data);
  }

  void _pivy_removeSelectionCallback(PyObject *callback_data) {
    self->removeSelectionCallback(SoSelectionPathPythonCB, (void *)callback_data);
  }

  void _pivy_addDeselectionCallback(PyObject *callback_data) {
    self->addDeselectionCallback(SoSelectionPathPythonCB, (void *)callback_data);
  }

  void _pivy_removeDeselectionCallback(PyObject *callback_data) {
    self->removeDeselectionCallback(SoSelectionPathPythonCB, (void *)callback_data);
  }

  void _pivy_addStartCallback(PyObject *callback_data) {
    self->addStartCallback(SoSelectionClassPythonCB, (void *)callback_data);
  }

  void _pivy_removeStartCallback(PyObject *callback_data) {
    self->removeStartCallback(SoSelectionClassPythonCB, (void *)callback_data);
  }

  void _pivy_addFinishCallback(PyObject *callback_data) {
    self->addFinishCallback(SoSelectionClassPythonCB, (void *)callback_data);
  }

  void _pivy_removeFinishCallback(PyObject *callback_data) {
    self->removeFinishCallback(SoSelectionClassPythonCB, (void *)callback_data);
  }

  void _pivy_setPickFilterCallback(
      PyObject *callback_data,
      int callOnlyIfSelectable = 1) {
    self->setPickFilterCallback(
      SoSelectionPickPythonCB,
      (void *)callback_data,
      callOnlyIfSelectable);
  }

  void _pivy_addChangeCallback(PyObject *callback_data) {
    self->addChangeCallback(SoSelectionClassPythonCB, (void *)callback_data);
  }

  void _pivy_removeChangeCallback(PyObject *callback_data) {
    self->removeChangeCallback(SoSelectionClassPythonCB, (void *)callback_data);
  }

%pythoncode %{
  def _pivy_add_callback(self, kind, native_callback, pyfunc, userdata):
    if not callable(pyfunc):
      raise TypeError("need a callable object!")
    closure = (pyfunc, userdata)
    result = native_callback(self, closure)
    callback_data = getattr(self, "_pivy_selection_callback_data", None)
    if callback_data is None:
      callback_data = []
    callback_data.append((kind, closure))
    self._pivy_selection_callback_data = callback_data
    return result

  def _pivy_remove_callback(self, kind, native_callback, pyfunc, userdata):
    callback_data = getattr(self, "_pivy_selection_callback_data", None)
    if callback_data is None:
      return None
    for index, (callback_kind, closure) in enumerate(callback_data):
      if (
        callback_kind == kind
        and closure[0] is pyfunc
        and closure[1] is userdata
      ):
        result = native_callback(self, closure)
        del callback_data[index]
        return result
    return None
%}
}

%feature("shadow") SoSelection::addSelectionCallback %{
def addSelectionCallback(self, pyfunc, userdata=None):
    return self._pivy_add_callback(
        "selection",
        _coin.SoSelection__pivy_addSelectionCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::removeSelectionCallback %{
def removeSelectionCallback(self, pyfunc, userdata=None):
    return self._pivy_remove_callback(
        "selection",
        _coin.SoSelection__pivy_removeSelectionCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::addDeselectionCallback %{
def addDeselectionCallback(self, pyfunc, userdata=None):
    return self._pivy_add_callback(
        "deselection",
        _coin.SoSelection__pivy_addDeselectionCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::removeDeselectionCallback %{
def removeDeselectionCallback(self, pyfunc, userdata=None):
    return self._pivy_remove_callback(
        "deselection",
        _coin.SoSelection__pivy_removeDeselectionCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::addStartCallback %{
def addStartCallback(self, pyfunc, userdata=None):
    return self._pivy_add_callback(
        "start",
        _coin.SoSelection__pivy_addStartCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::removeStartCallback %{
def removeStartCallback(self, pyfunc, userdata=None):
    return self._pivy_remove_callback(
        "start",
        _coin.SoSelection__pivy_removeStartCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::addFinishCallback %{
def addFinishCallback(self, pyfunc, userdata=None):
    return self._pivy_add_callback(
        "finish",
        _coin.SoSelection__pivy_addFinishCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::removeFinishCallback %{
def removeFinishCallback(self, pyfunc, userdata=None):
    return self._pivy_remove_callback(
        "finish",
        _coin.SoSelection__pivy_removeFinishCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::setPickFilterCallback %{
def setPickFilterCallback(self, pyfunc, userdata=None, callOnlyIfSelectable=1):
    if not callable(pyfunc):
        raise TypeError("need a callable object!")
    closure = (pyfunc, userdata)
    result = _coin.SoSelection__pivy_setPickFilterCallback(
        self,
        closure,
        callOnlyIfSelectable,
    )
    self._pivy_selection_pick_filter_callback_data = closure
    return result
%}

%feature("shadow") SoSelection::addChangeCallback %{
def addChangeCallback(self, pyfunc, userdata=None):
    return self._pivy_add_callback(
        "change",
        _coin.SoSelection__pivy_addChangeCallback,
        pyfunc,
        userdata,
    )
%}

%feature("shadow") SoSelection::removeChangeCallback %{
def removeChangeCallback(self, pyfunc, userdata=None):
    return self._pivy_remove_callback(
        "change",
        _coin.SoSelection__pivy_removeChangeCallback,
        pyfunc,
        userdata,
    )
%}
