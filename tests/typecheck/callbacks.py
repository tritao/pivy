# pyright: reportMissingModuleSource=false

from typing import Any, Callable, assert_type

from pivy import coin


def check_sensor_callbacks() -> None:
    def timer_callback(data: Any, sensor: coin.SoTimerSensor) -> None:
        pass

    def field_callback(data: Any, sensor: coin.SoFieldSensor) -> None:
        pass

    def node_callback(data: Any, sensor: coin.SoNodeSensor) -> None:
        pass

    timer = coin.SoTimerSensor(timer_callback, None)
    field = coin.SoFieldSensor(field_callback, None)
    node = coin.SoNodeSensor(node_callback, None)

    assert_type(timer, coin.SoTimerSensor)
    assert_type(field, coin.SoFieldSensor)
    assert_type(node, coin.SoNodeSensor)

    def base_sensor_callback(data: object, sensor: coin.SoSensor) -> None:
        pass

    plain_timer = coin.SoTimerSensor()
    plain_timer.setFunction(base_sensor_callback)

    data_sensor = coin.SoFieldSensor()
    data_sensor.setDeleteCallback(base_sensor_callback, {"source": "test"})
    data_sensor.setDeleteCallback(base_sensor_callback)

    def changed_callback(data: Any) -> None:
        pass

    coin.SoDB.getSensorManager().setChangedCallback(changed_callback, None)


def check_database_callbacks() -> None:
    def header_callback(data: object, input: coin.SoInput) -> None:
        pass

    def progress_callback(
        data: object,
        itemid: coin.SbName,
        fraction: float,
        interruptible: bool,
    ) -> bool:
        return interruptible and fraction >= 0.0 and bool(itemid)

    assert_type(
        coin.SoDB.registerHeader(
            coin.SbString("#PivyTypingHeader"),
            False,
            1.0,
            header_callback,
            header_callback,
        ),
        bool,
    )
    coin.SoDB.addProgressCallback(progress_callback, None)
    coin.SoDB.removeProgressCallback(progress_callback, None)


def check_callback_list() -> None:
    callback_list = coin.SoCallbackList()

    def callback(data: object, callbackdata: object) -> None:
        pass

    callback_list.addCallback(callback, None)
    callback_list.removeCallback(callback, None)
    callback_list.invokeCallbacks({"source": "typing"})


def check_context_handler_callbacks() -> None:
    def callback(data: object, contextid: int) -> None:
        pass

    coin.SoContextHandler.addContextDestructionCallback(callback, None)
    coin.SoContextHandler.removeContextDestructionCallback(callback, None)

    coin.SoGLCacheContextElement.scheduleDeleteCallback(41, callback, None)


def check_graphics_callback_setters() -> None:
    def end_frame_callback(data: object) -> None:
        pass

    image = coin.SoGLImage()
    image.setEndFrameCallback(end_frame_callback, None)
    image.setEndFrameCallback(None)

    def enable_callback(
        data: object,
        state: coin.SoState,
        enable: bool,
    ) -> None:
        pass

    shader_program = coin.SoShaderProgram()
    shader_program.setEnableCallback(enable_callback, None)
    shader_program.setEnableCallback(None)

    def fetch_proto_callback(
        data: object,
        input: coin.SoInput,
        urls: list[coin.SbString],
        numurls: int,
    ) -> coin.SoProto | None:
        return None if numurls != len(urls) else None

    coin.SoProto.setFetchExternProtoCallback(fetch_proto_callback, None)
    coin.SoProto.setFetchExternProtoCallback(None)

    def image_read_callback(
        data: object,
        filename: coin.SbString,
        image: coin.SbImage,
    ) -> bool:
        return bool(filename) and isinstance(image, coin.SbImage)

    coin.SbImage.addReadImageCB(image_read_callback, None)
    coin.SbImage.removeReadImageCB(image_read_callback, None)

    image = coin.SbImage()
    assert_type(
        image.scheduleReadFile(
            image_read_callback,
            None,
            coin.SbString("missing-image"),
        ),
        bool,
    )


def check_callback_action_callbacks() -> None:
    def node_callback(
        data: Any,
        action: coin.SoCallbackAction,
        node: coin.SoNode,
    ) -> int:
        return action.CONTINUE

    def triangle_callback(
        data: Any,
        action: coin.SoCallbackAction,
        v1: coin.SoPrimitiveVertex,
        v2: coin.SoPrimitiveVertex,
        v3: coin.SoPrimitiveVertex,
    ) -> None:
        pass

    def line_callback(
        data: Any,
        action: coin.SoCallbackAction,
        v1: coin.SoPrimitiveVertex,
        v2: coin.SoPrimitiveVertex,
    ) -> None:
        pass

    def point_callback(
        data: Any,
        action: coin.SoCallbackAction,
        vertex: coin.SoPrimitiveVertex,
    ) -> None:
        pass

    action = coin.SoCallbackAction()
    type_id = coin.SoType.badType()
    action.addPreCallback(type_id, node_callback, None)
    action.addPostCallback(type_id, node_callback, None)
    action.addPreTailCallback(node_callback, None)
    action.addPostTailCallback(node_callback, None)
    action.addTriangleCallback(type_id, triangle_callback, None)
    action.addLineSegmentCallback(type_id, line_callback, None)
    action.addPointCallback(type_id, point_callback, None)


def check_event_and_selection_callbacks() -> None:
    def event_callback(data: Any, event: coin.SoEventCallback) -> None:
        pass

    event_node = coin.SoEventCallback()
    event_handle = event_node.addEventCallback(
        coin.SoType.badType(), event_callback, None
    )
    assert_type(
        event_handle,
        tuple[Callable[[Any, coin.SoEventCallback], None], Any],
    )
    event_node.removeEventCallback(coin.SoType.badType(), event_handle)

    def selection_callback(data: Any, path: coin.SoPath) -> None:
        pass

    def selection_class_callback(
        data: Any,
        selection: coin.SoSelection,
    ) -> None:
        pass

    def pick_filter_callback(
        data: Any,
        point: coin.SoPickedPoint,
    ) -> coin.SoPath:
        return coin.SoPath()

    selection = coin.SoSelection()
    selection.addSelectionCallback(selection_callback, None)
    selection.removeSelectionCallback(selection_callback, None)
    selection.addDeselectionCallback(selection_callback, None)
    selection.removeDeselectionCallback(selection_callback, None)
    selection.addStartCallback(selection_class_callback, None)
    selection.removeStartCallback(selection_class_callback, None)
    selection.addFinishCallback(selection_class_callback, None)
    selection.removeFinishCallback(selection_class_callback, None)
    selection.setPickFilterCallback(pick_filter_callback, None)
    selection.addChangeCallback(selection_class_callback, None)
    selection.removeChangeCallback(selection_class_callback, None)


def check_render_and_scene_callbacks() -> None:
    def pass_callback(data: Any) -> None:
        pass

    def abort_callback(data: Any) -> int:
        return coin.SoGLRenderAction.CONTINUE

    def gl_callback(
        data: Any,
        action: coin.SoGLRenderAction,
    ) -> None:
        pass

    gl_action = coin.SoGLRenderAction(coin.SbViewportRegion())
    gl_action.setPassCallback(pass_callback, None)
    gl_action.setAbortCallback(abort_callback, None)
    gl_action.addPreRenderCallback(gl_callback, None)
    gl_action.removePreRenderCallback(gl_callback, None)

    def sorted_object_callback(
        data: object,
        action: coin.SoGLRenderAction,
    ) -> float:
        return 0.0

    gl_action.setSortedObjectOrderStrategy(
        coin.SoGLRenderAction.CUSTOM_CALLBACK,
        sorted_object_callback,
        None,
    )
    gl_action.setSortedObjectOrderStrategy(coin.SoGLRenderAction.BBOX_CENTER)

    def scene_callback(data: Any, manager: coin.SoSceneManager) -> None:
        pass

    def render_callback(data: Any, manager: coin.SoRenderManager) -> None:
        pass

    scene_manager = coin.SoSceneManager()
    scene_manager.setRenderCallback(scene_callback)

    render_manager = coin.SoRenderManager()
    render_manager.setRenderCallback(render_callback)
    render_manager.addPreRenderCallback(render_callback, None)
    render_manager.removePreRenderCallback(render_callback, None)
    render_manager.addPostRenderCallback(render_callback, None)
    render_manager.removePostRenderCallback(render_callback, None)


def check_other_callback_domains() -> None:
    def dragger_callback(data: Any, dragger: coin.SoDragger) -> None:
        pass

    dragger = coin.SoDragger()
    dragger.addStartCallback(dragger_callback)
    dragger.removeStartCallback(dragger_callback)
    dragger.addMotionCallback(dragger_callback)
    dragger.removeMotionCallback(dragger_callback)

    def visitation_callback(data: Any, path: coin.SoPath) -> int:
        return 0

    def filter_callback(
        data: Any,
        left: coin.SoPath,
        right: coin.SoPath,
    ) -> bool:
        return True

    def intersection_callback(
        data: Any,
        left: coin.SoIntersectingPrimitive,
        right: coin.SoIntersectingPrimitive,
    ) -> int:
        return 0

    intersection_action = coin.SoIntersectionDetectionAction()
    type_id = coin.SoType.badType()
    intersection_action.addVisitationCallback(
        type_id, visitation_callback, None
    )
    intersection_action.removeVisitationCallback(
        type_id, visitation_callback, None
    )
    intersection_action.setFilterCallback(filter_callback)
    intersection_action.addIntersectionCallback(intersection_callback)
    intersection_action.removeIntersectionCallback(intersection_callback)


def check_error_callbacks() -> None:
    def error_callback(data: object, error: coin.SoError) -> None:
        pass

    coin.SoError.setHandlerCallback(error_callback, {"source": "test"})
    coin.SoDebugError.setHandlerCallback(error_callback, None)
    coin.SoMemoryError.setHandlerCallback(error_callback, None)
    coin.SoReadError.setHandlerCallback(error_callback, None)
