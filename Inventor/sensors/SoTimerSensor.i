%rename(SoTimerSensor_scb_v) SoTimerSensor::SoTimerSensor(SoSensorCB * func, void * data);

%feature("shadow") SoTimerSensor::SoTimerSensor %{
def __init__(self, *args):
   newobj = None
   callback_data = None
   if len(args) == 2:
      callback_data = (args[0], args[1], "SoTimerSensor *")
      args = (args[0], callback_data)
      newobj = _coin.new_SoTimerSensor_scb_v(*args)
   else:
      self.this = _coin.new_SoTimerSensor(*args)
      self.thisown = 1


   if newobj:
      self.this = newobj.this
      self.thisown = 1
      if callback_data is not None:
         self._pivy_sensor_callback_data = callback_data
%}
