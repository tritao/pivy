# pyright: reportMissingModuleSource=false

from typing import Any
from typing_extensions import assert_type

from pivy import coin


def check_named_callback_protocols() -> None:
    class SensorCallbackObject:
        def __call__(self, data: object, sensor: coin.SoSensor) -> None:
            pass

    sensor = coin.SoSensor()
    sensor.setFunction(SensorCallbackObject())
    assert_type(
        sensor.getFunction(),
        coin.SoSensorCallback[coin.SoSensor, object] | None,
    )

    class ErrorCallbackObject:
        def __call__(self, data: object, error: coin.SoError) -> None:
            pass

    coin.SoError.setHandlerCallback(ErrorCallbackObject(), None)

    class StateMachineDeleteCallback:
        def __call__(
            self,
            data: object,
            machine: coin.ScXMLStateMachine,
        ) -> None:
            pass

    class StateChangeCallback:
        def __call__(
            self,
            data: object,
            machine: coin.ScXMLStateMachine,
            stateidentifier: str,
            enterstate: bool,
            success: bool,
        ) -> None:
            pass

    state_machine = coin.ScXMLStateMachine()
    state_machine.addDeleteCallback(StateMachineDeleteCallback(), None)
    state_machine.addStateChangeCallback(StateChangeCallback(), None)


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

    def typed_timer_callback(data: str, sensor: coin.SoTimerSensor) -> None:
        del data, sensor

    typed_timer = coin.SoTimerSensor(typed_timer_callback, "timer")

    assert_type(timer, coin.SoTimerSensor)
    assert_type(field, coin.SoFieldSensor)
    assert_type(node, coin.SoNodeSensor)
    assert_type(typed_timer, coin.SoTimerSensor)

    def base_sensor_callback(data: object, sensor: coin.SoSensor) -> None:
        pass

    plain_timer = coin.SoTimerSensor()
    plain_timer.setData({"source": "typing"})
    assert_type(plain_timer.getData(), object | None)
    plain_timer.setFunction(base_sensor_callback)
    sensor_callback: coin.SoSensorCallback[coin.SoSensor, object] | None = (
        plain_timer.getFunction()
    )
    if sensor_callback is not None:
        sensor_callback({}, plain_timer)
    assert_type(plain_timer.getData(), object | None)

    data_sensor = coin.SoFieldSensor()
    data_sensor.setDeleteCallback(base_sensor_callback, {"source": "test"})
    data_sensor.setDeleteCallback(base_sensor_callback)

    def changed_callback(data: Any) -> None:
        pass

    changed_contract: coin.SoSensorManagerChangedCallback = changed_callback
    coin.SoDB.getSensorManager().setChangedCallback(changed_contract, None)


def check_database_callbacks() -> None:
    def header_callback(data: object, input: coin.SoInput) -> None:
        pass

    header_contract: coin.SoDBHeaderCallback = header_callback

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
            header_contract,
            header_contract,
        ),
        bool,
    )
    coin.SoDB.addProgressCallback(progress_callback, None)
    coin.SoDB.removeProgressCallback(progress_callback, None)


def check_callback_list() -> None:
    callback_list = coin.SoCallbackList()
    callback_api: coin.SoCallbackListAPI = callback_list

    def callback(data: object, callbackdata: object) -> None:
        pass

    callback_contract: coin.SoCallbackListCallback[object] = callback

    callback_list.addCallback(callback_contract, None)
    callback_api.addCallback(callback_contract, None)
    callback_list.removeCallback(callback_contract, None)
    callback_list.invokeCallbacks({"source": "typing"})

    def typed_callback(data: str, callbackdata: object) -> None:
        del data, callbackdata

    typed_callback_contract: coin.SoCallbackListCallback[str] = typed_callback

    class TypedCallbackList:
        def addCallback(
            self,
            f: coin.SoCallbackListCallback[str],
            userData: str | None = None,
        ) -> None:
            del f, userData

        def removeCallback(
            self,
            f: coin.SoCallbackListCallback[str],
            userdata: str | None = None,
        ) -> None:
            del f, userdata

        def clearCallbacks(self) -> None:
            pass

        def getNumCallbacks(self) -> int:
            return 0

        def invokeCallbacks(self, callbackdata: object) -> None:
            del callbackdata

    typed_api: coin.SoCallbackListAPI[str] = TypedCallbackList()
    typed_api.addCallback(typed_callback_contract, "owner")
    typed_api.removeCallback(typed_callback_contract, "owner")


def check_context_handler_callbacks() -> None:
    def callback(data: object, contextid: int) -> None:
        pass

    callback_contract: coin.SoContextDestructionCallback = callback

    coin.SoContextHandler.addContextDestructionCallback(callback_contract, None)
    coin.SoContextHandler.removeContextDestructionCallback(callback_contract, None)

    coin.SoGLCacheContextElement.scheduleDeleteCallback(41, callback_contract, None)


def check_database_progress_callback_protocol() -> None:
    def callback(
        data: object,
        itemid: coin.SbName,
        fraction: float,
        interruptible: bool,
    ) -> bool:
        return interruptible and fraction >= 0.0 and bool(itemid)

    callback_contract: coin.SoDBProgressCallback = callback
    coin.SoDB.addProgressCallback(callback_contract, None)
    coin.SoDB.removeProgressCallback(callback_contract, None)


def check_graphics_callback_setters() -> None:
    def end_frame_callback(data: object) -> None:
        pass

    end_frame_contract: coin.SoGLImageEndFrameCallback = end_frame_callback
    image = coin.SoGLImage()
    image.setEndFrameCallback(end_frame_contract, None)
    image.setEndFrameCallback(None)

    def enable_callback(
        data: object,
        state: coin.SoState,
        enable: bool,
    ) -> None:
        pass

    enable_contract: coin.SoShaderEnableCallback = enable_callback
    shader_program = coin.SoShaderProgram()
    shader_program.setEnableCallback(enable_contract, None)
    shader_program.setEnableCallback(None)

    def fetch_proto_callback(
        data: object,
        input: coin.SoInput,
        urls: list[coin.SbString],
        numurls: int,
    ) -> coin.SoProto | None:
        return None if numurls != len(urls) else None

    fetch_proto_contract: coin.SoProtoFetchExternProtoCallback = fetch_proto_callback
    coin.SoProto.setFetchExternProtoCallback(fetch_proto_contract, None)
    coin.SoProto.setFetchExternProtoCallback(None)

    def image_read_callback(
        data: object,
        filename: coin.SbString,
        image: coin.SbImage,
    ) -> bool:
        return bool(filename) and isinstance(image, coin.SbImage)

    image_read_contract: coin.SbImageReadImageCallback = image_read_callback
    coin.SbImage.addReadImageCB(image_read_contract, None)
    coin.SbImage.removeReadImageCB(image_read_contract, None)

    image = coin.SbImage()
    assert_type(
        image.scheduleReadFile(
            image_read_contract,
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
        tuple[coin.SoEventCallbackHandler, object],
    )
    event_node.removeEventCallback(coin.SoType.badType(), event_handle)

    def selection_callback(data: object, path: coin.SoPath) -> None:
        pass

    def selection_class_callback(
        data: object,
        selection: coin.SoSelection,
    ) -> None:
        pass

    def pick_filter_callback(
        data: object,
        point: coin.SoPickedPoint,
    ) -> coin.SoPath:
        return coin.SoPath()

    selection_path_contract: coin.SoSelectionPathCallback[object] = (
        selection_callback
    )
    selection_class_contract: coin.SoSelectionClassCallback[object] = (
        selection_class_callback
    )
    selection_pick_contract: coin.SoSelectionPickCallback[object] = (
        pick_filter_callback
    )

    def typed_selection_callback(data: str, path: coin.SoPath) -> None:
        del data, path

    def typed_selection_class_callback(
        data: int,
        selection: coin.SoSelection,
    ) -> None:
        del data, selection

    def typed_pick_filter_callback(
        data: bytes,
        point: coin.SoPickedPoint,
    ) -> coin.SoPath:
        del data, point
        return coin.SoPath()

    typed_selection_contract: coin.SoSelectionPathCallback[str] = (
        typed_selection_callback
    )

    selection = coin.SoSelection()
    selection.addSelectionCallback(selection_callback, None)
    selection.addSelectionCallback(typed_selection_callback, "selection")
    selection.removeSelectionCallback(selection_callback, None)
    selection.addDeselectionCallback(selection_callback, None)
    selection.removeDeselectionCallback(selection_callback, None)
    selection.addStartCallback(selection_class_callback, None)
    selection.addStartCallback(
        typed_selection_class_callback,
        1,
    )
    selection.removeStartCallback(selection_class_callback, None)
    selection.addFinishCallback(selection_class_callback, None)
    selection.removeFinishCallback(selection_class_callback, None)
    selection.setPickFilterCallback(pick_filter_callback, None)
    selection.setPickFilterCallback(
        typed_pick_filter_callback,
        b"pick",
    )
    selection.addChangeCallback(selection_class_callback, None)
    selection.removeChangeCallback(selection_class_callback, None)

    def lasso_filter_callback(
        data: object,
        path: coin.SoPath,
    ) -> coin.SoPath | None:
        return path

    def triangle_filter_callback(
        data: object,
        action: coin.SoCallbackAction,
        v1: coin.SoPrimitiveVertex,
        v2: coin.SoPrimitiveVertex,
        v3: coin.SoPrimitiveVertex,
    ) -> bool:
        return True

    def line_filter_callback(
        data: object,
        action: coin.SoCallbackAction,
        v1: coin.SoPrimitiveVertex,
        v2: coin.SoPrimitiveVertex,
    ) -> bool:
        return False

    def point_filter_callback(
        data: object,
        action: coin.SoCallbackAction,
        vertex: coin.SoPrimitiveVertex,
    ) -> bool:
        return True

    lasso_contract: coin.SoExtSelectionLassoFilterCallback = lasso_filter_callback
    triangle_contract: coin.SoExtSelectionTriangleFilterCallback = triangle_filter_callback
    line_contract: coin.SoExtSelectionLineSegmentFilterCallback = line_filter_callback
    point_contract: coin.SoExtSelectionPointFilterCallback = point_filter_callback

    extended_selection = coin.SoExtSelection()
    extended_selection.setLassoFilterCallback(
        lasso_filter_callback,
        None,
        False,
    )
    extended_selection.setLassoFilterCallback(None)
    extended_selection.setTriangleFilterCallback(
        triangle_filter_callback,
        None,
    )
    extended_selection.setTriangleFilterCallback(None)
    extended_selection.setLineSegmentFilterCallback(
        line_filter_callback,
        None,
    )
    extended_selection.setLineSegmentFilterCallback(None)
    extended_selection.setPointFilterCallback(point_filter_callback, None)
    extended_selection.setPointFilterCallback(None)


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

    sorted_object_contract: coin.SoGLSortedObjectOrderCallback = (
        sorted_object_callback
    )
    gl_action.setSortedObjectOrderStrategy(
        coin.SoGLRenderAction.CUSTOM_CALLBACK,
        sorted_object_contract,
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
    def dragger_callback(data: object, dragger: coin.SoDragger) -> None:
        pass

    dragger_contract: coin.SoDraggerCallback = dragger_callback

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

    error_handler: coin.SoErrorCallback | None = coin.SoError.getHandlerCallback()
    debug_handler: coin.SoErrorCallback | None = (
        coin.SoDebugError.getHandlerCallback()
    )
    memory_handler: coin.SoErrorCallback | None = (
        coin.SoMemoryError.getHandlerCallback()
    )
    read_handler: coin.SoErrorCallback | None = coin.SoReadError.getHandlerCallback()
    assert_type(coin.SoError.getHandlerData(), object | None)
    assert_type(coin.SoDebugError.getHandlerData(), object | None)
    assert_type(coin.SoMemoryError.getHandlerData(), object | None)
    assert_type(coin.SoReadError.getHandlerData(), object | None)
