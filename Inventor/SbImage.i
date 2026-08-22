%typemap(in) (const unsigned char * bytes, const SbVec2s & size, const int bytesperpixel) {
  unsigned char * image;
  PyObject * buf = $input;
  PyObject * vec2s = $input;
  PyObject * nc = $input;

  if ((SWIG_ConvertPtr(vec2s, (void **) &$2, SWIGTYPE_p_SbVec2s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $3 = PyInt_AsLong(nc);
#ifdef PY_2
  if (PyString_Check(buf))
#else
  if (PyBytes_Check(buf))
#endif
  {
    Py_ssize_t len = (*$2)[0] * (*$2)[1] * $3;
#ifdef PY_2
    PyString_AsStringAndSize(buf, (char **)&image, &len);
#else
    PyBytes_AsStringAndSize(buf, (char **)&image, &len);
#endif
    $1 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a string."); SWIG_fail;
  }
}

%typemap(in) (const unsigned char * bytes, const SbVec3s & size, const int bytesperpixel) {
  unsigned char * image;
  PyObject * buf = $input;
  PyObject * vec3s = $input;
  PyObject * nc = $input;

  if ((SWIG_ConvertPtr(vec3s, (void **)&$2, SWIGTYPE_p_SbVec3s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $3 = PyInt_AsLong(nc);
  if (PyString_Check(buf)) {
    Py_ssize_t len = (*$2)[0] * (*$2)[1] * (*$2)[2] * $3;
#ifdef PY_2
    PyString_AsStringAndSize(buf, (char **)&image, &len);
#else
    PyBytes_AsStringAndSize(buf, (char **)&image, &len);
#endif
    $1 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a string."); SWIG_fail;
  }
}

%typemap(in) (const SbVec2s & size, const int bytesperpixel, const unsigned char * bytes) {
  unsigned char * image;
  PyObject * vec2s = $input;
  PyObject * nc = $input;
  PyObject * buf = $input;

  if ((SWIG_ConvertPtr(vec2s, (void **)&$1, SWIGTYPE_p_SbVec2s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($1 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $2 = PyInt_AsLong(nc);
#ifdef PY_2
  if (PyString_Check(buf))
#else
  if (PyBytes_Check(buf))
#endif
  {
    Py_ssize_t len = (*$1)[0] * (*$1)[1] * $2;
#ifdef PY_2
    PyString_AsStringAndSize(buf, (char **)&image, &len);
#else
    PyBytes_AsStringAndSize(buf, (char **)&image, &len);
#endif
    $3 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a string."); SWIG_fail;
  }
}

%typemap(in) (const SbVec3s & size, const int bytesperpixel, const unsigned char * bytes) {
  unsigned char * image;
  PyObject * vec3s = $input;
  PyObject * nc = $input;
  PyObject * buf = $input;

  if ((SWIG_ConvertPtr(vec3s, (void **)&$1, SWIGTYPE_p_SbVec3s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($1 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $2 = PyInt_AsLong(nc);
#ifdef PY_2
  if (PyString_Check(buf))
#else
  if (PyBytes_Check(buf))
#endif
  {
    Py_ssize_t len = (*$1)[0] * (*$1)[1] * ((*$1)[2] ? (*$1)[2] : 1) * $2;
#ifdef PY_2
    PyString_AsStringAndSize(buf, (char **)&image, &len);
#else
    PyBytes_AsStringAndSize(buf, (char **)&image, &len);
#endif
    $3 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a string."); SWIG_fail;
  }
}

%extend SbImage {
  PyObject * getValue() {
    int nc;
    SbVec3s size;
    PyObject * result;

    const unsigned char * image = self->getValue(size, nc);
    
    /* check for 3D image */
    if (size[2] == 0) {
      SbVec2s * vec2s = new SbVec2s(size[0], size[1]);
      result = Py_BuildValue("(y#Oi)",
                             (const char*)image,
                             (*vec2s)[0] * (*vec2s)[1] * nc,
                             SWIG_NewPointerObj((void *)vec2s, SWIGTYPE_p_SbVec2s, 1),
                             nc);
    } else {
      SbVec3s * vec3s = new SbVec3s(size[0], size[1], size[2]);
      result = Py_BuildValue("(y#Oi)",
                             (const char*)image,
                             (*vec3s)[0] * (*vec3s)[1] * (*vec3s)[2] * nc,
                             SWIG_NewPointerObj((void *)vec3s, SWIGTYPE_p_SbVec3s, 1),
                             nc);
    }
      
    return result;
  }
}

%{
static PyObject *pivy_sb_image_read_closures = NULL;

static int
pivy_sb_image_keep_read_closure(PyObject *closure)
{
  if (pivy_sb_image_read_closures == NULL) {
    pivy_sb_image_read_closures = PyList_New(0);
    if (pivy_sb_image_read_closures == NULL) {
      return -1;
    }
  }
  return PyList_Append(pivy_sb_image_read_closures, closure);
}

static PyObject *
pivy_sb_image_find_read_closure(PyObject *cb, PyObject *userdata)
{
  if (pivy_sb_image_read_closures == NULL) {
    return NULL;
  }

  Py_ssize_t count = PyList_Size(pivy_sb_image_read_closures);
  for (Py_ssize_t index = 0; index < count; ++index) {
    PyObject *closure = PyList_GetItem(
      pivy_sb_image_read_closures,
      index);
    if (PyTuple_Check(closure) &&
        PyTuple_GET_ITEM(closure, 0) == cb &&
        PyTuple_GET_ITEM(closure, 1) == userdata) {
      return closure;
    }
  }
  return NULL;
}

static void
pivy_sb_image_remove_read_closure(PyObject *pyclosure)
{
  if (pivy_sb_image_read_closures == NULL || pyclosure == NULL) {
    return;
  }

  Py_ssize_t count = PyList_Size(pivy_sb_image_read_closures);
  for (Py_ssize_t index = 0; index < count; ++index) {
    if (PyList_GetItem(
          pivy_sb_image_read_closures,
          index) == pyclosure) {
      PySequence_DelItem(pivy_sb_image_read_closures, index);
      return;
    }
  }
}

static SbBool
pivy_sb_image_read_python_cb(const SbString &filename,
                             SbImage *image,
                             void *userdata)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  PyObject *closure = (PyObject *)userdata;
  PyObject *pyfilename = NULL;
  PyObject *pyimage = NULL;
  PyObject *arglist = NULL;
  PyObject *result = NULL;
  SbBool callback_result = FALSE;

  if (PyTuple_Check(closure) && PyTuple_GET_SIZE(closure) == 2) {
    pyfilename = SWIG_NewPointerObj(
      (void *)new SbString(filename),
      SWIGTYPE_p_SbString,
      SWIG_POINTER_OWN);
    pyimage = SWIG_NewPointerObj(
      (void *)image,
      SWIGTYPE_p_SbImage,
      0);
    if (pyfilename != NULL && pyimage != NULL) {
      arglist = Py_BuildValue(
        "(OOO)",
        PyTuple_GET_ITEM(closure, 1),
        pyfilename,
        pyimage);
      if (arglist != NULL) {
        result = PyObject_CallObject(
          PyTuple_GET_ITEM(closure, 0),
          arglist);
        if (result == NULL) {
          PyErr_Print();
        } else {
          callback_result = PyObject_IsTrue(result) ? TRUE : FALSE;
        }
      }
    }
  }

  Py_XDECREF(result);
  Py_XDECREF(arglist);
  Py_XDECREF(pyimage);
  Py_XDECREF(pyfilename);
  PyGILState_Release(gil);
  return callback_result;
}

static SbBool
pivy_sb_image_schedule_read_python_cb(const SbString &filename,
                                      SbImage *image,
                                      void *userdata)
{
  SbBool callback_result = pivy_sb_image_read_python_cb(
    filename,
    image,
    userdata);
  PyGILState_STATE gil = PyGILState_Ensure();
  pivy_sb_image_remove_read_closure((PyObject *)userdata);
  PyGILState_Release(gil);
  return callback_result;
}
%}

%typemap(in) PyObject * cb {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%typemap(typecheck) PyObject * cb {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%typemap(in) PyObject * closure {
  $1 = $input;
}

%typemap(typecheck) PyObject * closure {
  $1 = 1;
}

%ignore SbImage::addReadImageCB;
%ignore SbImage::removeReadImageCB;
%ignore SbImage::scheduleReadFile;
%rename(addReadImageCB) SbImage::_pivy_addReadImageCB;
%rename(removeReadImageCB) SbImage::_pivy_removeReadImageCB;
%rename(scheduleReadFile) SbImage::_pivy_scheduleReadFile;

%extend SbImage {
  static void _pivy_addReadImageCB(
      PyObject * cb,
      PyObject * closure = NULL) {
    PyObject *pyclosure = Py_BuildValue(
      "(OO)",
      cb,
      closure ? closure : Py_None);
    if (pyclosure == NULL) {
      return;
    }
    if (pivy_sb_image_keep_read_closure(pyclosure) < 0) {
      Py_DECREF(pyclosure);
      return;
    }

    SbImage::addReadImageCB(
      pivy_sb_image_read_python_cb,
      (void *)pyclosure);
    Py_DECREF(pyclosure);
  }

  static void _pivy_removeReadImageCB(
      PyObject * cb,
      PyObject * closure = NULL) {
    PyObject *userdata = closure ? closure : Py_None;
    PyObject *pyclosure = pivy_sb_image_find_read_closure(cb, userdata);
    if (pyclosure == NULL) {
      return;
    }

    SbImage::removeReadImageCB(
      pivy_sb_image_read_python_cb,
      (void *)pyclosure);

    pivy_sb_image_remove_read_closure(pyclosure);
  }

  SbBool _pivy_scheduleReadFile(
      PyObject * cb,
      PyObject * closure,
      const SbString & filename,
      const SbString * const * searchdirectories = NULL,
      const int numdirectories = 0) {
    PyObject *pyclosure = Py_BuildValue(
      "(OO)",
      cb,
      closure ? closure : Py_None);
    if (pyclosure == NULL) {
      return FALSE;
    }
    if (pivy_sb_image_keep_read_closure(pyclosure) < 0) {
      Py_DECREF(pyclosure);
      return FALSE;
    }

    SbBool result = self->scheduleReadFile(
      pivy_sb_image_schedule_read_python_cb,
      (void *)pyclosure,
      filename,
      searchdirectories,
      numdirectories);
    if (!result) {
      pivy_sb_image_remove_read_closure(pyclosure);
    }
    Py_DECREF(pyclosure);
    return result;
  }
}
