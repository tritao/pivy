# pyright: reportMissingModuleSource=false

from typing import Literal, Sequence
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

    render_widget: sogui.SoGuiRenderWidget = _Widget()
    assert_type(render_widget.getSoRenderManager(), coin.SoRenderManager)
    assert_type(render_widget.size().width, int)
    render_widget.setBackgroundColor(coin.SbColor())
    render_widget.enableHeadlight(True)
    render_widget.setSceneGraph(coin.SoSeparator())
    render_widget.viewAll()


def check_sogui_viewer_aliases() -> None:
    viewer = sogui.SoGuiExaminerViewer(_Widget())
    assert_type(viewer, sogui.SoGui_Quarter_Wrapper)
    assert_type(sogui.SoGuiViewer.BROWSER, Literal[0])
    widget = sogui.SoGui.init()
    assert_type(widget, sogui.SoGuiWidget)
    sogui.SoGui.show(widget)


def check_backend_contract() -> None:
    backend: sogui.SoGuiBinding = sogui.SoGui
    assert_type(backend.init(), sogui.SoGuiWidget)
    backend.mainLoop()
    backend.show(_Widget())


class _Size:
    width: int = 640
    height: int = 480


class _Widget:
    def show(self) -> None:
        pass

    def hide(self) -> None:
        pass

    def isVisible(self) -> bool:
        return True

    def setVisible(self, visible: bool) -> None:
        del visible

    def setWindowTitle(self, title: str) -> None:
        pass

    def windowTitle(self) -> str:
        return "Pivy"

    def resize(self, width: int, height: int) -> None:
        pass

    def width(self) -> int:
        return 640

    def height(self) -> int:
        return 480

    def getSoRenderManager(self) -> coin.SoRenderManager:
        return coin.SoRenderManager()

    def size(self) -> _Size:
        return _Size()

    def setBackgroundColor(
        self, color: coin.SbColor | coin.SbColor4f
    ) -> None:
        del color

    def enableHeadlight(self, onoff: bool) -> None:
        del onoff

    def setSceneGraph(self, root: coin.SoNode) -> None:
        del root

    def viewAll(self) -> None:
        pass


def check_widget_contract() -> None:
    widget: sogui.SoGuiWidget = _Widget()
    widget.setWindowTitle("Pivy")
    widget.hide()
    assert_type(widget.isVisible(), bool)
    widget.setVisible(True)
    assert_type(widget.windowTitle(), str)
    widget.resize(640, 480)
    assert_type(widget.width(), int)
    assert_type(widget.height(), int)
    widget.show()


def check_enum_contract() -> None:
    assert_type(sogui.SoGuiViewer.STILL, Literal[0])
    assert_type(sogui.SoGuiViewer.VIEW_LINE, Literal[4])
    assert_type(sogui.SoGuiViewer.BUFFER_DOUBLE, Literal[1])
    assert_type(sogui.SoGuiViewer.VARIABLE_NEAR_PLANE, Literal[0])
