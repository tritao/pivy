%rename(SoDelayQueueSensor_scb_v) SoDelayQueueSensor::SoDelayQueueSensor(SoSensorCB * func, void * data);

%feature("shadow") SoDelayQueueSensor::SoDelayQueueSensor %{
def __init__(self, *args):
   newobj = None
   callback_data = None
   if len(args) == 2:
      callback_data = (args[0], args[1], "SoDelayQueueSensor *")
      args = (args[0], callback_data)
      newobj = _coin.new_SoDelayQueueSensor_scb_v(*args)
   else:
      self.this = _coin.new_SoDelayQueueSensor(*args)
      self.thisown = 1
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      if callback_data is not None:
         self._pivy_sensor_callback_data = callback_data
%}
