%{
static int
convert_SoMFEnum_array(PyObject * input, int len, int * temp)
{
  int i;
  for (i=0; i<len; i++) {
    PyObject * oi = PySequence_GetItem(input,i);
    if (PyNumber_Check(oi)) {
      temp[i] = (int) PyInt_AsLong(oi);
      if (PyErr_Occurred()) {
        Py_DECREF(oi);
        return -1;
      }
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
      Py_DECREF(oi);
      return -1;
    }
    Py_DECREF(oi);
  }
  return 0;
}
%}

%typemap(in) const int * newvals (int * values_temp) {
  if (PySequence_Check($input)) {
    Py_ssize_t length = PySequence_Length($input);
    if (length < 0) {
      SWIG_fail;
    }
    values_temp = length > 0
      ? (int *) malloc(length * sizeof(int))
      : NULL;
    if (length > 0 && values_temp == NULL) {
      SWIG_exception_fail(SWIG_MemoryError, "unable to allocate enum values");
    }
    if (convert_SoMFEnum_array($input, (int) length, values_temp) < 0) {
      free(values_temp);
      values_temp = NULL;
      SWIG_fail;
    }
    $1 = values_temp;
  } else {
    SWIG_exception_fail(SWIG_TypeError, "expected a sequence.");
  }
}

%typemap(in) const SbName * const names (SbName * names_temp) {
  if (PySequence_Check($input) &&
      !PyUnicode_Check($input) && !PyBytes_Check($input)) {
    Py_ssize_t length = PySequence_Length($input);
    if (length < 0) {
      SWIG_fail;
    }
    names_temp = new SbName[length];
    for (Py_ssize_t i = 0; i < length; i++) {
      PyObject * item = PySequence_GetItem($input, i);
      if (item == NULL) {
        delete[] names_temp;
        names_temp = NULL;
        SWIG_fail;
      }

      if (PyUnicode_Check(item)) {
        const char * value = PyUnicode_AsUTF8(item);
        if (value == NULL) {
          Py_DECREF(item);
          delete[] names_temp;
          names_temp = NULL;
          SWIG_fail;
        }
        names_temp[i] = SbName(value);
      } else {
        SbName * name = NULL;
        if (SWIG_ConvertPtr(
              item, (void **) &name, $descriptor(SbName *), 0) != 0 ||
            name == NULL) {
          PyErr_SetString(
            PyExc_TypeError,
            "enum names must be SbName or str instances");
          Py_DECREF(item);
          delete[] names_temp;
          names_temp = NULL;
          SWIG_fail;
        }
        names_temp[i] = *name;
      }
      Py_DECREF(item);
    }
    $1 = names_temp;
  } else {
    SbName * name = NULL;
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

%typemap(freearg) const SbName * const names {
  if ($1) {
    delete[] $1;
  }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER)
    const SbName * const names {
  if (PySequence_Check($input) &&
      !PyUnicode_Check($input) && !PyBytes_Check($input)) {
    $1 = 1;
  } else {
    void * pointer = NULL;
    $1 = SWIG_ConvertPtr(
      $input, &pointer, $descriptor(SbName *), 0) == 0;
  }
}

%typemap(in) SbName & name {
  void * pointer = NULL;
  if (SWIG_ConvertPtr(
        $input, &pointer, $descriptor(SbName *), 0) != 0 ||
      pointer == NULL) {
    SWIG_exception_fail(
      SWIG_TypeError, "expected an SbName instance");
  }
  $1 = reinterpret_cast<SbName *>(pointer);
}

%typemap(freearg) SbName & name {
}

%feature("shadow") SoMFEnum::setEnums %{
def setEnums(*args):
   if len(args) == 4:
      try:
         values = list(args[2])
      except TypeError:
         raise TypeError("enum values must be a sequence")
      if len(values) != args[1]:
         raise ValueError("enum values must match num")
      names = args[3]
      if isinstance(names, str):
         names = [names]
      elif isinstance(names, SbName):
         if args[1] != 1:
            raise ValueError("a single enum name requires num == 1")
      else:
         try:
            names = list(names)
         except TypeError:
            raise TypeError("enum names must be an SbName or a sequence")
         if len(names) != args[1]:
            raise ValueError("enum names must match num")
      args = (args[0], args[1], values, names)
   return _coin.SoMFEnum_setEnums(*args)
%}

%ignore SoMFEnum::getValues(const int start) const;

%typemap(in,numinputs=0) int & len (int temp) {
  $1 = &temp;
  *$1 = 0;
}

%typemap(argout) int & len {
  Py_XDECREF($result); /* free up any previous result */
  $result = PyList_New(*$1);
  if (result) {
    for (int i = 0; i < *$1; i++){
      PyList_SetItem($result, i, PyInt_FromLong((long)result[i]));
    }
  }
}

%feature("shadow") SoMFEnum::setValues %{
def setValues(*args):
   if len(args) == 2:
      if isinstance(args[1], SoMFEnum):
         val = args[1].getValues()
         return _coin.SoMFEnum_setValues(args[0],0,len(val),val)
      else:
         return _coin.SoMFEnum_setValues(args[0],0,len(args[1]),args[1])
   elif len(args) == 3:
      if isinstance(args[2], SoMFEnum):
         val = args[2].getValues()
         return _coin.SoMFEnum_setValues(args[0],args[1],len(val),val)
      else:
         return _coin.SoMFEnum_setValues(args[0],args[1],len(args[2]),args[2])
   return _coin.SoMFEnum_setValues(*args)
%}

%rename(getValues) SoMFEnum::__getValuesHelper__;

%extend SoMFEnum {
  const int __getitem__(int i) { return (*self)[i]; }
  void  __setitem__(int i, int value) { self->set1Value(i, value); }
  void setValue(const SoMFEnum * other) { *self = *other; }  
  const int * __getValuesHelper__(int & len, int i = 0) {
    if (i < 0 || i > self->getNum()) { return NULL; }
    len = self->getNum() - i;
    return self->getValues(i);
  }
}
