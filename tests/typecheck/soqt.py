# pyright: reportMissingModuleSource=false

from typing import assert_type

from pivy import coin
from pivy.gui import soqt


def check_soqt_lifecycle_contract() -> None:
    assert_type(soqt.SoQt.getVersionString(), str)
    assert_type(soqt.SoQt.getVersionToolkitString(), str)
    assert_type(soqt.SoQt.getABIType(), int)
    assert_type(soqt.SoQt.isDebugLibrary(), bool)
    assert_type(soqt.SoQt.isCompatible(1, 0), bool)

    widget = soqt.SoQt.init("Pivy", "Pivy")
    assert_type(widget, soqt.QWidget)
    assert_type(soqt.SoQt.getTopLevelWidget(), soqt.QWidget)
    assert_type(soqt.SoQt.getShellWidget(widget), soqt.QWidget)
    assert_type(soqt.SoQt.getWidgetSize(widget), soqt.SbVec2s)


def check_soqt_render_area_contract() -> None:
    area = soqt.SoQtRenderArea()

    assert_type(area.getSceneGraph(), coin.SoNode | None)
    assert_type(area.getOverlaySceneGraph(), coin.SoNode | None)
    assert_type(area.getSceneManager(), coin.SoSceneManager)
    assert_type(area.getOverlaySceneManager(), coin.SoSceneManager)
    assert_type(area.getGLRenderAction(), coin.SoGLRenderAction)
    assert_type(area.getOverlayGLRenderAction(), coin.SoGLRenderAction)
    assert_type(area.getWidget(), soqt.QWidget)
    assert_type(area.getParentWidget(), soqt.QWidget)


def check_soqt_viewer_contract() -> None:
    viewer = soqt.SoQtExaminerViewer()

    assert_type(viewer.getCamera(), coin.SoCamera | None)
    assert_type(viewer.getHeadlight(), coin.SoDirectionalLight)
    assert_type(viewer.getSceneGraph(), coin.SoNode | None)

    viewer.setCamera(coin.SoPerspectiveCamera())
    viewer.setSceneGraph(coin.SoSeparator())
