from typing import Any, ClassVar, Protocol, Sequence

from pivy import coin


class SoGuiBinding(Protocol):
    @staticmethod
    def init(*args: Any, **kwargs: Any) -> Any: ...

    @staticmethod
    def mainLoop() -> None: ...

    @staticmethod
    def show(mainwindow: Any) -> None: ...


class SoGuiWidget(Protocol):
    def show(self) -> None: ...
    def setWindowTitle(self, title: str) -> None: ...
    def resize(self, width: int, height: int) -> None: ...


class SoGui_Proxy:
    debug: bool

    def __init__(self, gui: str | None, debug: bool) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __str__(self) -> str: ...


class SoGui:
    @staticmethod
    def init(*args: Any, **kwargs: Any) -> Any: ...

    @staticmethod
    def mainLoop() -> None: ...

    @staticmethod
    def show(mainwindow: Any) -> None: ...


class SoGuiViewer:
    BROWSER: ClassVar[int]
    EDITOR: ClassVar[int]
    VIEW_AS_IS: ClassVar[int]
    VIEW_HIDDEN_LINE: ClassVar[int]
    VIEW_NO_TEXTURE: ClassVar[int]
    VIEW_LOW_COMPLEXITY: ClassVar[int]
    VIEW_LINE: ClassVar[int]
    VIEW_POINT: ClassVar[int]
    VIEW_BBOX: ClassVar[int]
    VIEW_LOW_RES_LINE: ClassVar[int]
    VIEW_LOW_RES_POINT: ClassVar[int]
    VIEW_SAME_AS_STILL: ClassVar[int]
    VIEW_WIREFRAME_OVERLAY: ClassVar[int]
    STILL: ClassVar[int]
    INTERACTIVE: ClassVar[int]
    BUFFER_SINGLE: ClassVar[int]
    BUFFER_DOUBLE: ClassVar[int]
    BUFFER_INTERACTIVE: ClassVar[int]
    VARIABLE_NEAR_PLANE: ClassVar[int]
    CONSTANT_NEAR_PLANE: ClassVar[int]


class SoGui_Quarter_Wrapper:
    _root: coin.SoNode | None
    quarterwidget: Any

    def __init__(self, mainwindow: Any) -> None: ...
    def getCamera(self) -> coin.SoCamera: ...
    def getSize(self) -> coin.SbVec2s: ...
    def getViewportRegion(self) -> coin.SbViewportRegion: ...
    def redrawOnSelectionChange(self, selection: coin.SoSelection) -> None: ...
    def setBackgroundColor(self, color: coin.SbColor) -> None: ...
    def setDrawStyle(self, type: int, style: int) -> None: ...
    def setGLRenderAction(self, renderaction: coin.SoGLRenderAction) -> None: ...
    def setHeadlight(self, onOff: bool) -> None: ...
    def setOverlaySceneGraph(self, overlay: coin.SoNode | None) -> None: ...
    def setSceneGraph(self, root: coin.SoNode) -> None: ...
    def setSize(self, size: Sequence[int]) -> None: ...
    def setTitle(self, title: str) -> None: ...
    def show(self) -> None: ...
    def viewAll(self) -> None: ...


SoGuiCursor: type[Any]
SoGuiComponent: type[Any]
SoGuiGLWidget: type[Any]
SoGuiFullViewer: type[Any]
SoGuiFlyViewer: type[Any]
SoGuiPlaneViewer: type[Any]
SoGuiDevice: type[Any]
SoGuiKeyboard: type[Any]
SoGuiMouse: type[Any]
SoGuiConstrainedViewer: type[Any]

SoGuiExaminerViewer = SoGui_Quarter_Wrapper
SoGuiRenderArea = SoGui_Quarter_Wrapper

gui: str | None
debug: bool
