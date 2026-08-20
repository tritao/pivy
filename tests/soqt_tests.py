#!/usr/bin/env python

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pivy import coin
from pivy.gui import soqt


class SoQtContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.top_level_widget = soqt.SoQt.init("Pivy", "Pivy")

    def test_lifecycle_and_metadata(self):
        self.assertIsNotNone(self.top_level_widget)
        self.assertIsNotNone(soqt.SoQt.getTopLevelWidget())
        self.assertTrue(soqt.SoQt.getVersionString())
        self.assertTrue(soqt.SoQt.isCompatible(1, 0))
        self.assertIsInstance(
            soqt.SoQt.getWidgetSize(self.top_level_widget), soqt.SbVec2s
        )

    def test_render_area_optional_scene_graphs(self):
        area = soqt.SoQtRenderArea(soqt.SoQt.getTopLevelWidget())

        self.assertIsNone(area.getSceneGraph())
        self.assertIsNone(area.getOverlaySceneGraph())
        self.assertIsNotNone(area.getSceneManager())
        self.assertIsNotNone(area.getOverlaySceneManager())
        self.assertIsNotNone(area.getGLRenderAction())
        self.assertIsNotNone(area.getOverlayGLRenderAction())
        self.assertIsNotNone(area.getWidget())
        self.assertIsNotNone(area.getParentWidget())

        scene = coin.SoSeparator()
        area.setSceneGraph(scene)
        self.assertIsInstance(area.getSceneGraph(), coin.SoSeparator)

    def test_viewer_optional_camera_and_scene_graph(self):
        viewer = soqt.SoQtExaminerViewer()

        self.assertIsNone(viewer.getCamera())
        self.assertIsNone(viewer.getSceneGraph())
        self.assertIsNotNone(viewer.getHeadlight())

        camera = coin.SoPerspectiveCamera()
        scene = coin.SoSeparator()
        viewer.setCamera(camera)
        viewer.setSceneGraph(scene)
        self.assertIsInstance(viewer.getCamera(), coin.SoCamera)
        self.assertIsInstance(viewer.getSceneGraph(), coin.SoSeparator)


if __name__ == "__main__":
    unittest.main(verbosity=2)
