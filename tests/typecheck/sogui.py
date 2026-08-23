# pyright: reportMissingModuleSource=false

from typing import Any, Sequence
from typing_extensions import assert_type

from pivy import coin, sogui


def check_sogui_wrapper_contract() -> None:
    wrapper = sogui.SoGui_Quarter_Wrapper(_Widget())
    assert_type(wrapper.getCamera(), coin.SoCamera)
    assert_type(wrapper.getSize(), coin.SbVec2s)
    assert_type(wrapper.getViewportRegion(), coin.SbViewportRegion)

    wrapper.setBackgroundColor(coin.SbColor())
    wrapper.setDrawStyle(0, 1)
    wrapper.setGLRenderAction(coin.SoGLRenderAction(coin.SbViewportRegion()))
    wrapper.setHeadlight(True)
    wrapper.setOverlaySceneGraph(None)
    wrapper.setSceneGraph(coin.SoSeparator())
    size: Sequence[int] = (640, 480)
    wrapper.setSize(size)
    wrapper.setTitle("Pivy")


def check_sogui_viewer_aliases() -> None:
    viewer = sogui.SoGuiExaminerViewer(_Widget())
    assert_type(viewer, sogui.SoGui_Quarter_Wrapper)
    assert_type(sogui.SoGuiViewer.BROWSER, int)
    widget = sogui.SoGui.init()
    assert_type(widget, sogui.SoGuiWidget)
    sogui.SoGui.show(widget)


def check_backend_contract() -> None:
    backend: sogui.SoGuiBinding = sogui.SoGui
    assert_type(backend.init(), sogui.SoGuiWidget)
    backend.mainLoop()
    backend.show(_Widget())


class _Widget:
    def show(self) -> None:
        pass

    def setWindowTitle(self, title: str) -> None:
        pass

    def resize(self, width: int, height: int) -> None:
        pass


def check_widget_contract() -> None:
    widget: sogui.SoGuiWidget = _Widget()
    widget.setWindowTitle("Pivy")
    widget.resize(640, 480)
    widget.show()
