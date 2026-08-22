%{
#include <stddef.h>

typedef struct {
  PyObject **owners;
  Py_ssize_t count;
  char *values[1];
} PivyStringArray;

static void
pivy_free_string_array(char **values)
{
  if (values) {
    PivyStringArray *array = (PivyStringArray *)(
        (char *)values - offsetof(PivyStringArray, values));
    if (array->owners) {
      for (Py_ssize_t i = 0; i < array->count; i++) {
        Py_XDECREF(array->owners[i]);
      }
      free(array->owners);
    }
    free(array);
  }
}
%}

%typemap(in) const char * strings[] {
  Py_ssize_t length;

  $1 = NULL;
  if (!PySequence_Check($input) || PyUnicode_Check($input) ||
      PyBytes_Check($input)) {
    SWIG_exception_fail(SWIG_TypeError, "expected a sequence of strings");
  }

  length = PySequence_Length($input);
  if (length < 0) {
    SWIG_fail;
  }
  if (length > 0) {
    PivyStringArray *array = (PivyStringArray *)calloc(
        1, sizeof(PivyStringArray) +
        (size_t)(length - 1) * sizeof(char *));
    if (array == NULL) {
      SWIG_exception_fail(
          SWIG_MemoryError, "unable to allocate string values");
    }
    array->count = length;
    array->owners = (PyObject **)calloc(
        (size_t)length, sizeof(PyObject *));
    if (array->owners == NULL) {
      free(array);
      SWIG_exception_fail(
          SWIG_MemoryError, "unable to allocate string owners");
    }
    $1 = array->values;

    for (Py_ssize_t i = 0; i < length; i++) {
      PyObject *item = PySequence_GetItem($input, i);
      PyObject *text = item;
      const char *value;

      if (item == NULL) {
        pivy_free_string_array($1);
        $1 = NULL;
        SWIG_fail;
      }

      if (!PyUnicode_Check(item) && !PyBytes_Check(item)) {
        text = PyObject_Str(item);
        Py_DECREF(item);
        if (text == NULL) {
          pivy_free_string_array($1);
          $1 = NULL;
          SWIG_fail;
        }
      }

#ifdef PY_2
      value = PyString_AsString(text);
#else
      value = PyBytes_Check(text) ? PyBytes_AsString(text) :
        PyUnicode_AsUTF8(text);
#endif
      if (value == NULL) {
        Py_DECREF(text);
        pivy_free_string_array($1);
        $1 = NULL;
        SWIG_fail;
      }

      $1[i] = (char *)value;
      array->owners[i] = text;
    }
  }
}

%typemap(freearg) const char * strings[] {
  pivy_free_string_array($1);
  $1 = NULL;
}

%typemap(typecheck,precedence=SWIG_TYPECHECK_POINTER) const char * strings[] {
  $1 = PySequence_Check($input) && !PyUnicode_Check($input) &&
       !PyBytes_Check($input) ? 1 : 0;
}

%feature("shadow") SoMFName::setValues %{
def setValues(*args):
   if len(args) == 2:
     return _coin.SoMFName_setValues(args[0], 0, len(args[1]), args[1])
   elif len(args) == 3:
     return _coin.SoMFName_setValues(args[0], args[1], len(args[2]), args[2])
   return _coin.SoMFName_setValues(*args)
%}

%ignore SoMFName::getValues(const int start) const;

%typemap(in,numinputs=0) int & len (int temp) {
  $1 = &temp;
  *$1 = 0;
}

%typemap(argout) int & len {
  Py_XDECREF($result); /* free up any previous result */
  $result = PyList_New(*$1);
  if (result) {
    for (int i = 0; i < *$1; i++) {
      PyObject * str = 
#ifdef PY_2
        PyString_FromString(result[i].getString());
#else
        PyUnicode_DecodeUTF8(result[i].getString(), strlen(result[i].getString()), "strict");
#endif
      PyList_SetItem($result, i, str);
    }
  }
}

%rename(getValues) SoMFName::__getValuesHelper__;

%extend SoMFName {
  const SbName & __getitem__(int i) { return (*self)[i]; }
  void  __setitem__(int i, const SbName & value) { self->set1Value(i, value); }
  void setValue(const SoMFName * other ){ *self = *other; }
  const SbName * __getValuesHelper__(int & len, int i = 0) {
    if (i < 0 || i >= self->getNum()) { return NULL; }
    len = self->getNum() - i;
    return self->getValues(i);
  }
}
