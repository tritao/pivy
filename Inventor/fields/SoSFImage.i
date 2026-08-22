%typemap(in,numinputs=0) (SbVec2s & size, int & nc) (int temp) {
   $1 = new SbVec2s();
   $2 = &temp;
}

%typemap(argout) (SbVec2s & size, int & nc) {
  Py_XDECREF($result); /* free up any previous result */
#ifdef PY_2
  $result = Py_BuildValue("(s#Oi)",
                          (const char *)result,
                          (*$1)[0] * (*$1)[1] * (*$2),
                          SWIG_NewPointerObj((void *)$1, SWIGTYPE_p_SbVec2s, 1),
                          *$2);
#else
  PyObject *pixels = PyBytes_FromStringAndSize(
      (const char *)result, (*$1)[0] * (*$1)[1] * (*$2));
  PyObject *size = SWIG_NewPointerObj(
      (void *)$1, SWIGTYPE_p_SbVec2s, 1);
  $result = Py_BuildValue("(OOi)", pixels, size, *$2);
  Py_DECREF(pixels);
  Py_DECREF(size);
#endif
}

%extend SoSFImage {
  /* Snapshot a borrowed subtexture pointer before it crosses into Python.
     The native API exposes dimensions and offset through output references;
     returning owned values keeps both the pixel lifetime and output storage
     independent from the field. */
  PyObject *getSubTextureValue(const int idx) {
    SbVec2s image_size(0, 0);
    SbVec2s dims(0, 0);
    SbVec2s offset(0, 0);
    int numcomps = 0;
    const unsigned char *pixels = NULL;
    Py_ssize_t pixel_count = 0;
    PyObject *pixel_object = NULL;
    PyObject *dims_object = NULL;
    PyObject *offset_object = NULL;
    PyObject *result = NULL;

    self->getValue(image_size, numcomps);
    pixels = self->getSubTexture(idx, dims, offset);
    if (pixels == NULL) {
      Py_INCREF(Py_None);
      pixel_object = Py_None;
    } else {
      if (dims[0] > 0 && dims[1] > 0 && numcomps > 0) {
        pixel_count = (Py_ssize_t)dims[0] * (Py_ssize_t)dims[1] * numcomps;
      }
      pixel_object = PyBytes_FromStringAndSize(
        (const char *)pixels, pixel_count);
      if (pixel_object == NULL) {
        return NULL;
      }
    }

    dims_object = SWIG_NewPointerObj(
      (void *)new SbVec2s(dims),
      SWIGTYPE_p_SbVec2s,
      SWIG_POINTER_OWN);
    if (dims_object == NULL) {
      Py_DECREF(pixel_object);
      return NULL;
    }
    offset_object = SWIG_NewPointerObj(
      (void *)new SbVec2s(offset),
      SWIGTYPE_p_SbVec2s,
      SWIG_POINTER_OWN);
    if (offset_object == NULL) {
      Py_DECREF(pixel_object);
      Py_DECREF(dims_object);
      return NULL;
    }

    result = Py_BuildValue(
      "(OOOi)", pixel_object, dims_object, offset_object, numcomps);
    Py_DECREF(pixel_object);
    Py_DECREF(dims_object);
    Py_DECREF(offset_object);
    return result;
  }

  void setValue(const SbVec2s & size, const int nc, PyObject * pixels)
  {
    Py_ssize_t len = size[0] * size[1] * nc;
    unsigned char * image;
#ifdef PY_2
    PyString_AsStringAndSize(pixels, (char **)&image, &len);
#else
    PyObject *  b_pixels = pixels;
    if  (PyUnicode_Check(pixels)){
      b_pixels = PyUnicode_AsEncodedString(pixels, "utf-8", "strict");
    }
    PyBytes_AsStringAndSize(b_pixels, (char **)&image, &len);
#endif
    self->setValue(size, nc, image);
  }

  void setValue(const SoSFImage * other) { *self = *other; }
}
