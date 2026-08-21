%rename(SoFieldSensor_scb_v) SoFieldSensor::SoFieldSensor(SoSensorCB * func, void * data);

%feature("shadow") SoFieldSensor::SoFieldSensor %{
def __init__(self, *args):
   newobj = None
   callback_data = None
   if len(args) == 2:
      callback_data = (args[0], args[1], "SoFieldSensor *")
      args = (args[0], callback_data)
      newobj = _coin.new_SoFieldSensor_scb_v(*args)
   else:
      self.this = _coin.new_SoFieldSensor(*args)
      self.thisown = 1
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      if callback_data is not None:
         self._pivy_sensor_callback_data = callback_data
%}
