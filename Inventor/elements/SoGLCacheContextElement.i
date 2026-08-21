%{
static PyObject *pivy_so_gl_cache_delete_closures = NULL;

static int
pivy_so_gl_cache_delete_keep_closure(PyObject *closure)
{
  if (pivy_so_gl_cache_delete_closures == NULL) {
    pivy_so_gl_cache_delete_closures = PyList_New(0);
    if (pivy_so_gl_cache_delete_closures == NULL) {
      return -1;
    }
  }
  return PyList_Append(pivy_so_gl_cache_delete_closures, closure);
}

static void
pivy_so_gl_cache_delete_python_cb(void *userdata, uint32_t contextid)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *func = NULL;
  PyObject *user_data = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (PyTuple_Check(closure) && PyTuple_GET_SIZE(closure) == 2) {
    /* Hold the tuple while removing its owning reference from the list. */
    Py_INCREF(closure);
    if (pivy_so_gl_cache_delete_closures != NULL) {
      Py_ssize_t count = PyList_Size(pivy_so_gl_cache_delete_closures);
      for (Py_ssize_t index = 0; index < count; ++index) {
        if (PyList_GetItem(
              pivy_so_gl_cache_delete_closures,
              index) == closure) {
          PySequence_DelItem(pivy_so_gl_cache_delete_closures, index);
          break;
        }
      }
    }

    func = PyTuple_GET_ITEM(closure, 0);
    user_data = PyTuple_GET_ITEM(closure, 1);
    arglist = Py_BuildValue("(OI)", user_data, (unsigned int)contextid);
    if (arglist != NULL) {
      result = PyObject_CallObject(func, arglist);
      if (result == NULL) {
        PyErr_Print();
      }
    }
    Py_XDECREF(result);
    Py_XDECREF(arglist);
    Py_DECREF(closure);
  }

  PyGILState_Release(gil);
}
%}

%typemap(in) PyObject * callback {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject * callback {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%typemap(in) PyObject * userdata {
  $1 = $input;
}

%typemap(typecheck) PyObject * userdata {
  $1 = 1;
}

%ignore SoGLCacheContextElement::scheduleDeleteCallback;
%rename(scheduleDeleteCallback) SoGLCacheContextElement::_pivy_scheduleDeleteCallback;

%extend SoGLCacheContextElement {
  static void _pivy_scheduleDeleteCallback(
      uint32_t contextid,
      PyObject * callback,
      PyObject * userdata = NULL) {
    PyObject *closure = Py_BuildValue(
      "(OO)",
      callback,
      userdata ? userdata : Py_None);
    if (closure == NULL) {
      return;
    }

    if (pivy_so_gl_cache_delete_keep_closure(closure) < 0) {
      Py_DECREF(closure);
      return;
    }

    SoGLCacheContextElement::scheduleDeleteCallback(
      contextid,
      pivy_so_gl_cache_delete_python_cb,
      (void *)closure);
    Py_DECREF(closure);
  }
}
