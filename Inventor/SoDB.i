%{
static PyObject *pivy_sodb_header_closures = NULL;
static PyObject *pivy_sodb_progress_closures = NULL;

static int
pivy_sodb_keep_closure(PyObject **closures, PyObject *closure)
{
  if (*closures == NULL) {
    *closures = PyList_New(0);
    if (*closures == NULL) {
      return -1;
    }
  }
  return PyList_Append(*closures, closure);
}

static void
pivy_sodb_header_python_cb(void * data, SoInput * input, Py_ssize_t callback_index)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)data;
  PyObject *pyinput = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;

  if (PyTuple_Check(closure)) {
    pyinput = SWIG_NewPointerObj((void *)input, SWIGTYPE_p_SoInput, 0);
    if (pyinput != NULL) {
      arglist = Py_BuildValue(
        "(OO)",
        PyTuple_GetItem(closure, 2),
        pyinput);
      if (arglist != NULL) {
        result = PyObject_CallObject(
          PyTuple_GetItem(closure, callback_index),
          arglist);
        if (result == NULL) {
          PyErr_Print();
        }
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pyinput);
  PyGILState_Release(gil);
}

static void
pivy_sodb_header_pre_python_cb(void * data, SoInput * input)
{
  pivy_sodb_header_python_cb(data, input, 0);
}

static void
pivy_sodb_header_post_python_cb(void * data, SoInput * input)
{
  pivy_sodb_header_python_cb(data, input, 1);
}

static SbBool
pivy_sodb_progress_python_cb(const SbName & itemid,
                             float fraction,
                             SbBool interruptible,
                             void * data)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)data;
  PyObject *pyitemid = NULL;
  SbName *itemid_copy = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;
  SbBool callback_result = FALSE;

  if (PyTuple_Check(closure)) {
    itemid_copy = new SbName(itemid);
    pyitemid = SWIG_NewPointerObj(
      (void *)itemid_copy,
      SWIGTYPE_p_SbName,
      SWIG_POINTER_OWN);
    if (pyitemid != NULL) {
      arglist = Py_BuildValue(
        "(OOdO)",
        PyTuple_GetItem(closure, 1),
        pyitemid,
        fraction,
        interruptible ? Py_True : Py_False);
      if (arglist != NULL) {
        result = PyObject_CallObject(PyTuple_GetItem(closure, 0), arglist);
        if (result == NULL) {
          PyErr_Print();
        } else {
          callback_result = PyObject_IsTrue(result) ? TRUE : FALSE;
        }
      }
    } else {
      delete itemid_copy;
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pyitemid);
  PyGILState_Release(gil);
  return callback_result;
}

static PyObject *
pivy_sodb_find_progress_closure(PyObject * func, PyObject * userdata)
{
  if (pivy_sodb_progress_closures == NULL) {
    return NULL;
  }

  Py_ssize_t count = PyList_Size(pivy_sodb_progress_closures);
  for (Py_ssize_t index = 0; index < count; ++index) {
    PyObject *closure = PyList_GetItem(pivy_sodb_progress_closures, index);
    if (PyTuple_Check(closure) &&
        PyTuple_GetItem(closure, 0) == func &&
        PyTuple_GetItem(closure, 1) == userdata) {
      return closure;
    }
  }
  return NULL;
}
%}

%typemap(in) PyObject * precallback {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject * precallback {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%typemap(in) PyObject * postcallback {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject * postcallback {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

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

%ignore SoDB::registerHeader;
%ignore SoDB::addProgressCallback;
%ignore SoDB::removeProgressCallback;
%rename(registerHeader) SoDB::pivy_registerHeader;
%rename(addProgressCallback) SoDB::pivy_addProgressCallback;
%rename(removeProgressCallback) SoDB::pivy_removeProgressCallback;

%extend SoDB {
  static SbBool pivy_registerHeader(const SbString & headerstring,
                                    SbBool isbinary,
                                    float ivversion,
                                    PyObject * precallback,
                                    PyObject * postcallback,
                                    PyObject * userdata = NULL) {
    PyObject *preclosure = Py_BuildValue(
      "(OOO)", precallback, postcallback, userdata ? userdata : Py_None);
    if (preclosure == NULL) {
      Py_XDECREF(preclosure);
      return FALSE;
    }

    if (pivy_sodb_keep_closure(&pivy_sodb_header_closures, preclosure) < 0) {
      Py_DECREF(preclosure);
      return FALSE;
    }

    SbBool result = SoDB::registerHeader(
      headerstring,
      isbinary,
      ivversion,
      pivy_sodb_header_pre_python_cb,
      pivy_sodb_header_post_python_cb,
      (void *)preclosure);
    Py_DECREF(preclosure);
    return result;
  }

  static void pivy_addProgressCallback(PyObject * func, PyObject * userdata) {
    PyObject *closure = Py_BuildValue("(OO)", func, userdata ? userdata : Py_None);
    if (closure == NULL) {
      return;
    }
    if (pivy_sodb_keep_closure(&pivy_sodb_progress_closures, closure) < 0) {
      Py_DECREF(closure);
      return;
    }
    SoDB::addProgressCallback(
      pivy_sodb_progress_python_cb,
      (void *)closure);
    Py_DECREF(closure);
  }

  static void pivy_removeProgressCallback(PyObject * func, PyObject * userdata) {
    PyObject *pyuserdata = userdata ? userdata : Py_None;
    PyObject *closure = pivy_sodb_find_progress_closure(func, pyuserdata);
    if (closure == NULL) {
      return;
    }

    SoDB::removeProgressCallback(
      pivy_sodb_progress_python_cb,
      (void *)closure);

    Py_ssize_t count = PyList_Size(pivy_sodb_progress_closures);
    for (Py_ssize_t index = 0; index < count; ++index) {
      if (PyList_GetItem(pivy_sodb_progress_closures, index) == closure) {
        PySequence_DelItem(pivy_sodb_progress_closures, index);
        return;
      }
    }
  }
}
