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

%define COIN_MODULE_DOCSTRING
"Pivy is a Coin binding for Python. Coin is a high-level 3D graphics
library with a C++ Application Programming Interface. Coin uses
scene-graph data structures to render real-time graphics suitable for
mostly all kinds of scientific and engineering visualization
applications."
%enddef

%module(package="pivy", docstring=COIN_MODULE_DOCSTRING) coin

// stdint is not wrapped automatically anymore with swig4.0
// https://stackoverflow.com/questions/40959436/swig-python-detected-a-memory-leak-of-type-uint32-t-no-destructor-found
%include "stdint.i"

%begin %{
#define PY_SSIZE_T_CLEAN
%}

%{
#if defined(_WIN32) || defined(__WIN32__)
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#endif

#undef ANY

#include "coin_header_includes.h"
#include <limits.h>

/* make GLState in SoGLLazyElement known to SWIG */
typedef SoGLLazyElement::GLState GLState;
%}

/* enable autodoc'ing for the generated wrapper */
%feature("autodoc", "1");

/* let SWIG handle reference counting for all SoBase derived classes */
%feature("ref") SoBase "$this->ref();"
%feature("unref") SoBase "$this->unref();"

%{
/*
  Workaround for FILE* typemap. Import IO module instead of using extern PyTypeObject PyIOBase_Type,
  because the windows python lib does not export PyIOBase_Type.
  Copied from: https://github.com/Kagami/pygraphviz/commit/fe442dc16accb629c3feaf157af75f67ccabbd6e
*/
#if PY_MAJOR_VERSION >= 3
static PyObject *PyIOBase_TypeObj;

static int init_file_emulator(void)
{
    PyObject *io = PyImport_ImportModule("_io");
    if (io == NULL)
        return -1;
    PyIOBase_TypeObj = PyObject_GetAttrString(io, "_IOBase");
    if (PyIOBase_TypeObj == NULL)
        return -1;
    return 0;
}
#endif
%}

%init %{
#if PY_MAJOR_VERSION >= 3
if (init_file_emulator() < 0) {
  #if (SWIG_VERSION < 0x040400)
    return NULL;
  #else
    return 0;
  #endif
}
#endif
%}

/* include the typemaps common to all pivy modules */
%include pivy_common_typemaps.i
%ignore SoDepthBufferElement::get;
%include coin_header_includes.h

/* Return scalar box output parameters as owned Python tuples.  The native
   short-reference overloads have no usable Python proxy type, while the
   vector overloads require callers to allocate temporary wrappers. */
%extend SbBox2s {
  PyObject *_pivy_getBoundsTuple() const {
    short xmin, ymin, xmax, ymax;
    self->getBounds(xmin, ymin, xmax, ymax);
    return Py_BuildValue("(hhhh)", xmin, ymin, xmax, ymax);
  }

  PyObject *_pivy_getOriginTuple() const {
    short originX, originY;
    self->getOrigin(originX, originY);
    return Py_BuildValue("(hh)", originX, originY);
  }
}

%extend SbBox3s {
  PyObject *_pivy_getBoundsTuple() const {
    short xmin, ymin, zmin, xmax, ymax, zmax;
    self->getBounds(xmin, ymin, zmin, xmax, ymax, zmax);
    return Py_BuildValue("(hhhhhh)", xmin, ymin, zmin, xmax, ymax, zmax);
  }

  PyObject *_pivy_getOriginTuple() const {
    short originX, originY, originZ;
    self->getOrigin(originX, originY, originZ);
    return Py_BuildValue("(hhh)", originX, originY, originZ);
  }
}

%extend SbBox2i32 {
  PyObject *_pivy_getBoundsTuple() const {
    int32_t xmin, ymin, xmax, ymax;
    self->getBounds(xmin, ymin, xmax, ymax);
    return Py_BuildValue("(iiii)", xmin, ymin, xmax, ymax);
  }

  PyObject *_pivy_getOriginTuple() const {
    int32_t originX, originY;
    self->getOrigin(originX, originY);
    return Py_BuildValue("(ii)", originX, originY);
  }
}

%extend SbBox3i32 {
  PyObject *_pivy_getBoundsTuple() const {
    int32_t xmin, ymin, zmin, xmax, ymax, zmax;
    self->getBounds(xmin, ymin, zmin, xmax, ymax, zmax);
    return Py_BuildValue("(iiiiii)", xmin, ymin, zmin, xmax, ymax, zmax);
  }

  PyObject *_pivy_getOriginTuple() const {
    int32_t originX, originY, originZ;
    self->getOrigin(originX, originY, originZ);
    return Py_BuildValue("(iii)", originX, originY, originZ);
  }
}

%pythoncode %{
SbBox2s.getBounds = lambda self: self._pivy_getBoundsTuple()
SbBox2s.getOrigin = lambda self: self._pivy_getOriginTuple()
SbBox3s.getBounds = lambda self: self._pivy_getBoundsTuple()
SbBox3s.getOrigin = lambda self: self._pivy_getOriginTuple()
SbBox2i32.getBounds = lambda self: self._pivy_getBoundsTuple()
SbBox2i32.getOrigin = lambda self: self._pivy_getOriginTuple()
SbBox3i32.getBounds = lambda self: self._pivy_getBoundsTuple()
SbBox3i32.getOrigin = lambda self: self._pivy_getOriginTuple()
%}

/* Return an owned Python snapshot instead of exposing SoColorPacker's
   borrowed internal uint32_t array.  This extension is declared after the
   aggregate Coin header so SWIG has seen the complete class definition. */
%extend SoColorPacker {
  PyObject *_pivy_getPackedColorsBytes() const {
    return PyBytes_FromStringAndSize(
      (const char *)self->getPackedColors(),
      self->getSize() * sizeof(uint32_t));
  }
}

%pythoncode %{
SoColorPacker.getPackedColors = (
    lambda self: self._pivy_getPackedColorsBytes()
)
%}

/* SoMFDouble's native sequence operators are not wrapped by SWIG because
   its values are exposed only as a const double pointer.  Copy the bounded
   field contents while the field owns them instead of leaking that pointer
   into Python. */
%extend SoMFDouble {
  PyObject *_pivy_setValuesArguments(PyObject *arguments) {
    if (!PyTuple_Check(arguments)) {
      PyErr_SetString(
          PyExc_TypeError,
          "SoMFDouble.setValues expects a positional argument tuple");
      return NULL;
    }

    const Py_ssize_t argument_count = PyTuple_GET_SIZE(arguments);
    int start = 0;
    int num = -1;
    PyObject *values_object = NULL;

    if (argument_count == 1) {
      values_object = PyTuple_GET_ITEM(arguments, 0);
    } else if (argument_count == 2 || argument_count == 3) {
      long parsed_start = PyLong_AsLong(PyTuple_GET_ITEM(arguments, 0));
      if (PyErr_Occurred()) return NULL;
      if (parsed_start < INT_MIN || parsed_start > INT_MAX) {
        PyErr_SetString(PyExc_OverflowError, "SoMFDouble.setValues start is out of range");
        return NULL;
      }
      start = (int)parsed_start;
      if (argument_count == 2) {
        values_object = PyTuple_GET_ITEM(arguments, 1);
      } else {
        long parsed_num = PyLong_AsLong(PyTuple_GET_ITEM(arguments, 1));
        if (PyErr_Occurred()) return NULL;
        if (parsed_num < 0 || parsed_num > INT_MAX) {
          PyErr_SetString(PyExc_OverflowError, "SoMFDouble.setValues count is out of range");
          return NULL;
        }
        num = (int)parsed_num;
        values_object = PyTuple_GET_ITEM(arguments, 2);
      }
    } else {
      PyErr_SetString(
          PyExc_TypeError,
          "SoMFDouble.setValues expects values, start/values, or start/count/values");
      return NULL;
    }

    PyObject *values = PySequence_Fast(
        values_object, "SoMFDouble.setValues expects a numeric sequence");
    if (values == NULL) return NULL;

    Py_ssize_t length = PySequence_Fast_GET_SIZE(values);
    if (num < 0) num = (int)length;
    if (length != num) {
      PyErr_Format(
          PyExc_ValueError,
          "SoMFDouble.setValues expected %d values, got %zd",
          num, length);
      Py_DECREF(values);
      return NULL;
    }

    double *storage = NULL;
    if (num > 0) {
      storage = (double *)PyMem_Malloc((size_t)num * sizeof(double));
      if (storage == NULL) {
        Py_DECREF(values);
        return PyErr_NoMemory();
      }
    }

    for (int index = 0; index < num; ++index) {
      PyObject *number = PyNumber_Float(
          PySequence_Fast_GET_ITEM(values, index));
      if (number == NULL) {
        PyMem_Free(storage);
        Py_DECREF(values);
        return NULL;
      }
      storage[index] = PyFloat_AsDouble(number);
      Py_DECREF(number);
      if (PyErr_Occurred()) {
        PyMem_Free(storage);
        Py_DECREF(values);
        return NULL;
      }
    }

    self->setValues(start, num, storage);
    PyMem_Free(storage);
    Py_DECREF(values);
    Py_RETURN_NONE;
  }

  PyObject *_pivy_getValuesSnapshot(int start) const {
    const int count = self->getNum();
    if (start < 0 || start > count) {
      PyErr_SetString(
          PyExc_IndexError,
          "SoMFDouble.getValues start is outside the field");
      return NULL;
    }

    const int snapshot_count = count - start;
    PyObject *snapshot = PyList_New(snapshot_count);
    if (snapshot == NULL) return NULL;
    if (snapshot_count == 0) return snapshot;

    const double *values = self->getValues(start);
    for (int index = 0; index < snapshot_count; ++index) {
      PyObject *value = PyFloat_FromDouble(values[index]);
      if (value == NULL) {
        Py_DECREF(snapshot);
        return NULL;
      }
      PyList_SET_ITEM(snapshot, index, value);
    }
    return snapshot;
  }

  PyObject *__getitem__(int index) const {
    const int count = self->getNum();
    if (index < 0) index += count;
    if (index < 0 || index >= count) {
      PyErr_SetString(PyExc_IndexError, "SoMFDouble index is out of range");
      return NULL;
    }
    return PyFloat_FromDouble(self->getValues(0)[index]);
  }

  PyObject *__setitem__(int index, double value) {
    const int count = self->getNum();
    if (index < 0) index += count;
    if (index < 0 || index >= count) {
      PyErr_SetString(PyExc_IndexError, "SoMFDouble index is out of range");
      return NULL;
    }
    self->set1Value(index, value);
    Py_RETURN_NONE;
  }
}

%pythoncode %{
def _pivy_getValues(self, start=0):
  return self._pivy_getValuesSnapshot(start)

SoMFDouble.getValuesSnapshot = lambda self: self._pivy_getValuesSnapshot(0)
SoMFDouble.getValues = _pivy_getValues

SoMFDouble._pivy_setValuesRaw = SoMFDouble.setValues
SoMFDouble.setValues = lambda self, *args: self._pivy_setValuesArguments(args)
%}

/* Return an owned snapshot for SoByteStream's internal buffer. */
%extend SoByteStream {
  PyObject *_pivy_getDataBytes() {
    return PyBytes_FromStringAndSize(
      (const char *)self->getData(),
      self->getNumBytes());
  }
}

%pythoncode %{
SoByteStream.getData = lambda self: self._pivy_getDataBytes()
%}

/* Expose SbByteBuffer::data() as an owned Python bytes snapshot.  SWIG's
   default char * conversion treats the pointer as text and can leak both
   embedded NULs and the buffer's lifetime semantics into Python. */
%extend SbByteBuffer {
  PyObject *_pivy_data_bytes() {
    const size_t size = self->size();
    if (size > (size_t)PY_SSIZE_T_MAX) {
      PyErr_SetString(PyExc_OverflowError, "SbByteBuffer is too large");
      return NULL;
    }
    return PyBytes_FromStringAndSize(self->data(), (Py_ssize_t)size);
  }
}

%pythoncode %{
SbByteBuffer.data = lambda self: self._pivy_data_bytes()
%}

%include "Inventor/nodes/SoExtSelection.i"

/* Coin 4.0.7 leaves these ScXML factories as void * even though the
   concrete Python proxy is available.  The runtime type IDs for these
   classes are incomplete, so use the explicit SWIG cast and transfer the
   factory's ownership to the typed proxy. */
%pythoncode %{
def _pivy_scxml_factory(native_factory, class_name):
  object_ = cast(native_factory(), class_name)
  object_.thisown = True
  return object_

ScXMLInExprDataObj.createInstance = staticmethod(
    lambda: _pivy_scxml_factory(
        _coin.ScXMLInExprDataObj_createInstance, "ScXMLInExprDataObj"
    )
)
ScXMLAppendOpExprDataObj.createInstance = staticmethod(
    lambda: _pivy_scxml_factory(
        _coin.ScXMLAppendOpExprDataObj_createInstance,
        "ScXMLAppendOpExprDataObj",
    )
)
ScXMLScriptElt.createInstance = staticmethod(
    lambda: _pivy_scxml_factory(
        _coin.ScXMLScriptElt_createInstance, "ScXMLScriptElt"
    )
)
%}

/* Coin's enum reference is represented by its underlying integer in the
   Python binding, just like the other scalar output references. */
%rename(get) SoDepthBufferElement::getInt;
%extend SoDepthBufferElement {
  static void getInt(SoState * state, int & test_out, int & write_out,
                     int & function_out, SbVec2f & range_out) {
    SbBool test;
    SbBool write;
    SoDepthBufferElement::DepthWriteFunction function;
    SoDepthBufferElement::get(
      state,
      test,
      write,
      function,
      range_out);
    test_out = static_cast<int>(test);
    write_out = static_cast<int>(write);
    function_out = static_cast<int>(function);
  }
}

/*
  removes all the properties for fields in classes derived from
  SoFieldContainer. this makes way for the dynamic access to fields
  as attributes.
  
  Note: this has to be the last code in the pivy file, therefore it
  is after all other SWIG declarations!
*/

%pythoncode %{        
for key in list(locals()):
  x = locals()[key]
  if isinstance(x, type) and issubclass(x, SoFieldContainer):
    for name in list(x.__dict__):
      thing = x.__dict__[name]
      if isinstance(thing, property):
        delattr(x, name)
del key, x, name, thing
%}
