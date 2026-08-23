from typing import Any, Callable, ClassVar, Literal, Protocol, Sequence, overload

from pivy import coin


SoGuiDrawType = Literal[0, 1]
SoGuiViewStyle = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
SoGuiBufferMode = Literal[0, 1, 2]
SoGuiNearPlaneMode = Literal[0, 1]


class SoGuiBinding(Protocol):
    @staticmethod
    def init(*args: Any, **kwargs: Any) -> SoGuiWidget: ...

    @staticmethod
    def mainLoop() -> None: ...

    @staticmethod
    def show(mainwindow: SoGuiWidget) -> None: ...


class SoGuiWidget(Protocol):
    def show(self) -> None: ...
    def setWindowTitle(self, title: str) -> None: ...
    def resize(self, width: int, height: int) -> None: ...


class SoGuiSize(Protocol):
    width: int
    height: int


class SoGuiRenderWidget(SoGuiWidget, Protocol):
    """The additional surface used by the Quarter-backed wrapper."""

    def getSoRenderManager(self) -> coin.SoRenderManager: ...
    def size(self) -> SoGuiSize: ...
    def setBackgroundColor(
        self, color: coin.SbColor | coin.SbColor4f
    ) -> None: ...
    def enableHeadlight(self, onoff: bool) -> None: ...
    def setSceneGraph(self, root: coin.SoNode) -> None: ...
    def viewAll(self) -> None: ...


class SoGui_Proxy:
    debug: bool

    def __init__(self, gui: str | None, debug: bool) -> None: ...
    @overload
    def __getattr__(self, name: Literal["init"]) -> Callable[..., SoGuiWidget]: ...
    @overload
    def __getattr__(self, name: Literal["mainLoop"]) -> Callable[[], None]: ...
    @overload
    def __getattr__(
        self, name: Literal["show"]
    ) -> Callable[[SoGuiWidget], None]: ...
    def __getattr__(self, name: str) -> Any: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __str__(self) -> str: ...


class SoGui:
    @staticmethod
    def init(*args: Any, **kwargs: Any) -> SoGuiWidget: ...

    @staticmethod
    def mainLoop() -> None: ...

    @staticmethod
    def show(mainwindow: SoGuiWidget) -> None: ...


class SoGuiViewer:
    BROWSER: ClassVar[Literal[0]]
    EDITOR: ClassVar[Literal[1]]
    VIEW_AS_IS: ClassVar[Literal[0]]
    VIEW_HIDDEN_LINE: ClassVar[Literal[1]]
    VIEW_NO_TEXTURE: ClassVar[Literal[2]]
    VIEW_LOW_COMPLEXITY: ClassVar[Literal[3]]
    VIEW_LINE: ClassVar[Literal[4]]
    VIEW_POINT: ClassVar[Literal[5]]
    VIEW_BBOX: ClassVar[Literal[6]]
    VIEW_LOW_RES_LINE: ClassVar[Literal[7]]
    VIEW_LOW_RES_POINT: ClassVar[Literal[8]]
    VIEW_SAME_AS_STILL: ClassVar[Literal[9]]
    VIEW_WIREFRAME_OVERLAY: ClassVar[Literal[10]]
    STILL: ClassVar[Literal[0]]
    INTERACTIVE: ClassVar[Literal[1]]
    BUFFER_SINGLE: ClassVar[Literal[0]]
    BUFFER_DOUBLE: ClassVar[Literal[1]]
    BUFFER_INTERACTIVE: ClassVar[Literal[2]]
    VARIABLE_NEAR_PLANE: ClassVar[Literal[0]]
    CONSTANT_NEAR_PLANE: ClassVar[Literal[1]]


class SoGui_Quarter_Wrapper:
    _root: coin.SoNode | None
    quarterwidget: SoGuiRenderWidget

    def __init__(self, mainwindow: SoGuiRenderWidget) -> None: ...
    def getCamera(self) -> coin.SoCamera: ...
    def getSize(self) -> coin.SbVec2s: ...
    def getViewportRegion(self) -> coin.SbViewportRegion: ...
    def redrawOnSelectionChange(self, selection: coin.SoSelection) -> None: ...
    def setBackgroundColor(self, color: coin.SbColor) -> None: ...
    def setDrawStyle(self, type: SoGuiDrawType, style: SoGuiViewStyle) -> None: ...
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
