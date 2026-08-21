%rename(SoDataSensor_scb_v) SoDataSensor::SoDataSensor(SoSensorCB * func, void * data);

%feature("shadow") SoDataSensor::setDeleteCallback %{
def setDeleteCallback(self, function, data=None):
   """setDeleteCallback(SoDataSensor self, SoSensorCB * function, void * data=None)"""
   if not callable(function):
      raise TypeError("need a callable object!")

   callback_data = (function, data, type(self).__name__ + " *")
   self._pivy_sensor_delete_callback_data = callback_data
   return _coin.SoDataSensor_setDeleteCallback(self, function, callback_data)
%}

%feature("shadow") SoDataSensor::SoDataSensor %{
def __init__(self, *args):
   newobj = None
   callback_data = None
   if len(args) == 2:
      callback_data = (args[0], args[1], "SoDataSensor *")
      args = (args[0], callback_data)
      newobj = _coin.new_SoDataSensor_scb_v(*args)
   else:
      self.this = _coin.new_SoDataSensor(*args)
      self.thisown = 1
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      if callback_data is not None:
         self._pivy_sensor_callback_data = callback_data
%}
