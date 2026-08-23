# pyright: reportMissingModuleSource=false

from typing_extensions import assert_type

from pivy import coin, sogui
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
    assert_type(soqt.SoQt.getWidgetSize(widget), coin.SbVec2s)
    widget.show()
    widget.setWindowTitle("Pivy")
    widget.resize(640, 480)
    gui_widget: sogui.SoGuiWidget = widget
    gui_widget.show()

    def fatal_error_callback(
        message: coin.SbString, code: int, data: object
    ) -> None:
        del message, code, data

    previous_handler: soqt.SoQtFatalErrorCallback | None = (
        soqt.SoQt.setFatalErrorHandler(fatal_error_callback, None)
    )
    assert_type(previous_handler, soqt.SoQtFatalErrorCallback | None)


def check_soqt_render_area_contract() -> None:
    area = soqt.SoQtRenderArea()

    def event_callback(data: object, event: soqt.QEvent) -> object:
        return event

    area.setEventCallback(event_callback, {"source": "typing"})
    area.setEventCallback(event_callback)

    assert_type(area.getSceneGraph(), coin.SoNode | None)
    assert_type(area.getOverlaySceneGraph(), coin.SoNode | None)
    assert_type(area.getSceneManager(), coin.SoSceneManager)
    assert_type(area.getOverlaySceneManager(), coin.SoSceneManager)
    assert_type(area.getGLRenderAction(), coin.SoGLRenderAction)
    assert_type(area.getOverlayGLRenderAction(), coin.SoGLRenderAction)
    assert_type(area.getBackgroundColor(), coin.SbColor)
    assert_type(area.getBackgroundIndex(), int)
    assert_type(area.getOverlayBackgroundIndex(), int)
    assert_type(area.getViewportRegion(), coin.SbViewportRegion)
    assert_type(area.getTransparencyType(), int)
    assert_type(area.isAutoRedraw(), bool)
    assert_type(area.isClearBeforeRender(), bool)
    assert_type(area.isClearZBufferBeforeRender(), bool)
    assert_type(area.getWidget(), soqt.QWidget)
    assert_type(area.getParentWidget(), soqt.QWidget)
    assert_type(area.sendSoEvent(coin.SoEvent()), bool)


def check_soqt_component_and_gl_widget_contract() -> None:
    component = soqt.SoQtComponent()

    def window_close_callback(user: object, closed: soqt.SoQtComponent) -> None:
        del user, closed

    component.setWindowCloseCallback(window_close_callback)
    assert_type(component.getWidget(), soqt.QWidget)
    assert_type(component.getBaseWidget(), soqt.QWidget)
    assert_type(component.getShellWidget(), soqt.QWidget)
    assert_type(component.getParentWidget(), soqt.QWidget)
    assert_type(component.getSize(), coin.SbVec2s)
    assert_type(component.getTitle(), str)
    assert_type(component.getIconTitle(), str)
    assert_type(component.getWidgetName(), str)
    assert_type(component.getClassName(), str)
    assert_type(component.isFullScreen(), bool)
    assert_type(component.isVisible(), bool)
    assert_type(component.isTopLevelShell(), bool)

    gl_widget = soqt.SoQtGLWidget()
    assert_type(gl_widget.isBorder(), bool)
    assert_type(gl_widget.isDoubleBuffer(), bool)
    assert_type(gl_widget.isOverlayRender(), bool)
    assert_type(gl_widget.getAccumulationBuffer(), bool)
    assert_type(gl_widget.getSampleBuffers(), int)
    assert_type(gl_widget.getGLWidget(), soqt.QWidget)
    assert_type(gl_widget.getNormalWidget(), soqt.QWidget)
    assert_type(gl_widget.getOverlayWidget(), soqt.QWidget)
    assert_type(gl_widget.hasOverlayGLArea(), bool)


def check_soqt_viewer_family_contract() -> None:
    viewer = soqt.SoQtConstrainedViewer()
    assert_type(viewer.getUpDirection(), coin.SbVec3f)
    assert_type(viewer.getCamera(), coin.SoCamera | None)

    plane = soqt.SoQtPlaneViewer()
    plane.setViewing(True)
    plane.setCamera(coin.SoOrthographicCamera())

    examiner = soqt.SoQtExaminerViewer()
    assert_type(examiner.isAnimationEnabled(), bool)
    assert_type(examiner.isAnimating(), bool)
    assert_type(examiner.isFeedbackVisible(), bool)
    assert_type(examiner.getFeedbackSize(), int)

    fly = soqt.SoQtFlyViewer()
    fly.setViewing(True)
    fly.setCamera(coin.SoPerspectiveCamera())


def check_soqt_devices_and_utility_contract() -> None:
    device = soqt.SoQtKeyboard()
    assert_type(device.translateEvent(soqt.QEvent()), coin.SoEvent)

    popup = soqt.SoQtPopupMenu()

    def menu_callback(item_id: int, data: object) -> None:
        del item_id, data

    menu_callback_contract: soqt.SoQtMenuSelectionCallback = menu_callback

    popup.addMenuSelectionCallback(menu_callback_contract, None)
    popup.removeMenuSelectionCallback(menu_callback_contract, None)
    assert_type(popup.newMenu("File"), int)
    assert_type(popup.getMenuTitle(1), str)
    assert_type(popup.getMenuItemEnabled(1), bool)
    assert_type(popup.getRadioGroupSize(1), int)

    cursor = soqt.SoQtCursor()
    assert_type(cursor.getShape(), int)
    assert_type(cursor.getCustomCursor(), int)
    assert_type(cursor.getZoomCursor(), soqt.SoQtCursor)
    assert_type(cursor.getPanCursor(), soqt.SoQtCursor)
    assert_type(cursor.getRotateCursor(), soqt.SoQtCursor)


def check_soqt_viewer_contract() -> None:
    viewer = soqt.SoQtExaminerViewer()

    def viewer_callback(data: object, callback_viewer: soqt.SoQtViewer) -> None:
        del data, callback_viewer

    def auto_clipping_callback(
        data: object, nearfar: coin.SbVec2f
    ) -> coin.SbVec2f:
        del data
        return nearfar

    auto_clipping_contract: soqt.SoQtAutoClippingCallback = auto_clipping_callback

    viewer.setAutoClippingStrategy(0, cb=auto_clipping_contract)
    viewer.addStartCallback(viewer_callback)
    viewer.addFinishCallback(viewer_callback)
    viewer.removeStartCallback(viewer_callback)
    viewer.removeFinishCallback(viewer_callback)

    assert_type(viewer.getCamera(), coin.SoCamera | None)
    assert_type(viewer.getHeadlight(), coin.SoDirectionalLight)
    assert_type(viewer.getSceneGraph(), coin.SoNode | None)

    viewer.setCamera(coin.SoPerspectiveCamera())
    viewer.setSceneGraph(coin.SoSeparator())
