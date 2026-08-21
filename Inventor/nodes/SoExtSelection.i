%{
static SoPath *
pivy_so_extselection_lasso_cb(void * userdata, const SoPath * path)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *path_obj = NULL;
  PyObject *args = NULL;
  PyObject *result = NULL;
  SoPath *result_path = NULL;

  path_obj = SWIG_NewPointerObj((void *)path, SWIGTYPE_p_SoPath, 0);
  if (path_obj != NULL) {
    args = Py_BuildValue("(OO)", PyTuple_GET_ITEM(closure, 1), path_obj);
  }
  if (args != NULL) {
    result = PyObject_CallObject(PyTuple_GET_ITEM(closure, 0), args);
    if (result == NULL) {
      PyErr_Print();
    }
    else if (result != Py_None) {
      SWIG_ConvertPtr(result, (void **)&result_path, SWIGTYPE_p_SoPath, 1);
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(args);
  Py_XDECREF(path_obj);
  PyGILState_Release(gil);
  return result_path;
}

static SbBool
pivy_so_extselection_triangle_cb(void * userdata,
                                 SoCallbackAction * action,
                                 const SoPrimitiveVertex * v1,
                                 const SoPrimitiveVertex * v2,
                                 const SoPrimitiveVertex * v3)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *action_obj = NULL;
  PyObject *vertex1 = NULL;
  PyObject *vertex2 = NULL;
  PyObject *vertex3 = NULL;
  PyObject *args = NULL;
  PyObject *result = NULL;
  int accepted = 0;

  action_obj = SWIG_NewPointerObj((void *)action, SWIGTYPE_p_SoCallbackAction, 0);
  vertex1 = SWIG_NewPointerObj((void *)v1, SWIGTYPE_p_SoPrimitiveVertex, 0);
  vertex2 = SWIG_NewPointerObj((void *)v2, SWIGTYPE_p_SoPrimitiveVertex, 0);
  vertex3 = SWIG_NewPointerObj((void *)v3, SWIGTYPE_p_SoPrimitiveVertex, 0);
  if (action_obj != NULL && vertex1 != NULL && vertex2 != NULL && vertex3 != NULL) {
    args = Py_BuildValue(
      "(OOOOO)",
      PyTuple_GET_ITEM(closure, 1),
      action_obj,
      vertex1,
      vertex2,
      vertex3);
  }
  if (args != NULL) {
    result = PyObject_CallObject(PyTuple_GET_ITEM(closure, 0), args);
    if (result == NULL) {
      PyErr_Print();
    }
    else {
      accepted = PyObject_IsTrue(result);
      if (accepted < 0) {
        PyErr_Print();
        accepted = 0;
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(args);
  Py_XDECREF(vertex3);
  Py_XDECREF(vertex2);
  Py_XDECREF(vertex1);
  Py_XDECREF(action_obj);
  PyGILState_Release(gil);
  return accepted ? TRUE : FALSE;
}

static SbBool
pivy_so_extselection_line_segment_cb(void * userdata,
                                     SoCallbackAction * action,
                                     const SoPrimitiveVertex * v1,
                                     const SoPrimitiveVertex * v2)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *action_obj = NULL;
  PyObject *vertex1 = NULL;
  PyObject *vertex2 = NULL;
  PyObject *args = NULL;
  PyObject *result = NULL;
  int accepted = 0;

  action_obj = SWIG_NewPointerObj((void *)action, SWIGTYPE_p_SoCallbackAction, 0);
  vertex1 = SWIG_NewPointerObj((void *)v1, SWIGTYPE_p_SoPrimitiveVertex, 0);
  vertex2 = SWIG_NewPointerObj((void *)v2, SWIGTYPE_p_SoPrimitiveVertex, 0);
  if (action_obj != NULL && vertex1 != NULL && vertex2 != NULL) {
    args = Py_BuildValue(
      "(OOOO)",
      PyTuple_GET_ITEM(closure, 1),
      action_obj,
      vertex1,
      vertex2);
  }
  if (args != NULL) {
    result = PyObject_CallObject(PyTuple_GET_ITEM(closure, 0), args);
    if (result == NULL) {
      PyErr_Print();
    }
    else {
      accepted = PyObject_IsTrue(result);
      if (accepted < 0) {
        PyErr_Print();
        accepted = 0;
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(args);
  Py_XDECREF(vertex2);
  Py_XDECREF(vertex1);
  Py_XDECREF(action_obj);
  PyGILState_Release(gil);
  return accepted ? TRUE : FALSE;
}

static SbBool
pivy_so_extselection_point_cb(void * userdata,
                              SoCallbackAction * action,
                              const SoPrimitiveVertex * vertex)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *action_obj = NULL;
  PyObject *vertex_obj = NULL;
  PyObject *args = NULL;
  PyObject *result = NULL;
  int accepted = 0;

  action_obj = SWIG_NewPointerObj((void *)action, SWIGTYPE_p_SoCallbackAction, 0);
  vertex_obj = SWIG_NewPointerObj((void *)vertex, SWIGTYPE_p_SoPrimitiveVertex, 0);
  if (action_obj != NULL && vertex_obj != NULL) {
    args = Py_BuildValue(
      "(OOO)",
      PyTuple_GET_ITEM(closure, 1),
      action_obj,
      vertex_obj);
  }
  if (args != NULL) {
    result = PyObject_CallObject(PyTuple_GET_ITEM(closure, 0), args);
    if (result == NULL) {
      PyErr_Print();
    }
    else {
      accepted = PyObject_IsTrue(result);
      if (accepted < 0) {
        PyErr_Print();
        accepted = 0;
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(args);
  Py_XDECREF(vertex_obj);
  Py_XDECREF(action_obj);
  PyGILState_Release(gil);
  return accepted ? TRUE : FALSE;
}
%}

%typemap(in) PyObject *ext_callback_data {
  if ($input == Py_None) {
    $1 = Py_None;
  }
  else if (!PyTuple_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "expected an internal callback tuple");
    return NULL;
  }
  else {
    $1 = $input;
  }
}

%typemap(typecheck) PyObject *ext_callback_data {
  $1 = ($input == Py_None || PyTuple_Check($input)) ? 1 : 0;
}

%rename(_pivy_setLassoFilterCallback) SoExtSelection::_pivy_setLassoFilterCallback;
%rename(_pivy_setTriangleFilterCallback) SoExtSelection::_pivy_setTriangleFilterCallback;
%rename(_pivy_setLineSegmentFilterCallback) SoExtSelection::_pivy_setLineSegmentFilterCallback;
%rename(_pivy_setPointFilterCallback) SoExtSelection::_pivy_setPointFilterCallback;

%extend SoExtSelection {
  void _pivy_setLassoFilterCallback(
      PyObject *ext_callback_data,
      int callonlyifselectable = 1) {
    if (ext_callback_data == Py_None) {
      self->setLassoFilterCallback(NULL, NULL, callonlyifselectable);
    }
    else {
      self->setLassoFilterCallback(
        pivy_so_extselection_lasso_cb,
        (void *)ext_callback_data,
        callonlyifselectable);
    }
  }

  void _pivy_setTriangleFilterCallback(PyObject *ext_callback_data) {
    if (ext_callback_data == Py_None) {
      self->setTriangleFilterCallback(NULL, NULL);
    }
    else {
      self->setTriangleFilterCallback(
        pivy_so_extselection_triangle_cb,
        (void *)ext_callback_data);
    }
  }

  void _pivy_setLineSegmentFilterCallback(PyObject *ext_callback_data) {
    if (ext_callback_data == Py_None) {
      self->setLineSegmentFilterCallback(NULL, NULL);
    }
    else {
      self->setLineSegmentFilterCallback(
        pivy_so_extselection_line_segment_cb,
        (void *)ext_callback_data);
    }
  }

  void _pivy_setPointFilterCallback(PyObject *ext_callback_data) {
    if (ext_callback_data == Py_None) {
      self->setPointFilterCallback(NULL, NULL);
    }
    else {
      self->setPointFilterCallback(
        pivy_so_extselection_point_cb,
        (void *)ext_callback_data);
    }
  }
}

%feature("shadow") SoExtSelection::setLassoFilterCallback %{
def setLassoFilterCallback(self, f, userdata=None, callonlyifselectable=True):
    if f is not None and not callable(f):
        raise TypeError("need a callable object!")
    callback_data = None if f is None else (f, userdata)
    result = _coin.SoExtSelection__pivy_setLassoFilterCallback(
        self,
        callback_data,
        callonlyifselectable,
    )
    self._pivy_lasso_filter_callback_data = callback_data
    return result
%}

%feature("shadow") SoExtSelection::setTriangleFilterCallback %{
def setTriangleFilterCallback(self, func, userdata=None):
    if func is not None and not callable(func):
        raise TypeError("need a callable object!")
    callback_data = None if func is None else (func, userdata)
    result = _coin.SoExtSelection__pivy_setTriangleFilterCallback(
        self,
        callback_data,
    )
    self._pivy_triangle_filter_callback_data = callback_data
    return result
%}

%feature("shadow") SoExtSelection::setLineSegmentFilterCallback %{
def setLineSegmentFilterCallback(self, func, userdata=None):
    if func is not None and not callable(func):
        raise TypeError("need a callable object!")
    callback_data = None if func is None else (func, userdata)
    result = _coin.SoExtSelection__pivy_setLineSegmentFilterCallback(
        self,
        callback_data,
    )
    self._pivy_line_segment_filter_callback_data = callback_data
    return result
%}

%feature("shadow") SoExtSelection::setPointFilterCallback %{
def setPointFilterCallback(self, func, userdata=None):
    if func is not None and not callable(func):
        raise TypeError("need a callable object!")
    callback_data = None if func is None else (func, userdata)
    result = _coin.SoExtSelection__pivy_setPointFilterCallback(
        self,
        callback_data,
    )
    self._pivy_point_filter_callback_data = callback_data
    return result
%}
