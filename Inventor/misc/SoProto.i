%{
static PyObject *pivy_so_proto_fetch_closure = NULL;

static SoProto *
pivy_so_proto_fetch_python_cb(SoInput *input,
                              const SbString *urls,
                              int numurls,
                              void *userdata)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *pyinput = NULL;
  PyObject *pyurls = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;
  SoProto *proto = NULL;

  if (PyTuple_Check(closure) && PyTuple_GET_SIZE(closure) == 2) {
    pyinput = SWIG_NewPointerObj(
      (void *)input,
      SWIGTYPE_p_SoInput,
      0);
    pyurls = PyList_New(numurls > 0 ? numurls : 0);
    if (pyurls != NULL) {
      for (int index = 0; index < numurls; ++index) {
        PyObject *pyurl = SWIG_NewPointerObj(
          (void *)&urls[index],
          SWIGTYPE_p_SbString,
          0);
        if (pyurl == NULL) {
          Py_DECREF(pyurls);
          pyurls = NULL;
          break;
        }
        PyList_SET_ITEM(pyurls, index, pyurl);
      }
    }

    if (pyinput != NULL && pyurls != NULL) {
      arglist = Py_BuildValue(
        "(OOOi)",
        PyTuple_GET_ITEM(closure, 0),
        pyinput,
        pyurls,
        numurls);
      if (arglist != NULL) {
        result = PyObject_CallObject(
          PyTuple_GET_ITEM(closure, 1),
          arglist);
        if (result == NULL) {
          PyErr_Print();
        } else if (result != Py_None &&
                   SWIG_ConvertPtr(
                     result,
                     (void **)&proto,
                     SWIGTYPE_p_SoProto,
                     SWIG_POINTER_EXCEPTION | 0) == -1) {
          PyErr_Print();
          proto = NULL;
        }
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pyurls);
  Py_XDECREF(pyinput);
  PyGILState_Release(gil);
  return proto;
}
%}

%typemap(in) PyObject * cb {
  if ($input != Py_None && !PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject * cb {
  $1 = ($input == Py_None || PyCallable_Check($input)) ? 1 : 0;
}

%typemap(in) PyObject * closure {
  $1 = $input;
}

%typemap(typecheck) PyObject * closure {
  $1 = 1;
}

%ignore SoProto::setFetchExternProtoCallback;
%rename(setFetchExternProtoCallback)
  SoProto::_pivy_setFetchExternProtoCallback;

%extend SoProto {
  static void _pivy_setFetchExternProtoCallback(
      PyObject * cb,
      PyObject * closure = NULL) {
    SoFetchExternProtoCB *callback = NULL;
    PyObject *pyclosure = NULL;
    if (cb != Py_None) {
      callback = pivy_so_proto_fetch_python_cb;
      pyclosure = Py_BuildValue(
        "(OO)",
        closure ? closure : Py_None,
        cb);
      if (pyclosure == NULL) {
        return;
      }
    }

    SoProto::setFetchExternProtoCallback(
      callback,
      (void *)pyclosure);
    Py_XDECREF(pivy_so_proto_fetch_closure);
    pivy_so_proto_fetch_closure = pyclosure;
  }
}
