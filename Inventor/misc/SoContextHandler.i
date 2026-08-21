%{
static PyObject *pivy_so_context_handler_closures = NULL;

static int
pivy_so_context_handler_keep_closure(PyObject *closure)
{
  if (pivy_so_context_handler_closures == NULL) {
    pivy_so_context_handler_closures = PyList_New(0);
    if (pivy_so_context_handler_closures == NULL) {
      return -1;
    }
  }
  return PyList_Append(pivy_so_context_handler_closures, closure);
}

static void
pivy_so_context_handler_python_cb(uint32_t contextid, void *userdata)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (PyTuple_Check(closure)) {
    arglist = Py_BuildValue(
      "(OI)",
      PyTuple_GetItem(closure, 1),
      (unsigned int)contextid);
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

static PyObject *
pivy_so_context_handler_find_closure(PyObject *func, PyObject *userdata)
{
  if (pivy_so_context_handler_closures == NULL) {
    return NULL;
  }

  Py_ssize_t count = PyList_Size(pivy_so_context_handler_closures);
  for (Py_ssize_t index = 0; index < count; ++index) {
    PyObject *closure = PyList_GetItem(
      pivy_so_context_handler_closures,
      index);
    if (PyTuple_Check(closure) &&
        PyTuple_GetItem(closure, 0) == func &&
        PyTuple_GetItem(closure, 1) == userdata) {
      return closure;
    }
  }
  return NULL;
}
%}

%typemap(in) PyObject * func {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject * func {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%typemap(in) PyObject * userdata {
  $1 = $input;
}

%typemap(typecheck) PyObject * userdata {
  $1 = 1;
}

%ignore SoContextHandler::addContextDestructionCallback;
%ignore SoContextHandler::removeContextDestructionCallback;
%rename(addContextDestructionCallback) SoContextHandler::_pivy_addContextDestructionCallback;
%rename(removeContextDestructionCallback) SoContextHandler::_pivy_removeContextDestructionCallback;

%extend SoContextHandler {
  static void _pivy_addContextDestructionCallback(
      PyObject * func,
      PyObject * userdata = NULL) {
    PyObject *pyclosure = Py_BuildValue(
      "(OO)",
      func,
      userdata ? userdata : Py_None);
    if (pyclosure == NULL) {
      return;
    }

    if (pivy_so_context_handler_keep_closure(pyclosure) < 0) {
      Py_DECREF(pyclosure);
      return;
    }

    SoContextHandler::addContextDestructionCallback(
      pivy_so_context_handler_python_cb,
      (void *)pyclosure);
    Py_DECREF(pyclosure);
  }

  static void _pivy_removeContextDestructionCallback(
      PyObject * func,
      PyObject * userdata = NULL) {
    userdata = userdata ? userdata : Py_None;
    PyObject *pyclosure = pivy_so_context_handler_find_closure(
      func,
      userdata);
    if (pyclosure == NULL) {
      return;
    }

    SoContextHandler::removeContextDestructionCallback(
      pivy_so_context_handler_python_cb,
      (void *)pyclosure);

    Py_ssize_t count = PyList_Size(pivy_so_context_handler_closures);
    for (Py_ssize_t index = 0; index < count; ++index) {
      if (PyList_GetItem(
            pivy_so_context_handler_closures,
            index) == pyclosure) {
        PySequence_DelItem(pivy_so_context_handler_closures, index);
        return;
      }
    }
  }
}
