#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# Pivy Quarter unit test suite
#
# For detailed info on its usage and on how to write additional test cases
# read:
#   - http://pyunit.sourceforge.net/pyunit.html
#   - http://diveintopython.org/unit_testing/
#
# Invoke this script with '--help' for usage information.
#

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pivy import coin, quarter
from pivy.qt import QtCore, QtGui
from pivy.qt.QtWidgets import QApplication
from pivy.quarter.devices.DeviceHandler import DeviceHandler
from pivy.quarter.eventhandlers.EventHandler import EventHandler


class AcceptingEventHandler(EventHandler):
    def handleEvent(self, event):
        return True


class QuarterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])
        cls.widget = quarter.QuarterWidget()

    def test_widget_lifecycle_and_scene_graph(self):
        widget = self.widget

        self.assertIsNone(widget.sceneGraph)
        self.assertIsInstance(widget.getSoRenderManager(), coin.SoRenderManager)
        self.assertIsInstance(widget.getSoEventManager(), coin.SoEventManager)
        self.assertIsInstance(widget.getHeadlight(), coin.SoDirectionalLight)
        self.assertTrue(widget.contextMenuEnabled())
        self.assertIsInstance(widget.getBackgroundColor(), QtGui.QColor)

        root = coin.SoSeparator()
        widget.setSceneGraph(root)

        self.assertIs(widget.sceneGraph, root)
        self.assertGreater(widget.getCacheContextId(), 0)

    def test_manager_ownership_and_registration(self):
        widget = self.widget
        device_manager = widget.devicemanager
        event_manager = widget.eventmanager

        self.assertIs(device_manager.getWidget(), widget)
        self.assertIs(event_manager.getWidget(), widget)
        self.assertEqual(len(device_manager.devices), 2)
        self.assertEqual(len(event_manager.eventhandlers), 1)

        device = DeviceHandler()
        device_manager.registerDevice(device)
        self.assertIs(device.manager, device_manager)
        self.assertIn(device, device_manager.devices)
        device_manager.unregisterDevice(device)
        self.assertNotIn(device, device_manager.devices)

        handler = AcceptingEventHandler()
        event_manager.registerEventHandler(handler)
        self.assertIs(handler.manager, event_manager)
        self.assertTrue(event_manager.handleEvent(QtCore.QEvent(QtCore.QEvent.User)))
        event_manager.unregisterEventHandler(handler)
        self.assertNotIn(handler, event_manager.eventhandlers)

    def test_scene_and_render_controls(self):
        widget = self.widget
        widget.enableContextMenu(False)
        self.assertFalse(widget.contextMenuEnabled())
        widget.enableContextMenu(True)

        widget.enableHeadlight(False)
        self.assertFalse(widget.getHeadlight().on.getValue())
        widget.enableHeadlight(True)
        self.assertTrue(widget.getHeadlight().on.getValue())

        widget.setBackgroundColor(QtGui.QColor(10, 20, 30, 40))
        color = widget.getBackgroundColor()
        self.assertEqual(color.red(), 10)
        self.assertEqual(color.green(), 20)
        self.assertEqual(color.blue(), 30)
        self.assertEqual(color.alpha(), 40)

if __name__ == "__main__":
    unittest.main(verbosity=2)
