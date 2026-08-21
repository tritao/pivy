#ifndef PIVY_SB_VEC_COMMON_I
#define PIVY_SB_VEC_COMMON_I

%{
#include <limits>

template <typename T>
static bool
pivy_convert_sbvec_components(PyObject *input, int width, bool integer, T *output)
{
  if (!PySequence_Check(input)) {
    PyErr_SetString(PyExc_TypeError, "expected a sequence of components");
    return false;
  }

  Py_ssize_t length = PySequence_Length(input);
  if (length != width) {
    PyErr_SetString(PyExc_ValueError, "expected the correct number of components");
    return false;
  }

  for (int i = 0; i < width; ++i) {
    PyObject *value = PySequence_GetItem(input, i);
    if (value == NULL) {
      return false;
    }
    if (!PyNumber_Check(value)) {
      Py_DECREF(value);
      PyErr_SetString(PyExc_TypeError, "sequence elements must be numbers");
      return false;
    }

    if (integer) {
      long long converted = PyLong_AsLongLong(value);
      if (PyErr_Occurred()) {
        Py_DECREF(value);
        return false;
      }
      if (converted < static_cast<long long>(std::numeric_limits<T>::min()) ||
          converted > static_cast<long long>(std::numeric_limits<T>::max())) {
        Py_DECREF(value);
        PyErr_SetString(PyExc_OverflowError, "component is outside the supported range");
        return false;
      }
      output[i] = static_cast<T>(converted);
    } else {
      double converted = PyFloat_AsDouble(value);
      if (PyErr_Occurred()) {
        Py_DECREF(value);
        return false;
      }
      output[i] = static_cast<T>(converted);
    }
    Py_DECREF(value);
  }
  return true;
}

/* These names are part of the existing interface files for SbColor,
 * SbRotation, and the single-value field wrappers. Keep them as thin
 * compatibility functions while the vector typemaps share one converter. */
static void convert_SbVec2s_array(PyObject *input, short output[2])
{ (void)pivy_convert_sbvec_components(input, 2, true, output); }
static void convert_SbVec2f_array(PyObject *input, float output[2])
{ (void)pivy_convert_sbvec_components(input, 2, false, output); }
static void convert_SbVec2d_array(PyObject *input, double output[2])
{ (void)pivy_convert_sbvec_components(input, 2, false, output); }
static void convert_SbVec3s_array(PyObject *input, short output[3])
{ (void)pivy_convert_sbvec_components(input, 3, true, output); }
static void convert_SbVec3f_array(PyObject *input, float output[3])
{ (void)pivy_convert_sbvec_components(input, 3, false, output); }
static void convert_SbVec3d_array(PyObject *input, double output[3])
{ (void)pivy_convert_sbvec_components(input, 3, false, output); }
static void convert_SbVec4f_array(PyObject *input, float output[4])
{ (void)pivy_convert_sbvec_components(input, 4, false, output); }
static void convert_SbVec4d_array(PyObject *input, double output[4])
{ (void)pivy_convert_sbvec_components(input, 4, false, output); }
%}

%define PIVY_SB_VEC(_class_, _scalar_, _width_, _integer_)
%typemap(in) const _scalar_ v[_width_] (_scalar_ temp[_width_]) {
  if (!pivy_convert_sbvec_components($input, _width_, _integer_, temp)) {
    $1 = NULL;
    SWIG_fail;
  } else {
    $1 = temp;
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) const _scalar_ v[_width_] {
  void *ptr;
  $1 = (PySequence_Check($input) && PySequence_Size($input) == _width_ &&
        SWIG_ConvertPtr($input, &ptr, $descriptor(_class_ *), 0) == -1)
    ? 1 : 0;
}

/* Coin's older vector headers are inconsistent: constructors use a const
 * array while some setValue() overloads use a mutable array. Both are the
 * same Python-facing sequence contract. */
%typemap(in) _scalar_ v[_width_] (_scalar_ temp[_width_]) {
  if (!pivy_convert_sbvec_components($input, _width_, _integer_, temp)) {
    $1 = NULL;
    SWIG_fail;
  } else {
    $1 = temp;
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) _scalar_ v[_width_] {
  void *ptr;
  $1 = (PySequence_Check($input) && PySequence_Size($input) == _width_ &&
        SWIG_ConvertPtr($input, &ptr, $descriptor(_class_ *), 0) == -1)
    ? 1 : 0;
}

%ignore _class_::getValue() const;

%extend _class_ {
  _class_(const _class_ &other) {
    return new _class_(other);
  }

  _scalar_ __getitem__(int index) {
    if (index < 0) index += _width_;
    if (index < 0 || index >= _width_) {
      PyErr_SetString(PyExc_IndexError, "vector component index out of range");
      return (_scalar_)0;
    }
    return self->getValue()[index];
  }

  void __setitem__(int index, _scalar_ value) {
    if (index < 0) index += _width_;
    if (index < 0 || index >= _width_) {
      PyErr_SetString(PyExc_IndexError, "vector component index out of range");
      return;
    }
    (*self)[index] = value;
  }

  int __len__() { return _width_; }

  PyObject * __iter__() {
    PyObject *values = PyTuple_New(_width_);
    if (values == NULL) return NULL;
    for (int i = 0; i < _width_; ++i) {
      PyObject *value = _integer_
        ? PyLong_FromLongLong(static_cast<long long>(self->getValue()[i]))
        : PyFloat_FromDouble(static_cast<double>(self->getValue()[i]));
      if (value == NULL) {
        Py_DECREF(values);
        return NULL;
      }
      PyTuple_SET_ITEM(values, i, value);
    }
    PyObject *iterator = PyObject_GetIter(values);
    Py_DECREF(values);
    return iterator;
  }

%pythoncode %{
  def getValue(self, *args):
    values = getattr(_coin, "_class_" + "_getValue")(self)
    if not args:
      return values
    if len(args) != _width_:
      raise TypeError("expected _width_ output arguments")
    for output, value in zip(args, values):
      if not hasattr(output, "assign"):
        raise TypeError("output arguments must be scalar pointer helpers")
      output.assign(value)
    return None
%}
}
%enddef

%define PIVY_SB_VEC_OUTPUT2(_scalar_)
%apply _scalar_ *OUTPUT { _scalar_ & x, _scalar_ & y };
%enddef

%define PIVY_SB_VEC_OUTPUT3(_scalar_)
%apply _scalar_ *OUTPUT { _scalar_ & x, _scalar_ & y, _scalar_ & z };
%enddef

%define PIVY_SB_VEC_OUTPUT4(_scalar_)
%apply _scalar_ *OUTPUT { _scalar_ & x, _scalar_ & y, _scalar_ & z, _scalar_ & w };
%enddef

#endif
