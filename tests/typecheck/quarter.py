# pyright: reportMissingModuleSource=false

from typing import assert_type

from pivy import coin
from pivy.qt import QtCore, QtGui
from pivy.qt.QtWidgets import QMenu
from pivy.quarter.QuarterWidget import QuarterWidget
from pivy.quarter.devices.DeviceManager import DeviceManager
from pivy.quarter.devices.MouseHandler import MouseHandler
from pivy.quarter.eventhandlers.EventHandler import EventHandler
from pivy.quarter.eventhandlers.EventManager import EventManager


def check_quarter_widget_contract(
    widget: QuarterWidget, event: QtCore.QEvent
) -> None:
    assert_type(widget.sceneGraph, coin.SoNode | None)
    assert_type(widget.getSoRenderManager(), coin.SoRenderManager)
    assert_type(widget.getSoEventManager(), coin.SoEventManager)
    assert_type(widget.getHeadlight(), coin.SoDirectionalLight)
    assert_type(widget.getBackgroundColor(), QtGui.QColor)
    assert_type(widget.getContextMenu(), QMenu)
    assert_type(widget.contextMenuEnabled(), bool)
    assert_type(widget.getCacheContextId(), int)

    assert_type(widget.event(event), bool)

    widget.setSceneGraph(coin.SoSeparator())
    widget.sceneGraph = coin.SoSeparator()
    widget.enableContextMenu(True)
    widget.enableHeadlight(True)
    widget.setTransparencyType(coin.SoGLRenderAction.NONE)


def check_quarter_manager_contract(
    widget: QuarterWidget, event: QtCore.QEvent
) -> None:
    event_manager = widget.eventmanager
    device_manager = widget.devicemanager

    assert_type(event_manager, EventManager)
    assert_type(device_manager, DeviceManager)
    assert_type(event_manager.getWidget(), QuarterWidget)
    assert_type(device_manager.getWidget(), QuarterWidget)
    assert_type(device_manager.getLastMousePosition(), coin.SbVec2s)

    assert_type(event_manager.handleEvent(event), bool)

    handler = EventHandler()
    event_manager.registerEventHandler(handler)
    event_manager.unregisterEventHandler(handler)

    device = MouseHandler()
    assert_type(device.translateEvent(event), coin.SoEvent | None)
    device_manager.registerDevice(device)
    device_manager.unregisterDevice(device)
