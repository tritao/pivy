#ifndef PIVY_SOMFVEC_COMMON_I
#define PIVY_SOMFVEC_COMMON_I

%{
template <typename T>
static bool
pivy_convert_vector_components(PyObject * input, int width, T * output)
{
  if (!PySequence_Check(input) || PySequence_Length(input) != width) {
    PyErr_SetString(PyExc_ValueError,
                    "Expected a sequence with the correct number of components");
    return false;
  }

  for (int i = 0; i < width; i++) {
    PyObject * value = PySequence_GetItem(input, i);
    if (value == NULL) {
      return false;
    }
    if (!PyNumber_Check(value)) {
      PyErr_SetString(PyExc_ValueError, "Sequence elements must be numbers");
      Py_DECREF(value);
      return false;
    }
    output[i] = static_cast<T>(PyFloat_AsDouble(value));
    Py_DECREF(value);
    if (PyErr_Occurred()) {
      return false;
    }
  }
  return true;
}

template <typename T>
static bool
pivy_convert_vector_sequence(PyObject * input, int length, int width, T * output)
{
  for (int i = 0; i < length; i++) {
    PyObject * value = PySequence_GetItem(input, i);
    if (value == NULL) {
      return false;
    }
    if (!pivy_convert_vector_components(value, width, output + i * width)) {
      Py_DECREF(value);
      return false;
    }
    Py_DECREF(value);
  }
  return true;
}

static void
convert_SoMFVec3f_array(PyObject * input, int length, float output[][3])
{
  pivy_convert_vector_sequence<float>(input, length, 3, &output[0][0]);
}
%}

%define PIVY_SOMFVEC(_class_, _vector_, _scalar_, _components_, _width_, _setvalues_)
%typemap(in) const _scalar_ _components_[][ _width_ ] (_scalar_ (*temp)[ _width_ ]) {
  if (PySequence_Check($input)) {
    Py_ssize_t sequence_length = PySequence_Length($input);
    int length = static_cast<int>(sequence_length);
    temp = length > 0
      ? (_scalar_ (*)[ _width_ ]) malloc(length * _width_ * sizeof(_scalar_))
      : NULL;
    if (sequence_length < 0 || (length > 0 && temp == NULL)) {
      if (sequence_length >= 0 && temp == NULL) {
        SWIG_exception_fail(SWIG_MemoryError, "unable to allocate vector values");
      }
      $1 = NULL;
    } else if (length > 0 &&
               !pivy_convert_vector_sequence<_scalar_>(
                 $input, length, _width_, &temp[0][0])) {
      free(temp);
      temp = NULL;
      $1 = NULL;
      SWIG_fail;
    } else {
      $1 = temp;
    }
  } else {
    $1 = NULL;
    SWIG_exception_fail(SWIG_TypeError, "expected a sequence.");
  }
}

%typemap(freearg) const _scalar_ _components_[][ _width_ ] {
  if ($1) {
    free($1);
  }
}

%typemap(in) const _scalar_ _components_[_width_] (_scalar_ temp[_width_]) {
  if (!pivy_convert_vector_components($input, _width_, temp)) {
    $1 = NULL;
    SWIG_fail;
  } else {
    $1 = temp;
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER)
    const _scalar_ _components_[_width_] {
  void * ptr;
  $1 = (PySequence_Check($input) &&
        SWIG_ConvertPtr($input, &ptr, $descriptor(_class_ *), 0) == -1)
    ? 1 : 0;
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER)
    const _scalar_ _components_[][ _width_ ] {
  $1 = 0;
  if (PySequence_Check($input) && PySequence_Size($input) > 0) {
    PyObject * value = PySequence_GetItem($input, 0);
    if (value != NULL && PySequence_Check(value)) {
      void * ptr;
      $1 = SWIG_ConvertPtr(
        value, &ptr, $descriptor(_vector_ *), 0) == -1;
    }
    Py_XDECREF(value);
  } else if (PySequence_Check($input)) {
    $1 = 1;
  }
}

%typemap(in) const _vector_ *newvals {
  int length;
  if (PySequence_Check($input)) {
    length = PySequence_Length($input);
    if (length > 0) {
      $1 = new _vector_[length];
      for (int i = 0; i < length; i++) {
        _vector_ * vector_pointer = NULL;
        PyObject * item = PySequence_GetItem($input, i);
        if (item == NULL) {
          delete[] $1;
          $1 = NULL;
          SWIG_fail;
        }
        if (SWIG_ConvertPtr(item, (void **) &vector_pointer, $1_descriptor, 1) == -1 ||
            vector_pointer == NULL) {
          PyErr_SetString(PyExc_TypeError,
                          "Sequence elements must be vector instances");
          Py_DECREF(item);
          delete[] $1;
          $1 = NULL;
          SWIG_fail;
        }
        $1[i] = *vector_pointer;
        Py_DECREF(item);
      }
    } else {
      $1 = NULL;
    }
  } else {
    SWIG_exception_fail(SWIG_TypeError, "expected a sequence.");
  }
}

%typemap(freearg) const _vector_ *newvals {
  if ($1) {
    delete[] $1;
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) const _vector_ *newvals {
  if (PySequence_Check($input)) {
    if (PySequence_Size($input) == 0) {
      $1 = 1;
    } else {
      PyObject * value = PySequence_GetItem($input, 0);
      void * ptr;
      $1 = value != NULL &&
        SWIG_ConvertPtr(value, &ptr, $descriptor(_vector_ *), 0) != -1;
      Py_XDECREF(value);
    }
  } else {
    $1 = 0;
  }
}

%feature("shadow") _class_::setValues %{
def setValues(*args):
   if len(args) == 2:
      return _coin._setvalues_(args[0], 0, len(args[1]), args[1])
   elif len(args) == 3:
      return _coin._setvalues_(args[0], args[1], len(args[2]), args[2])
   return _coin._setvalues_(*args)
%}

%ignore _class_::getValues(const int start) const;

%typemap(in,numinputs=0) int & len (int temp) {
  $1 = &temp;
  *$1 = 0;
}

%typemap(argout) int & len {
  Py_XDECREF($result);
  $result = PyList_New(*$1);
  if ($result) {
    for (int i = 0; i < *$1; i++) {
      _vector_ * vector_pointer = new _vector_(result[i]);
      PyObject * object = SWIG_NewPointerObj(
        vector_pointer, $descriptor(_vector_ *), 1);
      PyList_SetItem($result, i, object);
    }
  }
}

%rename(getValues) _class_::__getValuesHelper__;

%extend _class_ {
  _vector_ __getitem__(int i) { return (*self)[i]; }
  void __setitem__(int i, const _vector_ & value) {
    self->set1Value(i, value);
  }
  void setValue(const _class_ * other) { *self = *other; }
  const _vector_ * __getValuesHelper__(int & len, int i = 0) {
    if (i < 0 || i >= self->getNum()) {
      return NULL;
    }
    len = self->getNum() - i;
    return self->getValues(i);
  }
}
%enddef

#endif
