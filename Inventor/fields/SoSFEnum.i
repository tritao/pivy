%{
static int
pivy_convert_sosfenum_values(PyObject *input, int *values, Py_ssize_t length)
{
  for (Py_ssize_t i = 0; i < length; i++) {
    PyObject *item = PySequence_GetItem(input, i);
    if (item == NULL) {
      return -1;
    }
    if (!PyNumber_Check(item)) {
      PyErr_SetString(PyExc_ValueError, "enum values must be numbers");
      Py_DECREF(item);
      return -1;
    }
    values[i] = (int) PyInt_AsLong(item);
    Py_DECREF(item);
    if (PyErr_Occurred()) {
      return -1;
    }
  }
  return 0;
}
%}

%typemap(in) const int * vals (int * values_temp) {
  Py_ssize_t length;
  if (!PySequence_Check($input) || PyUnicode_Check($input) ||
      PyBytes_Check($input)) {
    SWIG_exception_fail(SWIG_TypeError, "expected a sequence of enum values");
  }
  length = PySequence_Length($input);
  if (length < 0) {
    SWIG_fail;
  }
  values_temp = length > 0 ? (int *) malloc(length * sizeof(int)) : NULL;
  if (length > 0 && values_temp == NULL) {
    SWIG_exception_fail(SWIG_MemoryError, "unable to allocate enum values");
  }
  if (pivy_convert_sosfenum_values($input, values_temp, length) < 0) {
    free(values_temp);
    values_temp = NULL;
    SWIG_fail;
  }
  $1 = values_temp;
}

%typemap(freearg) const int * vals {
  if ($1) {
    free((void *) $1);
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) const int * vals {
  $1 = PySequence_Check($input) && !PyUnicode_Check($input) &&
       !PyBytes_Check($input) ? 1 : 0;
}

%typemap(in) const SbName * names (SbName * names_temp) {
  if (PySequence_Check($input) && !PyUnicode_Check($input) &&
      !PyBytes_Check($input)) {
    Py_ssize_t length = PySequence_Length($input);
    if (length < 0) {
      SWIG_fail;
    }
    names_temp = new SbName[length];
    for (Py_ssize_t i = 0; i < length; i++) {
      PyObject *item = PySequence_GetItem($input, i);
      SbName *name = NULL;
      if (item == NULL) {
        delete[] names_temp;
        names_temp = NULL;
        SWIG_fail;
      }
      if (PyUnicode_Check(item)) {
        const char *value = PyUnicode_AsUTF8(item);
        if (value == NULL) {
          Py_DECREF(item);
          delete[] names_temp;
          names_temp = NULL;
          SWIG_fail;
        }
        names_temp[i] = SbName(value);
      } else if (SWIG_ConvertPtr(
                   item, (void **) &name, $descriptor(SbName *), 0) == 0 &&
                 name != NULL) {
        names_temp[i] = *name;
      } else {
        PyErr_SetString(
            PyExc_TypeError, "enum names must be SbName or str instances");
        Py_DECREF(item);
        delete[] names_temp;
        names_temp = NULL;
        SWIG_fail;
      }
      Py_DECREF(item);
    }
    $1 = names_temp;
  } else {
    SbName *name = NULL;
    if (SWIG_ConvertPtr(
          $input, (void **) &name, $descriptor(SbName *), 0) != 0 ||
        name == NULL) {
      SWIG_exception_fail(
          SWIG_TypeError, "expected an SbName or a sequence of names");
    }
    names_temp = new SbName[1];
    names_temp[0] = *name;
    $1 = names_temp;
  }
}

%typemap(freearg) const SbName * names {
  if ($1) {
    delete[] (SbName *) $1;
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) const SbName * names {
  if (PySequence_Check($input) && !PyUnicode_Check($input) &&
      !PyBytes_Check($input)) {
    $1 = 1;
  } else {
    void *pointer = NULL;
    $1 = SWIG_ConvertPtr(
      $input, &pointer, $descriptor(SbName *), 0) == 0;
  }
}

%feature("shadow") SoSFEnum::setEnums %{
def setEnums(self, num, vals, names):
   try:
      values = list(vals)
   except TypeError:
      raise TypeError("enum values must be a sequence")
   if len(values) != num:
      raise ValueError("enum values must match num")
   if isinstance(names, str):
      names = [names]
   elif isinstance(names, SbName):
      if num != 1:
         raise ValueError("a single enum name requires num == 1")
   else:
      try:
         names = list(names)
      except TypeError:
         raise TypeError("enum names must be an SbName or a sequence")
      if len(names) != num:
         raise ValueError("enum names must match num")
   return _coin.SoSFEnum_setEnums(self, num, values, names)
%}

%extend SoSFEnum {
  void setValue(const SoSFEnum * other) { *self = *other; }
}
