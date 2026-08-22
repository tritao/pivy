# pyright: reportMissingModuleSource=false

from typing import assert_type

from pivy import coin


def sensor_callback(data: object, sensor: coin.SoSensor) -> None:
    pass


def check_sensor_lifecycle() -> None:
    def timer_callback(data: object, sensor: coin.SoTimerSensor) -> None:
        pass

    def alarm_callback(data: object, sensor: coin.SoAlarmSensor) -> None:
        pass

    def idle_callback(data: object, sensor: coin.SoIdleSensor) -> None:
        pass

    def oneshot_callback(data: object, sensor: coin.SoOneShotSensor) -> None:
        pass

    timer = coin.SoTimerSensor(timer_callback, None)
    alarm = coin.SoAlarmSensor(alarm_callback, None)
    idle = coin.SoIdleSensor(idle_callback, None)
    oneshot = coin.SoOneShotSensor(oneshot_callback, None)

    assert_type(timer, coin.SoTimerSensor)
    assert_type(alarm, coin.SoAlarmSensor)
    assert_type(idle, coin.SoIdleSensor)
    assert_type(oneshot, coin.SoOneShotSensor)

    for sensor in (timer, alarm, idle, oneshot):
        assert_type(sensor.isScheduled(), bool)
        assert_type(sensor.getNextInQueue(), coin.SoSensor | None)
        sensor.schedule()
        sensor.unschedule()
        sensor.trigger()

    assert_type(timer.getTriggerTime(), coin.SbTime)
    assert_type(timer.getBaseTime(), coin.SbTime)
    assert_type(timer.getInterval(), coin.SbTime)
    timer.setBaseTime(coin.SbTime())
    timer.setInterval(coin.SbTime())
    timer.reschedule(coin.SbTime())

    assert_type(alarm.getTriggerTime(), coin.SbTime)
    assert_type(alarm.getTime(), coin.SbTime)
    alarm.setTime(coin.SbTime())
    alarm.setTimeFromNow(coin.SbTime())


def check_delay_sensor_contract() -> None:
    delay = coin.SoDelayQueueSensor(sensor_callback, None)
    assert_type(delay.getPriority(), int)
    assert_type(delay.getDefaultPriority(), int)
    assert_type(delay.isIdleOnly(), bool)
    delay.setPriority(1)


def check_data_sensor_contract() -> None:
    def field_callback(data: object, sensor: coin.SoFieldSensor) -> None:
        pass

    def node_callback(data: object, sensor: coin.SoNodeSensor) -> None:
        pass

    def path_callback(data: object, sensor: coin.SoPathSensor) -> None:
        pass

    field = coin.SoFieldSensor(field_callback, None)
    node = coin.SoNodeSensor(node_callback, None)
    path = coin.SoPathSensor(path_callback, None)

    for sensor in (field, node, path):
        assert_type(sensor.getTriggerNode(), coin.SoNode | None)
        assert_type(sensor.getTriggerField(), coin.SoField | None)
        assert_type(sensor.getTriggerPath(), coin.SoPath | None)
        assert_type(sensor.getTriggerGroupChild(), coin.SoNode | None)
        assert_type(sensor.getTriggerReplacedGroupChild(), coin.SoNode | None)
        assert_type(sensor.getTriggerPathFlag(), bool)
        assert_type(sensor.getTriggerOperationType(), int)
        assert_type(sensor.getTriggerIndex(), int)
        assert_type(sensor.getTriggerFieldNumIndices(), int)
        sensor.setTriggerPathFlag(True)

    assert_type(field.getAttachedField(), coin.SoField | None)
    field.attach(coin.SoCube().width)
    field.detach()

    assert_type(node.getAttachedNode(), coin.SoNode | None)
    node.attach(coin.SoCube())
    node.detach()

    assert_type(path.getAttachedPath(), coin.SoPath | None)
    path.attach(coin.SoPath())
    path.detach()
    assert_type(path.getTriggerFilter(), int)
    path.setTriggerFilter(coin.SoPathSensor.PATH_AND_NODES)


def check_sensor_manager_contract() -> None:
    manager = coin.SoDB.getSensorManager()
    assert_type(manager.isDelaySensorPending(), bool)
    assert_type(manager.isTimerSensorPending(), coin.SbTime | None)
    assert_type(manager.isTimerSensorPending(coin.SbTime()), bool)
    assert_type(manager.getDelaySensorTimeout(), coin.SbTime)
    manager.setDelaySensorTimeout(coin.SbTime())
    manager.processImmediateQueue()
    manager.processDelayQueue(False)
    manager.processTimerQueue()
