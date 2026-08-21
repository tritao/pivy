%{
static void
SoSensorPythonCB(void * data, SoSensor * sensor)
{
  PyGILState_STATE gil = PyGILState_Ensure();
  swig_type_info * swig_type = 0;
  const char * sensor_cast_name = NULL;
  PyObject * func, * arglist;
  PyObject * result, * pysensor;

  /* the first item in the data sequence is the python callback
   * function; the second item is the supplied data python object; the
   * third item contains the sensor type that we should create */
#ifdef PY_2
    sensor_cast_name = PyString_AsString(PyTuple_GetItem((PyObject *)data, 2));
#else
    PyObject* item = PyTuple_GetItem((PyObject *)data, 2);
    if (PyUnicode_Check(item)){
    sensor_cast_name = PyUnicode_AsUTF8(item);
    }
    else if (PyBytes_Check(item)){
      sensor_cast_name = PyBytes_AsString(item);
    }

#endif
  if (!sensor_cast_name){
    PyErr_SetString(PyExc_TypeError, "Sensor type query failed.");
    return;
  }
  else if (!(swig_type = SWIG_TypeQuery(sensor_cast_name))) {
    PyErr_SetString(PyExc_TypeError, "Sensor type query failed.");
    return;
  }
  pysensor = SWIG_NewPointerObj((void *)sensor, swig_type, 0);

  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("(OO)", PyTuple_GetItem((PyObject *)data, 1), pysensor);

  if ((result = PyObject_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_DECREF(pysensor);
  Py_XDECREF(result);
  
  PyGILState_Release(gil);
}
%}

%typemap(in) SoSensorCB * {
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = SoSensorPythonCB;
}

%typemap(typecheck) SoSensorCB * {
  $1 = PyCallable_Check($input) ? 1 : 0;
}

%typemap(in) void * data {
  if (!PyTuple_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "tuple expected!");
    return NULL;
  }

  Py_INCREF($input);
  $1 = (void *)$input;
}

%typemap(typecheck) void * data {
  $1 = PyTuple_Check($input) ? 1 : 0;
}

%typemap(in) void * callbackdata {
  if (!PyTuple_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "tuple expected!");
    return NULL;
  }

  Py_INCREF($input);
  $1 = (void *)$input;
}

%typemap(typecheck) void * callbackdata {
  $1 = PyTuple_Check($input) ? 1 : 0;
}

%feature("shadow") SoSensor::setFunction %{
def setFunction(self, callbackfunction):
   """setFunction(SoSensor self, SoSensorCB * callbackfunction)"""
   if not callable(callbackfunction):
      raise TypeError("need a callable object!")

   callback_data = getattr(self, "_pivy_sensor_callback_data", None)
   if callback_data is None:
      callback_data = (callbackfunction, None, type(self).__name__ + " *")
   else:
      callback_data = (callbackfunction, callback_data[1], callback_data[2])

   self._pivy_sensor_callback_data = callback_data
   _coin.SoSensor_setData(self, callback_data)
   return _coin.SoSensor_setFunction(self, callbackfunction)
%}

%feature("shadow") SoSensor::getFunction %{
def getFunction(self):
   """getFunction(SoSensor self) -> SoSensorCB *"""
   callback_data = getattr(self, "_pivy_sensor_callback_data", None)
   if callback_data is None:
      return None
   return callback_data[0]
%}

%feature("shadow") SoSensor::getData %{
def getData(self):
   """getData(SoSensor self) -> void *"""
   callback_data = getattr(self, "_pivy_sensor_callback_data", None)
   if callback_data is None:
      return None
   return callback_data[1]
%}
