/*
 * Copyright (c) 2002-2007 Systems in Motion
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

/* header include needed to let nodekit extensions find the SbTime header */
%{
#include <Inventor/SbTime.h>
#include <stddef.h>
#include <time.h>
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>

#if (PY_VERSION_HEX < 0x02050000)
/* Py_ssize_t needed for Python 2.5 compatibility, but isn't defined
 * in earlier Python versions. */
typedef int Py_ssize_t;
#endif

#if PY_MAJOR_VERSION >= 3
  #define IS_PY3K
#endif

PyObject *
cast_internal(PyObject * self, PyObject * obj, const char * type_name, Py_ssize_t type_len,
              int own = 0)
{
  swig_type_info * swig_type = 0;
  void * cast_obj = 0;
  char * ptr_type;

  /*
   * add a pointer sign to the string coming from the interpreter
   * e.g. "SoSeparator" becomes "SoSeparator *" - so that SWIG_TypeQuery()
   * can do its job.
   */
  if (!(ptr_type = (char*)malloc(type_len+3))) { SWIG_fail; }

  memset(ptr_type, 0, type_len+3);
  strncpy(ptr_type, type_name, type_len);
  strcat(ptr_type, " *");

  if (!(swig_type = SWIG_TypeQuery(ptr_type))) {
    /* the britney maneuver: "baby one more time" by prefixing 'So' */
    char * cast_name = (char*)malloc(type_len + 5);
    memset(cast_name, 0, type_len + 5);
    cast_name[0] = 'S'; cast_name[1] = 'o';
    strncpy(cast_name+2, ptr_type, type_len+2);

    if (!(swig_type = SWIG_TypeQuery(cast_name))) {
      free(cast_name); free(ptr_type);
      SWIG_fail;
    }

    free(cast_name);
  }

  free(ptr_type);

  SWIG_ConvertPtr(obj, (void**)&cast_obj, NULL, SWIG_POINTER_EXCEPTION | 0);
  if (SWIG_arg_fail(1)) { SWIG_fail; }

  return SWIG_NewPointerObj((void*)cast_obj, swig_type, own ? SWIG_POINTER_OWN : 0);
fail:
  return NULL;
}

/* a casting helper function */
SWIGEXPORT PyObject *
cast(PyObject * self, PyObject * args)
{
  char * type_name;
  Py_ssize_t type_len;
  PyObject * obj = 0;

  if (!PyArg_ParseTuple(args, "Os#:cast", &obj, &type_name, &type_len)) {
    SWIG_fail;
  }

  return cast_internal(self, obj, type_name, type_len);
fail:
  return NULL;
}

/* autocasting helper function for SoBase */
SWIGEXPORT PyObject *
autocast_base(SoBase * base, int own = 0)
{
  PyObject * result = NULL;

  /* autocast the result to the corresponding type */
  if (base && base->isOfType(SoFieldContainer::getClassTypeId())) {
    PyObject * obj = NULL;
    SoType type = base->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)base, SWIGTYPE_p_SoBase, 0);
      
      result = cast_internal(NULL, obj, type.getName().getString(),
                             type.getName().getLength(), own);

      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }      

  if (!result) {
    if (base && own) {
      result = SWIG_NewPointerObj((void*)base, SWIGTYPE_p_SoBase,
                                  SWIG_POINTER_OWN);
    } else {
      Py_INCREF(Py_None);
      result = Py_None;
    }
  }

  return result;
}

/* autocasting helper function for SoPath */
SWIGEXPORT PyObject *
autocast_path(SoPath * path)
{
  PyObject * result = NULL;
  
  /* autocast the result to the corresponding type */
  if (path) {
    PyObject * obj = NULL;
    SoType type = path->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)path, SWIGTYPE_p_SoPath, 0);
      
      result = cast_internal(NULL, obj, type.getName().getString(), type.getName().getLength());

      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* autocasting helper function for SoField */
SWIGEXPORT PyObject *
autocast_field(SoField * field, int own = 0)
{
  PyObject * result = NULL;

  /* autocast the result to the corresponding type */
  if (field) {
    PyObject * obj = NULL;
    SoType type = field->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)field, SWIGTYPE_p_SoField, 0);
      
      result = cast_internal(NULL, obj, type.getName().getString(),
                             type.getName().getLength(), own);

      Py_DECREF(obj);
      
      if (!result) { type = type.getParent(); }
    }
  }

  if (!result && field && own) {
    result = SWIG_NewPointerObj((void*)field, SWIGTYPE_p_SoField,
                                SWIG_POINTER_OWN);
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* autocasting helper function for SoEvent */
SWIGEXPORT PyObject *
autocast_event(SoEvent * event)
{
  PyObject * result = NULL;
  
  /* autocast the result to the corresponding type */
  if (event) {
    PyObject * obj = NULL;
    SoType type = event->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)event, SWIGTYPE_p_SoEvent, 0);
      
      result = cast_internal(NULL, obj, type.getName().getString(), type.getName().getLength());

      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* autocasting helper for Coin's non-SoBase ScXML object hierarchy */
SWIGEXPORT PyObject *
autocast_scxml_object(ScXMLObject * object, int own = 0)
{
  PyObject * result = NULL;
  swig_type_info * base_swig_type = SWIG_TypeQuery("ScXMLObject *");

  if (object && base_swig_type) {
    PyObject * obj = NULL;
    SoType type = object->getTypeId();

    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void *)object, base_swig_type, 0);

      result = cast_internal(NULL, obj, type.getName().getString(),
                             type.getName().getLength(), own);

      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }

  if (!result) {
    if (object && own && base_swig_type) {
      result = SWIG_NewPointerObj((void *)object, base_swig_type,
                                  SWIG_POINTER_OWN);
    } else {
      Py_INCREF(Py_None);
      result = Py_None;
    }
  }

  return result;
}

%}

/* typemaps for autocasting types through the Inventor type system */
%typemap(out) SoBase * {
  $result = autocast_base($1);
}

%typemap(out) SoFieldContainer * {
  $result = autocast_base($1);
}

%typemap(out) SoNode * {
  $result = autocast_base($1);
}

%typemap(out) SoPath * {
  $result = autocast_path($1);
}

%typemap(out) SoEngine * {
  $result = autocast_base($1);
}

%typemap(out) SoField * {
  $result = autocast_field($1);
}

%typemap(out) SoEvent * {
  $result = autocast_event($1);
}

%native(cast) PyObject * cast(PyObject * self, PyObject * args);

/**
 * SWIG - interface includes and general typemap definitions
 **/

%include "typemaps.i"
%include "cpointer.i"

/* ``cpointer.i`` does not provide Python scalar conversions for these
 * platform typedefs.  Define them before creating the pointer helper
 * classes so ``sizep.value()`` and ``timep.value()`` remain ordinary Python
 * integers instead of leaking an opaque SWIG pointer value. */
%typemap(in) size_t {
  unsigned long long value = PyLong_AsUnsignedLongLong($input);
  if (PyErr_Occurred()) {
    SWIG_fail;
  }
  if (sizeof(size_t) < sizeof(unsigned long long) &&
      value > (unsigned long long)SIZE_MAX) {
    PyErr_SetString(PyExc_OverflowError, "size_t value is out of range");
    SWIG_fail;
  }
  $1 = (size_t)value;
}

%typemap(out) size_t {
  $result = PyLong_FromUnsignedLongLong((unsigned long long)$1);
}

%typemap(typecheck) size_t {
  $1 = PyLong_Check($input) ? 1 : 0;
}

%typemap(in) time_t {
  long long value = PyLong_AsLongLong($input);
  if (PyErr_Occurred()) {
    SWIG_fail;
  }
  $1 = (time_t)value;
  if ((long long)$1 != value) {
    PyErr_SetString(PyExc_OverflowError, "time_t value is out of range");
    SWIG_fail;
  }
}

%typemap(out) time_t {
  $result = PyLong_FromLongLong((long long)$1);
}

%typemap(typecheck) time_t {
  $1 = PyLong_Check($input) ? 1 : 0;
}

%pointer_class(char, charp);
%pointer_class(short, shortp);
%pointer_class(unsigned short, ushortp);
%pointer_class(int, intp);
%pointer_class(unsigned int, uintp);
%pointer_class(signed char, int8p);
%pointer_class(unsigned char, uint8p);
%pointer_class(unsigned int, uint32p);
%pointer_class(long, longp);
%pointer_class(size_t, sizep);
%pointer_class(time_t, timep);
%pointer_class(float, floatp);
%pointer_class(double, doublep);

%{
static int
pivy_convert_numeric_sequence(PyObject * input, int kind, void ** output)
{
  Py_ssize_t length;
  Py_ssize_t index;
  size_t element_size = kind == 0 ? sizeof(int) :
                        kind == 1 ? sizeof(int32_t) : sizeof(float);
  char * storage;

  if (!PySequence_Check(input)) {
    PyErr_SetString(PyExc_TypeError, "expected a numeric sequence");
    return -1;
  }

  length = PySequence_Length(input);
  if (length < 0) return -1;
  storage = length == 0 ? NULL : (char *)malloc((size_t)length * element_size);
  if (length != 0 && storage == NULL) {
    PyErr_NoMemory();
    return -1;
  }

  for (index = 0; index < length; index++) {
    PyObject * item = PySequence_GetItem(input, index);
    if (item == NULL) {
      free(storage);
      return -1;
    }

    if (kind == 2) {
      PyObject * number = PyNumber_Float(item);
      if (number == NULL) {
        Py_DECREF(item);
        free(storage);
        return -1;
      }
      ((float *)storage)[index] = (float)PyFloat_AsDouble(number);
      Py_DECREF(number);
      if (PyErr_Occurred()) {
        Py_DECREF(item);
        free(storage);
        return -1;
      }
    } else {
      long long value = PyLong_AsLongLong(item);
      long long minimum = kind == 0 ? INT_MIN : INT32_MIN;
      long long maximum = kind == 0 ? INT_MAX : INT32_MAX;
      if (PyErr_Occurred() || value < minimum || value > maximum) {
        if (!PyErr_Occurred()) {
          PyErr_SetString(PyExc_OverflowError, "integer is outside the C range");
        }
        Py_DECREF(item);
        free(storage);
        return -1;
      }
      if (kind == 0) ((int *)storage)[index] = (int)value;
      else ((int32_t *)storage)[index] = (int32_t)value;
    }
    Py_DECREF(item);
  }

  *output = storage;
  return 0;
}

template <typename T>
static bool
pivy_convert_fixed_numeric_sequence(PyObject * input, int width, bool integer,
                                    T * output)
{
  if (!PySequence_Check(input) || PySequence_Size(input) != width) {
    PyErr_SetString(PyExc_TypeError, "expected a fixed-width numeric sequence");
    return false;
  }
  for (int index = 0; index < width; ++index) {
    PyObject * item = PySequence_GetItem(input, index);
    if (item == NULL) return false;
    if (integer) {
      long long value = PyLong_AsLongLong(item);
      if (PyErr_Occurred() ||
          value < static_cast<long long>(std::numeric_limits<T>::min()) ||
          value > static_cast<long long>(std::numeric_limits<T>::max())) {
        Py_DECREF(item);
        if (!PyErr_Occurred())
          PyErr_SetString(PyExc_OverflowError, "component is outside the C range");
        return false;
      }
      output[index] = static_cast<T>(value);
    } else {
      output[index] = static_cast<T>(PyFloat_AsDouble(item));
      if (PyErr_Occurred()) {
        Py_DECREF(item);
        return false;
      }
    }
    Py_DECREF(item);
  }
  return true;
}
%}

%define PIVY_CONST_NUMERIC_SEQUENCE_POINTER(_type_, _kind_, _name_)
%typemap(in) const _type_ * const _name_ ( _type_ * temp ) {
  if (pivy_convert_numeric_sequence($input, _kind_, (void **)&temp) < 0) {
    SWIG_fail;
  }
  $1 = temp;
}

%typemap(freearg) const _type_ * const _name_ {
  free((void *)$1);
}

%typemap(typecheck) const _type_ * const _name_ {
  $1 = PySequence_Check($input) ? 1 : 0;
}
%enddef

PIVY_CONST_NUMERIC_SEQUENCE_POINTER(int, 0, values)
PIVY_CONST_NUMERIC_SEQUENCE_POINTER(int32_t, 1, indices)
PIVY_CONST_NUMERIC_SEQUENCE_POINTER(float, 2, values)

%define PIVY_CONST_NUMERIC_SEQUENCE_POINTER_NAMED(_type_, _kind_, _name_)
%typemap(in) const _type_ * _name_ ( _type_ * temp ) {
  if (pivy_convert_numeric_sequence($input, _kind_, (void **)&temp) < 0) {
    SWIG_fail;
  }
  $1 = temp;
}

%typemap(freearg) const _type_ * _name_ {
  free((void *)$1);
}

%typemap(typecheck) const _type_ * _name_ {
  $1 = PySequence_Check($input) ? 1 : 0;
}
%enddef

PIVY_CONST_NUMERIC_SEQUENCE_POINTER_NAMED(int32_t, 1, coordindices)
PIVY_CONST_NUMERIC_SEQUENCE_POINTER_NAMED(int32_t, 1, matindices)
PIVY_CONST_NUMERIC_SEQUENCE_POINTER_NAMED(int32_t, 1, normindices)
PIVY_CONST_NUMERIC_SEQUENCE_POINTER_NAMED(int32_t, 1, texindices)
PIVY_CONST_NUMERIC_SEQUENCE_POINTER_NAMED(int, 0, indices)

%define PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(_type_, _integer_, _name_, _width_)
%typemap(in) const _type_ _name_[_width_] (_type_ temp[_width_]) {
  if (!pivy_convert_fixed_numeric_sequence($input, _width_, _integer_, temp)) {
    SWIG_fail;
  }
  $1 = temp;
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) const _type_ _name_[_width_] {
  $1 = PySequence_Check($input) && PySequence_Size($input) == _width_;
}
%enddef

PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(int8_t, 1, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(int8_t, 1, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(int8_t, 1, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(uint8_t, 1, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(uint8_t, 1, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(uint8_t, 1, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(short, 1, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(short, 1, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(short, 1, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(unsigned short, 1, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(unsigned short, 1, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(unsigned short, 1, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(int32_t, 1, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(int32_t, 1, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(int32_t, 1, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(uint32_t, 1, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(uint32_t, 1, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(uint32_t, 1, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(float, 0, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(float, 0, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(float, 0, xyzw, 4)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(double, 0, xy, 2)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(double, 0, xyz, 3)
PIVY_FIXED_NUMERIC_ARRAY_PARAMETER(double, 0, xyzw, 4)

/* if SWIG determines the class abstract it doesn't generate
 * constructors of any kind. the following %feature
 * declarations take care about this for the classes we still
 * want a constructor for.
 */
%feature("notabstract") SoBoolOperation;
%feature("notabstract") SoComposeRotation;
%feature("notabstract") SoComposeVec3f;
%feature("notabstract") SoDecomposeVec3f;

%rename(output) print(FILE * fp) const;
%rename(output) print(FILE * const fp) const;
%rename(output) print(FILE * const file = stdout) const;
%rename(srcFrom) from;
%rename(destTo) to;

/* generic typemaps to allow using python types instead of instances
 * within the python interpreter
 */
%typemap(in) int32_t = int;
%typemap(out) int32_t = int;
%typemap(typecheck) int32_t = int;

%typemap(in) uint32_t = unsigned int;
%typemap(out) uint32_t = unsigned int;
%typemap(typecheck) uint32_t = unsigned int;

%typemap(typecheck) SbName & {
  void *ptr = NULL;
  $1 = 1;
#ifdef PY_2
  if (!PyString_Check($input) && 
     (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbName, 0) == -1)) 
#else
  if (!PyBytes_Check($input) && 
    !PyUnicode_Check($input) && 
    (SWIG_ConvertPtr($input, (void**)(&ptr), $descriptor(SbName *), 0) == -1))
#endif
  {
    $1 = 0;
  }
}

%typemap(in) SbName & {
#ifdef PY_2
  if (PyString_Check($input))
  {
    $1 = new SbName(PyString_AsString($input));
  }
#else
  if (PyBytes_Check($input))
  {
    $1 = new SbName(PyBytes_AsString($input));
  }
  else if  (PyUnicode_Check($input)){
    $1 = new SbName(PyBytes_AsString(PyUnicode_AsEncodedString($input, "utf-8", "strict")));
  }
#endif
   else {
    SbName * tmp = NULL;
    $1 = new SbName;
#ifdef PY_2
    SWIG_ConvertPtr($input, (void**)&tmp, SWIGTYPE_p_SbName, 1);
#else
    SWIG_ConvertPtr($input, (void**)&tmp,  $descriptor(SbName *), 1);
#endif
    *$1 = *tmp;
  }
}

%typemap(freearg) SbName & {
  if ($1) { delete $1; }
}

%typemap(typecheck) SbName {
  void *ptr = NULL;
  $1 = 1;
#ifdef PY_2
  if (!PyString_Check($input) && 
      !PyUnicode_Check($input) && 
     (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbName, 0) == -1))
#else       
  // http://stackoverflow.com/questions/2807887/cs-char-by-swig-got-problem-in-python-3-0
  if (!PyBytes_Check($input) &&
     !PyUnicode_Check($input) && 
     (SWIG_ConvertPtr($input, (void**)(&ptr), $descriptor(SbString *), 0) == -1))
#endif 
  {
    $1 = 0;
  }
}

%typemap(in) SbName {
#ifdef PY_2
  if (PyString_Check($input)){
    $1 = SbName(PyString_AsString($input));
  }
#else
  if (PyBytes_Check($input)){
    $1 = SbName(PyBytes_AsString($input));
  }
  else if  (PyUnicode_Check($input)){
    $1 = SbName(PyBytes_AsString(PyUnicode_AsEncodedString($input, "utf-8", "strict")));
  }
#endif
  else {
    SbName * namePtr;
#ifdef PY_2
    SWIG_ConvertPtr($input, (void**)&namePtr, SWIGTYPE_p_SbName, 1);
#else
    SWIG_ConvertPtr($input, (void**)&namePtr, $descriptor(SbName *), 1);
#endif
    $1 = *namePtr;
  }
}

%typemap(typecheck) SbString & {
  void *ptr = NULL;
  $1 = 1;
#ifdef PY_2
  if (!PyString_Check($input) && 
     (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbString, 0) == -1)) 
#else
  if (!PyBytes_Check($input) &&
      !PyUnicode_Check($input) && 
     (SWIG_ConvertPtr($input, (void**)(&ptr), $descriptor(SbString *), 0) == -1))
#endif
  {
    $1 = 0;
  }
}

%typemap(in) SbString & {
#ifdef PY_2
  if (PyString_Check($input))  
  {
    $1 = new SbString(PyString_AsString($input));
  }
#else
  if (PyBytes_Check($input))  
  {
    $1 = new SbString(PyBytes_AsString($input));
  }
  else if  (PyUnicode_Check($input)){
     $1 = new SbString(PyBytes_AsString(PyUnicode_AsEncodedString($input, "utf-8", "strict")));
  }
#endif
  else {
    SbString * tmp = NULL;
    $1 = new SbString;
#ifdef PY_2
    SWIG_ConvertPtr($input, (void**)&tmp, SWIGTYPE_p_SbString, 1);
#else
    SWIG_ConvertPtr($input, (void**)&tmp, $descriptor(SbString *), 1);
#endif
    *$1 = *tmp;
  }
}

%typemap(freearg) SbString & {
  if ($1) { delete $1; }
}

%typemap(typecheck) SbTime & {
  void *ptr = NULL;
  $1 = 1;
#ifdef PY_2
  if (!PyFloat_Check($input) && (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbTime, 0) == -1))
#else
  if (!PyFloat_Check($input) && (SWIG_ConvertPtr($input, (void**)(&ptr), $descriptor(SbTime *), 0) == -1))
#endif
  {
    $1 = 0;
  }
}

%typemap(in) SbTime & {
  if (PyFloat_Check($input)) {
    $1 = new SbTime(PyFloat_AsDouble($input));
  } else {
    SbTime * tmp = NULL;
    $1 = new SbTime;
#ifdef PY_2
    SWIG_ConvertPtr($input, (void**)&tmp, SWIGTYPE_p_SbTime, 1);
#else
    SWIG_ConvertPtr($input, (void**)&tmp, $descriptor(SbTime *), 1);
#endif
    *$1 = *tmp;
  }
}

%typemap(freearg) SbTime & {
  if ($1) { delete $1; }
}

%typemap(in) FILE * {
#ifdef PY_2
  if (PyFile_Check($input)) {
    $1 = PyFile_AsFile($input);
  }
#else
  if (PyObject_IsInstance($input, PyIOBase_TypeObj)) {
    int fd = PyObject_AsFileDescriptor($input);
    $1 = fdopen(fd, "w");
  }
#endif
  else {
    PyErr_SetString(PyExc_TypeError, "expected a file object.");
  }
}

%include Inventor/events/SoEvent.h
%include Inventor/fields/SoField.h
%include Inventor/SbString.h

/* some ignores for missing COIN_DLL_API specifications */
%ignore cc_rbptree_init;
%ignore cc_rbptree_clean;
%ignore cc_rbptree_insert;
%ignore cc_rbptree_remove;
%ignore cc_rbptree_size;
%ignore cc_rbptree_traverse;
%ignore cc_rbptree_debug;
%ignore so_plane_data::so_plane_data;
%ignore SoGLRenderCache::SoGLRenderCache;
%ignore SoGLRenderCache::open;
%ignore SoGLRenderCache::close;
%ignore SoGLRenderCache::call;
%ignore SoGLRenderCache::getCacheContext;
%ignore SoGLRenderCache::getPreLazyState;
%ignore SoGLRenderCache::getPostLazyState;
%ignore SoGLCacheList::SoGLCacheList;
%ignore SoGLCacheList::~SoGLCacheList;
%ignore SoGLCacheList::call;
%ignore SoGLCacheList::open;
%ignore SoGLCacheList::close;
%ignore SoGLCacheList::invalidateAll;
%ignore SoNormalBundle::SoNormalBundle;
%ignore SoNormalBundle::~SoNormalBundle;
%ignore SoNormalBundle::shouldGenerate;
%ignore SoNormalBundle::initGenerator;
%ignore SoNormalBundle::beginPolygon;
%ignore SoNormalBundle::polygonVertex;
%ignore SoNormalBundle::endPolygon;
%ignore SoNormalBundle::triangle;
%ignore SoNormalBundle::generate;
%ignore SoNormalBundle::getGeneratedNormals;
%ignore SoNormalBundle::getNumGeneratedNormals;
%ignore SoNormalBundle::set;
%ignore SoNormalBundle::get;
%ignore SoNormalBundle::send;

%ignore SoMultiTextureCoordinateElement::setFunction;
%ignore SoGLMultiTextureCoordinateElement::setTexGen;
