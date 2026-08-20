"""Shared, declarative policy for the generated Pivy typing surface."""

from __future__ import annotations

from dataclasses import dataclass


# Generator normalization policy.  These tables describe the Python-facing
# type chosen for a C++/SWIG surface; keeping them beside the semantic policy
# below makes the generator and validator consume one source of truth.
BOOL_TYPES = {"bool", "SbBool"}
FLOAT_TYPES = {"double", "float"}
INT_TYPES = {
    "int",
    "int8_t",
    "int16_t",
    "int32_t",
    "int64_t",
    "long",
    "long int",
    "long long",
    "SbUniqueId",
    "short",
    "short int",
    "signed char",
    "signed int",
    "size_t",
    "time_t",
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "uint64_t",
    "unsigned",
    "unsigned char",
    "unsigned int",
    "unsigned long",
    "unsigned long int",
    "unsigned long long",
    "unsigned short",
    "unsigned short int",
}
COMPARISON_METHODS = {
    "__eq__",
    "__ge__",
    "__gt__",
    "__le__",
    "__lt__",
    "__ne__",
}
POINTER_HELPER_TYPES = {
    "charp": "str",
    "intp": "int",
    "longp": "int",
    "floatp": "float",
    "doublep": "float",
}
SCALAR_POINTER_HELPER_PARAMETERS = {
    ("SoQt", "getVersionInfo", "major"): "intp",
    ("SoQt", "getVersionInfo", "minor"): "intp",
    ("SoQt", "getVersionInfo", "micro"): "intp",
}
SCALAR_REFERENCE_HELPER_TYPES = {
    "SbBool": "intp",
    "char": "charp",
    "double": "doublep",
    "float": "floatp",
    "int": "intp",
    "long": "longp",
}
SEQUENCE_POINTER_PARAMETERS = {
    ("SbColor", "__init__", "rgb"): "Sequence[float]",
    ("SbColor4f", "__init__", "rgba"): "Sequence[float]",
    ("SoQt", "init", "argv"): "Sequence[str]",
}
SEQUENCE_ARRAY_PARAMETERS = {
    ("SbVec2s", "__init__", "v"): ("Sequence[int]", "2"),
    ("SbVec2s", "setValue", "v"): ("Sequence[int]", "2"),
    ("SbVec3s", "__init__", "v"): ("Sequence[int]", "3"),
    ("SbVec3s", "setValue", "v"): ("Sequence[int]", "3"),
}
BOOL_SEQUENCE_ARRAY_PARAMETERS = {
    ("SoQtViewer", "setAnaglyphStereoColorMasks", "left"): (
        "Sequence[bool]",
        "3",
    ),
    ("SoQtViewer", "setAnaglyphStereoColorMasks", "right"): (
        "Sequence[bool]",
        "3",
    ),
}
MATRIX_SEQUENCE_PARAMETERS = {
    ("SbDPMatrix", "__init__", "matrix"): "Sequence[Sequence[float]]",
    ("SbDPMatrix", "setValue", "m"): "Sequence[Sequence[float]]",
    ("SbMatrix", "__init__", "matrix"): "Sequence[Sequence[float]]",
    ("SbMatrix", "setValue", "m"): "Sequence[Sequence[float]]",
}
MATRIX_CPP_TYPES = {"SbDPMat", "SbMat"}
SEQUENCE_VALUE_RETURN_TYPES = {
    "SbColor": "Sequence[float]",
    "SbColor4f": "Sequence[float]",
    "SbDPRotation": "Sequence[float]",
    "SbRotation": "Sequence[float]",
    "SbVec2d": "Sequence[float]",
    "SbVec2f": "Sequence[float]",
    "SbVec2s": "Sequence[int]",
    "SbVec3d": "Sequence[float]",
    "SbVec3f": "Sequence[float]",
    "SbVec4d": "Sequence[float]",
    "SbVec4f": "Sequence[float]",
}
MATRIX_VALUE_RETURN_TYPES = {
    "SbDPMatrix": "Sequence[Sequence[float]]",
    "SbMatrix": "Sequence[Sequence[float]]",
}
MATRIX_ROW_RETURN_TYPES = {"SbMatrix": "Sequence[float]"}
STRING_POINTER_PARAMETERS = {
    ("SbName", "__eq__", "u"),
    ("SbName", "__nq__", "u"),
    ("SbString", "__eq__", "u"),
    ("SbString", "__nq__", "u"),
}
INPLACE_DIVISION_METHODS = {"__idiv__", "__itruediv__"}
PYTHON_HELPER_METHOD_TYPES = {
    ("_SwigNonDynamicMeta", "__setattr__"): (
        "cls, name: str, value: Any",
        "None",
    ),
    ("SoBase", "__nonzero__"): ("self", "bool"),
    ("SoBaseKit", "__getattr__"): ("self, name: str", "SoNode | SoField"),
    ("SoBaseKit", "__setattr__"): ("self, name: str, value: Any", "None"),
    ("SoEngine", "__getattr__"): (
        "self, name: str",
        "SoField | SoEngineOutput",
    ),
    ("SoEngine", "__setattr__"): ("self, name: str, value: Any", "None"),
    ("SoFieldContainer", "__dir__"): ("self", "list[str]"),
    ("SoFieldContainer", "__getattr__"): ("self, name: str", "SoField"),
    ("SoFieldContainer", "__setattr__"): (
        "self, name: str, value: Any",
        "None",
    ),
    ("SoGroup", "__iadd__"): ("self, other: SoNode | Sequence[SoNode]", "SoGroup"),
    ("SoGroup", "__isub__"): ("self, other: SoNode | Sequence[SoNode]", "SoGroup"),
    ("SoGroup", "__contains__"): ("self, node: SoNode", "bool"),
    ("SoGroup", "getByName"): ("self, name: SbName | str", "SoNode | None"),
    ("SoNodeKitPath", "index"): ("self", "Iterator[int]"),
    ("SoPath", "index"): ("self", "Iterator[int]"),
    ("SoType", "fromName"): ("name: SbName | str", "SoType"),
}
METHOD_RETURN_TYPE_OVERRIDES = {
    ("SoAction", "getNodeAppliedTo"): "SoNode | None",
    ("SoAction", "getPathAppliedTo"): "SoPath | None",
    ("SoAction", "getPathListAppliedTo"): "SoPathList | None",
    ("SoAction", "getOriginalPathListAppliedTo"): "SoPathList | None",
    ("SoSensor", "getNextInQueue"): "SoSensor | None",
    ("SoDataSensor", "getTriggerNode"): "SoNode | None",
    ("SoDataSensor", "getTriggerField"): "SoField | None",
    ("SoDataSensor", "getTriggerPath"): "SoPath | None",
    ("SoDataSensor", "getTriggerGroupChild"): "SoNode | None",
    ("SoDataSensor", "getTriggerReplacedGroupChild"): "SoNode | None",
    ("SoFieldSensor", "getAttachedField"): "SoField | None",
    ("SoNodeSensor", "getAttachedNode"): "SoNode | None",
    ("SoPathSensor", "getAttachedPath"): "SoPath | None",
    ("SoHandleEventAction", "getEvent"): "SoEvent | None",
    ("SoHandleEventAction", "getGrabber"): "SoNode | None",
    ("SoHandleEventAction", "getPickRoot"): "SoNode | None",
    ("SoHandleEventAction", "getPickedPoint"): "SoPickedPoint | None",
    ("SoGetBoundingBoxAction", "getResetPath"): "SoPath | None",
    ("SoRayPickAction", "getPickedPoint"): "SoPickedPoint | None",
    ("SoSearchAction", "getNode"): "SoNode | None",
    ("SoSearchAction", "getPath"): "SoPath | None",
    ("SoEngine", "getOutput"): "SoEngineOutput | None",
    ("SoNodeEngine", "getOutput"): "SoEngineOutput | None",
    ("SoEngineOutput", "getContainer"): "SoEngine | None",
    ("SoEngineOutput", "getNodeContainer"): "SoNodeEngine | None",
    ("SoEngineOutput", "getFieldContainer"): "SoFieldContainer | None",
    ("SoEngineOutputData", "getOutput"): "SoEngineOutput | None",
    ("SoInput", "findProto"): "SoProto | None",
    ("SoInput", "getCurrentProto"): "SoProto | None",
    ("SoInput", "getCurFileName"): "str | None",
    ("SoInput", "findReference"): "SoBase | None",
    ("SoOutput", "getCurrentProto"): "SoProto | None",
    ("SoBase", "getNamedBase"): "SoBase | None",
    ("SoFieldContainer", "getField"): "SoField | None",
    ("SoFieldContainer", "getEventIn"): "SoField | None",
    ("SoFieldContainer", "getEventOut"): "SoField | None",
    ("SoNode", "getChildren"): "SoChildList | None",
    ("SoPath", "getHead"): "SoNode | None",
    ("SoPath", "getTail"): "SoNode | None",
    ("SoQtRenderArea", "getSceneGraph"): "SoNode | None",
    ("SoQtRenderArea", "getOverlaySceneGraph"): "SoNode | None",
    ("SoQtViewer", "getCamera"): "SoCamera | None",
    ("SoQtViewer", "getSceneGraph"): "SoNode | None",
}
EXTEND_HELPER_METHOD_TYPES = {
    ("SoEngine", "getByName", "name: SbName"): (
        "name: SbName",
        "SoEngine | None",
    ),
    ("SoNode", "getByName", "name: SbName"): (
        "name: SbName | str",
        "SoNode | None",
    ),
    ("SoNode", "getByName", "name: SbName, l: SoNodeList"): (
        "name: SbName | str, l: SoNodeList",
        "int",
    ),
    ("SoPath", "getByName", "name: SbName"): (
        "name: str",
        "SoPath | None",
    ),
    ("SoPath", "getByName", "name: SbName, l: SoPathList"): (
        "name: str, l: SoPathList",
        "int",
    ),
    ("SoBase", "getNamedBase", "name: SbName, type: SoType"): (
        "name: SbName | str, type: SoType",
        "SoBase | None",
    ),
    ("SoFieldContainer", "getField", "self, name: SbName"): (
        "self, name: SbName | str",
        "SoField | None",
    ),
    ("SoFieldContainer", "getEventIn", "self, name: SbName"): (
        "self, name: SbName | str",
        "SoField | None",
    ),
    ("SoFieldContainer", "getEventOut", "self, name: SbName"): (
        "self, name: SbName | str",
        "SoField | None",
    ),
    ("SoCallbackAction", "getMaterial", "self, index: int = ..."): (
        "self, index: int = ...",
        "tuple[SbColor, SbColor, SbColor, SbColor, float, float]",
    ),
    ("SoFieldContainer", "getFieldName", "self, field: SoField"): (
        "self, field: SoField",
        "str | None",
    ),
    ("SoSensorManager", "isTimerSensorPending", "self"): (
        "self",
        "SbTime | None",
    ),
    ("SoType", "createInstance", "self"): (
        "self",
        "SoBase | SoField | SoPath | None",
    ),
    ("SbMatrix", "getTransform", "self"): (
        "self",
        "tuple[SbVec3f, SbRotation, SbVec3f, SbRotation]",
    ),
    ("SbMatrix", "getTransform", "self, center: SbVec3f"): (
        "self, center: SbVec3f",
        "tuple[SbVec3f, SbRotation, SbVec3f, SbRotation]",
    ),
    ("SbMatrix", "multMatrixVec", "self, src: SbVec3f"): (
        "self, src: SbVec3f",
        "SbVec3f",
    ),
    ("SbMatrix", "multDirMatrix", "self, src: SbVec3f"): (
        "self, src: SbVec3f",
        "SbVec3f",
    ),
    ("SbMatrix", "multVecMatrix", "self, src: SbVec3f"): (
        "self, src: SbVec3f",
        "SbVec3f",
    ),
    ("SbMatrix", "multVecMatrix", "self, src: SbVec4f"): (
        "self, src: SbVec4f",
        "SbVec4f",
    ),
    ("SbRotation", "getAxisAngle", "self"): (
        "self",
        "tuple[SbVec3f, float]",
    ),
    ("SbRotation", "getMatrix", "self"): ("self", "SbMatrix"),
    ("SbRotation", "multVec", "self, src: SbVec3f"): (
        "self, src: SbVec3f",
        "SbVec3f",
    ),
    ("SbDPRotation", "getAxisAngle", "self"): (
        "self",
        "tuple[SbVec3d, float]",
    ),
    ("SbDPRotation", "getMatrix", "self"): ("self", "SbDPMatrix"),
    ("SbViewVolume", "projectPointToLine", "self, SbVec3f: Incomplete"): (
        "self, pt: SbVec2f",
        "tuple[SbVec3f, SbVec3f]",
    ),
    ("SbViewVolume", "projectToScreen", "self, arg1: SbVec3f"): (
        "self, src: SbVec3f",
        "SbVec3f",
    ),
}
CALLBACK_PARAMETER_NAMES = {
    "callback",
    "cb",
    "f",
    "func",
    "function",
    "pyfunc",
    "sensorQueueChangedCB",
}
CALLBACK_DATA_PARAMETER_NAMES = {
    "callbackdata",
    "cbuserdata",
    "closure",
    "data",
    "user",
    "userdata",
    "userData",
}
CALLBACK_HANDLE_PARAMETER_NAMES = {"tuple"}
CALLBACK_TYPE_SIGNATURES = {
    "ScXMLStateChangeCB": (
        "Callable[[Any, ScXMLStateMachine, str, bool, bool], None]"
    ),
    "ScXMLStateMachineDeleteCB": "Callable[[Any, ScXMLStateMachine], None]",
    "SoCallbackAction::SoCallbackActionCB": (
        "Callable[[Any, SoCallbackAction, SoNode], int]"
    ),
    "SoCallbackCB": "Callable[[Any, SoAction], None]",
    "SoDraggerCB": "Callable[[Any, SoDragger], None]",
    "SoEventCallbackCB": "Callable[[Any, SoEventCallback], None]",
    "SoGLPreRenderCB": "Callable[[Any, SoGLRenderAction], None]",
    "SoGLRenderAction::SoGLRenderAbortCB": "Callable[[Any], int]",
    "SoGLRenderPassCB": "Callable[[Any], None]",
    "SoIntersectionDetectionAction::SoIntersectionCB": (
        "Callable[[Any, SoIntersectingPrimitive, SoIntersectingPrimitive], int]"
    ),
    "SoIntersectionDetectionAction::SoIntersectionFilterCB": (
        "Callable[[Any, SoPath, SoPath], bool]"
    ),
    "SoIntersectionDetectionAction::SoIntersectionVisitationCB": (
        "Callable[[Any, SoPath], int]"
    ),
    "SoLineSegmentCB": (
        "Callable[[Any, SoCallbackAction, SoPrimitiveVertex, "
        "SoPrimitiveVertex], None]"
    ),
    "SoPointCB": "Callable[[Any, SoCallbackAction, SoPrimitiveVertex], None]",
    "SoRenderManagerRenderCB": "Callable[[Any, SoRenderManager], None]",
    "SoSceneManagerRenderCB": "Callable[[Any, SoSceneManager], None]",
    "SoSelectionClassCB": "Callable[[Any, SoSelection], None]",
    "SoSelectionPathCB": "Callable[[Any, SoPath], None]",
    "SoSelectionPickCB": "Callable[[Any, SoPickedPoint], SoPath]",
    "SoTriangleCB": (
        "Callable[[Any, SoCallbackAction, SoPrimitiveVertex, "
        "SoPrimitiveVertex, SoPrimitiveVertex], None]"
    ),
    "SoQtRenderAreaEventCB": "Callable[[Any, QEvent], Any]",
}
FUNCTION_POINTER_TYPE_SIGNATURES = {"void(*)(void*)": "Callable[[Any], None]"}
SENSOR_CALLBACK_CLASSES = {
    "SoAlarmSensor",
    "SoDelayQueueSensor",
    "SoFieldSensor",
    "SoIdleSensor",
    "SoNodeSensor",
    "SoOneShotSensor",
    "SoPathSensor",
    "SoTimerQueueSensor",
    "SoTimerSensor",
}
KNOWN_ITER_ELEMENT_TYPES = {
    "SbIntList": "int",
    "SbName": "str",
    "SbPList": "Any",
    "SbString": "str",
    "SbVec2d": "float",
    "SbVec2f": "float",
    "SbVec2s": "int",
    "SbVec3d": "float",
    "SbVec3f": "float",
    "SbVec3s": "int",
    "SbVec4d": "float",
    "SbVec4f": "float",
    "SoMField": "Any",
    "SoNodeKitPath": "SoNode",
    "SoPath": "SoNode",
}
RUNTIME_UNSUPPORTED_NOTE = (
    "NOTE: SWIG exposes raw C pointers here; keep Incomplete until a "
    "Python-level wrapper exists."
)
RUNTIME_UNSUPPORTED_METHOD_NOTES = {
    "pivy.coin": {
        ("SoDataSensor", "setDeleteCallback"),
        ("SoDebugError", "setHandlerCallback"),
        ("SoError", "setHandlerCallback"),
        ("SoGLImage", "setEndFrameCallback"),
        ("SoMFDouble", "getValues"),
        ("SoMFDouble", "setValues"),
        ("SoMemoryError", "setHandlerCallback"),
        ("SoReadError", "setHandlerCallback"),
        ("SoSensor", "setFunction"),
    },
    "pivy.gui.soqt": {
        ("SoDebugError", "setHandlerCallback"),
        ("SoError", "setHandlerCallback"),
    },
}
GENERATED_HEADER = (
    "# SPDX-License-Identifier: ISC\n"
    "# Generated from local Pivy stubgen output; lightly normalized for checker use.\n"
    "\n"
)
PRIVATE_EXTENSION_STUB = (
    GENERATED_HEADER
    + "from typing import Any\n"
    + "\n"
    + "def cast(*args: Any, **kwargs: Any) -> Any: ...\n"
)


def normalized_name(value: str | None) -> str:
    return "".join(
        character for character in (value or "").lower() if character.isalnum()
    )


INCOMPLETE_CATEGORIES = (
    "raw C pointers",
    "callbacks",
    "unknown output parameters",
    "function pointers",
    "dynamic/runtime API",
    "uncategorized",
)


@dataclass(frozen=True)
class FieldTypePolicy:
    """Python-level value policy for a single-value Coin field."""

    value_type: str
    setter_argument_type: str
    setter_value_type: str
    setter_parameter_name: str = "newvalue"


@dataclass(frozen=True)
class MultifieldTypePolicy:
    """Python-level value policy for a multiple-value Coin field."""

    element_type: str
    set_values_types: tuple[str, ...] = ()


FIELD_TYPE_POLICIES = {
    "SoSFNode": FieldTypePolicy(
        value_type="SoNode | None",
        setter_argument_type="SoNode",
        setter_value_type="SoNode | None",
    ),
    "SoSFPath": FieldTypePolicy(
        value_type="SoPath | None",
        setter_argument_type="SoPath",
        setter_value_type="SoPath | None",
    ),
}


MULTIFIELD_TYPE_POLICIES = {
    "SoMFName": MultifieldTypePolicy(
        element_type="SbName",
        set_values_types=("SbName | str",),
    ),
    "SoMFBool": MultifieldTypePolicy(
        element_type="bool",
        set_values_types=("bool",),
    ),
    "SoMFEnum": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
    ),
    "SoMFFloat": MultifieldTypePolicy(
        element_type="float",
        set_values_types=("float",),
    ),
    "SoMFVec3f": MultifieldTypePolicy(
        element_type="SbVec3f",
        set_values_types=("SbVec3f", "Sequence[float]"),
    ),
    "SoMFString": MultifieldTypePolicy(
        element_type="SbString",
        set_values_types=("SbString | str",),
    ),
    "SoMFVec2f": MultifieldTypePolicy(
        element_type="SbVec2f",
        set_values_types=("SbVec2f", "Sequence[float]"),
    ),
    "SoMFVec4f": MultifieldTypePolicy(
        element_type="SbVec4f",
        set_values_types=("SbVec4f", "Sequence[float]"),
    ),
    "SoMFRotation": MultifieldTypePolicy(
        element_type="SbRotation",
        set_values_types=("SbRotation", "Sequence[float]"),
    ),
    "SoMFMatrix": MultifieldTypePolicy(
        element_type="SbMatrix",
        set_values_types=("SbMatrix",),
    ),
    "SoMFColor": MultifieldTypePolicy(
        element_type="SbColor",
        set_values_types=("SbColor", "SbVec3f", "Sequence[float]"),
    ),
    "SoMFColorRGBA": MultifieldTypePolicy(element_type="SbColor4f"),
    "SoMFDouble": MultifieldTypePolicy(element_type="float"),
    "SoMFEngine": MultifieldTypePolicy(
        element_type="SoEngine",
        set_values_types=("SoEngine",),
    ),
    "SoMFInt32": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
    ),
    "SoMFNode": MultifieldTypePolicy(
        element_type="SoNode",
        set_values_types=("SoNode",),
    ),
    "SoMFPath": MultifieldTypePolicy(
        element_type="SoPath",
        set_values_types=("SoPath",),
    ),
    "SoMFPlane": MultifieldTypePolicy(
        element_type="SbPlane",
        set_values_types=("SbPlane",),
    ),
    "SoMFShort": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
    ),
    "SoMFTime": MultifieldTypePolicy(
        element_type="SbTime",
        set_values_types=("SbTime",),
    ),
    "SoMFUInt32": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
    ),
    "SoMFUShort": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
    ),
    "SoMFVec2b": MultifieldTypePolicy(element_type="SbVec2b"),
    "SoMFVec2d": MultifieldTypePolicy(element_type="SbVec2d"),
    "SoMFVec2i32": MultifieldTypePolicy(element_type="SbVec2i32"),
    "SoMFVec2s": MultifieldTypePolicy(element_type="SbVec2s"),
    "SoMFVec3b": MultifieldTypePolicy(element_type="SbVec3b"),
    "SoMFVec3d": MultifieldTypePolicy(
        element_type="SbVec3d",
        set_values_types=("SbVec3d", "Sequence[float]"),
    ),
    "SoMFVec3i32": MultifieldTypePolicy(element_type="SbVec3i32"),
    "SoMFVec3s": MultifieldTypePolicy(element_type="SbVec3s"),
    "SoMFVec4b": MultifieldTypePolicy(element_type="SbVec4b"),
    "SoMFVec4d": MultifieldTypePolicy(element_type="SbVec4d"),
    "SoMFVec4i32": MultifieldTypePolicy(element_type="SbVec4i32"),
    "SoMFVec4s": MultifieldTypePolicy(element_type="SbVec4s"),
    "SoMFVec4ub": MultifieldTypePolicy(element_type="SbVec4ub"),
    "SoMFVec4ui32": MultifieldTypePolicy(element_type="SbVec4ui32"),
    "SoMFVec4us": MultifieldTypePolicy(element_type="SbVec4us"),
}


def multifield_iter_element_types():
    """Return the element annotation used by each multifield iterator."""

    return {
        field_class: policy.element_type
        for field_class, policy in MULTIFIELD_TYPE_POLICIES.items()
    }


def multifield_setvalues_types():
    """Return supported Python sequence element types for ``setValues``."""

    return {
        field_class: policy.set_values_types
        for field_class, policy in MULTIFIELD_TYPE_POLICIES.items()
        if policy.set_values_types
    }


def field_method_type_overrides():
    """Return generator overrides derived from the field policies."""

    overrides = {}
    for field_class, policy in FIELD_TYPE_POLICIES.items():
        overrides[(field_class, "getValue", "self")] = (
            "self",
            policy.value_type,
        )
        setter_signature = "self, %s: %s" % (
            policy.setter_parameter_name,
            policy.setter_argument_type,
        )
        setter_arguments = "self, %s: %s" % (
            policy.setter_parameter_name,
            policy.setter_value_type,
        )
        overrides[(field_class, "setValue", setter_signature)] = (
            setter_arguments,
            "None",
        )
    return overrides


@dataclass(frozen=True)
class IncompleteRule:
    """One explicit rule for classifying an ``Incomplete`` annotation."""

    category: str
    kind: str | None = None
    class_names: frozenset[str] = frozenset()
    class_name_contains: tuple[str, ...] = ()
    class_name_suffixes: tuple[str, ...] = ()
    method_names: frozenset[str] = frozenset()
    method_name_contains: tuple[str, ...] = ()
    method_name_prefixes: tuple[str, ...] = ()
    parameter_names: frozenset[str] = frozenset()
    parameter_method_names: frozenset[str] = frozenset()
    parameter_method_prefixes: tuple[str, ...] = ()
    parameter_name_prefixes: tuple[str, ...] = ()
    parameter_name_suffixes: tuple[str, ...] = ()
    raw_pointer_note: bool = False

    def matches(
        self,
        *,
        kind: str,
        class_name: str,
        method_name: str | None,
        parameter_name: str,
        has_raw_pointer_note: bool,
    ) -> bool:
        if self.kind is not None and self.kind != kind:
            return False

        class_name = normalized_name(class_name)
        method_name = normalized_name(method_name)
        parameter_name = normalized_name(parameter_name)

        selectors = (
            class_name in self.class_names,
            any(value in class_name for value in self.class_name_contains),
            any(class_name.endswith(value) for value in self.class_name_suffixes),
            method_name in self.method_names,
            any(value in method_name for value in self.method_name_contains),
            any(method_name.startswith(value) for value in self.method_name_prefixes),
            parameter_name in self.parameter_names,
            parameter_name in self.parameter_method_names
            and any(
                method_name.startswith(value)
                for value in self.parameter_method_prefixes
            ),
            any(
                parameter_name.startswith(value)
                for value in self.parameter_name_prefixes
            ),
            any(
                parameter_name.endswith(value)
                for value in self.parameter_name_suffixes
            ),
            self.raw_pointer_note and has_raw_pointer_note,
        )
        return any(selectors)


RAW_POINTER_PARAMETER_NAMES = frozenset(
    {
        "buf",
        "buffer",
        "bytes",
        "c",
        "data",
        "file",
        "fp",
        "fptr",
        "newfp",
        "pixels",
        "pixelblocks",
        "pointer",
        "strings",
    }
)
RAW_POINTER_METHOD_NAMES = frozenset(
    {
        "getbuffer",
        "getcurfile",
        "getfilepointer",
        "getpackedarrayptr",
        "getpackedcolors",
        "getcolorindexpointer",
        "gettransparencypointer",
        "output",
        "readbinaryarray",
        "setbuffer",
        "setfilepointer",
        "setstringarray",
        "writebinaryarray",
    }
)
RAW_POINTER_CLASSES = frozenset(
    {
        "sbimage",
        "soinput",
        "somultitextureimageelement",
        "sooutput",
        "sosfimage",
        "sosfimage3",
    }
)

FUNCTION_POINTER_METHOD_NAMES = frozenset(
    {"addmethod", "apply", "applytoall", "sethashingfunction"}
)
FUNCTION_POINTER_PARAMETER_NAMES = frozenset({"method", "rtn", "reallocfunc"})

OUTPUT_PARAMETER_NAMES = frozenset(
    {
        "array",
        "exceptfds",
        "indices",
        "names",
        "num",
        "numcomponents",
        "numcoordindices",
        "numindices",
        "numstrips",
        "numtransp",
        "numvalues",
        "readfds",
        "values",
        "writefds",
    }
)

EXPLICIT_CALLBACK_PARAMETER_NAMES = frozenset(
    normalized_name(name)
    for name in CALLBACK_PARAMETER_NAMES
    if name in {"callback", "cb", "pyfunc", "sensorQueueChangedCB"}
)


INCOMPLETE_RULES = (
    IncompleteRule(
        "function pointers",
        method_names=FUNCTION_POINTER_METHOD_NAMES,
        parameter_names=FUNCTION_POINTER_PARAMETER_NAMES,
        class_name_suffixes=("funcs",),
    ),
    IncompleteRule(
        "callbacks",
        class_name_contains=("callback",),
        method_name_contains=("callback",),
        parameter_names=EXPLICIT_CALLBACK_PARAMETER_NAMES,
        parameter_name_suffixes=("callback", "cb"),
    ),
    IncompleteRule(
        "dynamic/runtime API",
        kind="return",
        method_names=frozenset({"createinstance"}),
    ),
    IncompleteRule(
        "raw C pointers",
        method_names=RAW_POINTER_METHOD_NAMES,
        parameter_names=RAW_POINTER_PARAMETER_NAMES,
        raw_pointer_note=True,
        kind=None,
    ),
    IncompleteRule(
        "raw C pointers",
        kind="return",
        class_names=RAW_POINTER_CLASSES,
    ),
    IncompleteRule(
        "unknown output parameters",
        kind="parameter",
        parameter_method_names=OUTPUT_PARAMETER_NAMES,
        parameter_method_prefixes=("get", "read", "set", "use", "generate"),
    ),
    IncompleteRule(
        "unknown output parameters",
        kind="parameter",
        parameter_name_prefixes=("out",),
    ),
    IncompleteRule(
        "unknown output parameters",
        kind="parameter",
        parameter_name_suffixes=("out",),
    ),
)

# Conservative inventory for currently opaque or domain-specific surfaces. These
# remain ``Incomplete`` intentionally, but they are known deferred runtime API
# work rather than unknown typing holes. New sites must be added deliberately.
TRIAGED_INCOMPLETE_SITES = frozenset(
    {
        ('attribute', 'SoMField', None, 'values'),
        ('parameter', 'SbBSPTree', 'addPoint', 'userdata'),
        ('parameter', 'SbBSPTree', 'findClosest', 'array'),
        ('parameter', 'SbBSPTree', 'findPoints', 'array'),
        ('parameter', 'SbBox2i32', 'getBounds', 'xmax'),
        ('parameter', 'SbBox2i32', 'getBounds', 'xmin'),
        ('parameter', 'SbBox2i32', 'getBounds', 'ymax'),
        ('parameter', 'SbBox2i32', 'getBounds', 'ymin'),
        ('parameter', 'SbBox2i32', 'getOrigin', 'originX'),
        ('parameter', 'SbBox2i32', 'getOrigin', 'originY'),
        ('parameter', 'SbBox2i32', 'getSize', 'sizeX'),
        ('parameter', 'SbBox2i32', 'getSize', 'sizeY'),
        ('parameter', 'SbBox2s', 'getBounds', 'xmax'),
        ('parameter', 'SbBox2s', 'getBounds', 'xmin'),
        ('parameter', 'SbBox2s', 'getBounds', 'ymax'),
        ('parameter', 'SbBox2s', 'getBounds', 'ymin'),
        ('parameter', 'SbBox2s', 'getOrigin', 'originX'),
        ('parameter', 'SbBox2s', 'getOrigin', 'originY'),
        ('parameter', 'SbBox2s', 'getSize', 'sizeX'),
        ('parameter', 'SbBox2s', 'getSize', 'sizeY'),
        ('parameter', 'SbBox3i32', 'getBounds', 'xmax'),
        ('parameter', 'SbBox3i32', 'getBounds', 'xmin'),
        ('parameter', 'SbBox3i32', 'getBounds', 'ymax'),
        ('parameter', 'SbBox3i32', 'getBounds', 'ymin'),
        ('parameter', 'SbBox3i32', 'getBounds', 'zmax'),
        ('parameter', 'SbBox3i32', 'getBounds', 'zmin'),
        ('parameter', 'SbBox3i32', 'getOrigin', 'originX'),
        ('parameter', 'SbBox3i32', 'getOrigin', 'originY'),
        ('parameter', 'SbBox3i32', 'getOrigin', 'originZ'),
        ('parameter', 'SbBox3i32', 'getSize', 'sizeX'),
        ('parameter', 'SbBox3i32', 'getSize', 'sizeY'),
        ('parameter', 'SbBox3i32', 'getSize', 'sizeZ'),
        ('parameter', 'SbBox3s', 'getBounds', 'xmax'),
        ('parameter', 'SbBox3s', 'getBounds', 'xmin'),
        ('parameter', 'SbBox3s', 'getBounds', 'ymax'),
        ('parameter', 'SbBox3s', 'getBounds', 'ymin'),
        ('parameter', 'SbBox3s', 'getBounds', 'zmax'),
        ('parameter', 'SbBox3s', 'getBounds', 'zmin'),
        ('parameter', 'SbBox3s', 'getOrigin', 'originX'),
        ('parameter', 'SbBox3s', 'getOrigin', 'originY'),
        ('parameter', 'SbBox3s', 'getOrigin', 'originZ'),
        ('parameter', 'SbBox3s', 'getSize', 'sizeX'),
        ('parameter', 'SbBox3s', 'getSize', 'sizeY'),
        ('parameter', 'SbBox3s', 'getSize', 'sizeZ'),
        ('parameter', 'SbClip', '__init__', 'userdata'),
        ('parameter', 'SbClip', 'addVertex', 'vdata'),
        ('parameter', 'SbClip', 'getVertex', 'vdata'),
        ('parameter', 'SbDPMatrix', 'LUBackSubstitution', 'index'),
        ('parameter', 'SbDPMatrix', 'LUDecomposition', 'index'),
        ('parameter', 'SbDPMatrix', '__init__', 'matrix'),
        ('parameter', 'SbDPMatrix', 'getValue', 'm'),
        ('parameter', 'SbDPMatrix', 'setValue', 'pMat'),
        ('parameter', 'SbDict', 'enter', 'value'),
        ('parameter', 'SbDict', 'find', 'value'),
        ('parameter', 'SbFifo', 'assign', 'ptr'),
        ('parameter', 'SbFifo', 'contains', 'item'),
        ('parameter', 'SbFifo', 'peek', 'item'),
        ('parameter', 'SbFifo', 'peek', 'type'),
        ('parameter', 'SbFifo', 'reclaim', 'item'),
        ('parameter', 'SbFifo', 'retrieve', 'ptr'),
        ('parameter', 'SbFifo', 'retrieve', 'type'),
        ('parameter', 'SbFifo', 'tryRetrieve', 'ptr'),
        ('parameter', 'SbFifo', 'tryRetrieve', 'type'),
        ('parameter', 'SbHeap', 'add', 'obj'),
        ('parameter', 'SbHeap', 'newWeight', 'obj'),
        ('parameter', 'SbHeap', 'remove', 'obj'),
        ('parameter', 'SbHeap', 'traverseHeap', 'func'),
        ('parameter', 'SbHeap', 'traverseHeap', 'userdata'),
        ('parameter', 'SbImage', 'addReadImageCB', 'closure'),
        ('parameter', 'SbImage', 'removeReadImageCB', 'closure'),
        ('parameter', 'SbImage', 'scheduleReadFile', 'closure'),
        ('parameter', 'SbMatrix', 'LUBackSubstitution', 'index'),
        ('parameter', 'SbMatrix', 'LUDecomposition', 'index'),
        ('parameter', 'SbMatrix', '__init__', 'matrix'),
        ('parameter', 'SbMatrix', 'getValue', 'm'),
        ('parameter', 'SbMatrix', 'setValue', 'pMat'),
        ('parameter', 'SbOctTree', 'addItem', 'item'),
        ('parameter', 'SbOctTree', 'findItems', 'destarray'),
        ('parameter', 'SbOctTree', 'removeItem', 'item'),
        ('parameter', 'SbPlane', 'intersect', 'SbPlane'),
        ('parameter', 'SbStorage', '__init__', 'constr'),
        ('parameter', 'SbStorage', '__init__', 'destr'),
        ('parameter', 'SbTesselator', '__init__', 'func'),
        ('parameter', 'SbThread', 'create', 'closure'),
        ('parameter', 'SbThread', 'create', 'func'),
        ('parameter', 'SbThread', 'join', 'retval'),
        ('parameter', 'SbTime', '__init__', 'tv'),
        ('parameter', 'SbTime', 'getValue', 'sec'),
        ('parameter', 'SbTime', 'getValue', 'tv'),
        ('parameter', 'SbTime', 'setValue', 'tv'),
        ('parameter', 'SbVec2b', '__init__', 'v'),
        ('parameter', 'SbVec2b', 'getValue', 'x'),
        ('parameter', 'SbVec2b', 'getValue', 'y'),
        ('parameter', 'SbVec2b', 'setValue', 'v'),
        ('parameter', 'SbVec2i32', '__init__', 'v'),
        ('parameter', 'SbVec2i32', 'getValue', 'x'),
        ('parameter', 'SbVec2i32', 'getValue', 'y'),
        ('parameter', 'SbVec2i32', 'setValue', 'v'),
        ('parameter', 'SbVec2s', '__init__', 'v'),
        ('parameter', 'SbVec2s', 'setValue', 'v'),
        ('parameter', 'SbVec3b', '__init__', 'v'),
        ('parameter', 'SbVec3b', 'getValue', 'x'),
        ('parameter', 'SbVec3b', 'getValue', 'y'),
        ('parameter', 'SbVec3b', 'getValue', 'z'),
        ('parameter', 'SbVec3b', 'setValue', 'v'),
        ('parameter', 'SbVec3i32', '__init__', 'v'),
        ('parameter', 'SbVec3i32', 'getValue', 'x'),
        ('parameter', 'SbVec3i32', 'getValue', 'y'),
        ('parameter', 'SbVec3i32', 'getValue', 'z'),
        ('parameter', 'SbVec3i32', 'setValue', 'v'),
        ('parameter', 'SbVec3s', '__init__', 'v'),
        ('parameter', 'SbVec3s', 'setValue', 'v'),
        ('parameter', 'SbVec4b', '__init__', 'v'),
        ('parameter', 'SbVec4b', 'getValue', 'w'),
        ('parameter', 'SbVec4b', 'getValue', 'x'),
        ('parameter', 'SbVec4b', 'getValue', 'y'),
        ('parameter', 'SbVec4b', 'getValue', 'z'),
        ('parameter', 'SbVec4b', 'setValue', 'v'),
        ('parameter', 'SbVec4i32', '__init__', 'v'),
        ('parameter', 'SbVec4i32', 'getValue', 'w'),
        ('parameter', 'SbVec4i32', 'getValue', 'x'),
        ('parameter', 'SbVec4i32', 'getValue', 'y'),
        ('parameter', 'SbVec4i32', 'getValue', 'z'),
        ('parameter', 'SbVec4i32', 'setValue', 'v'),
        ('parameter', 'SbVec4s', '__init__', 'v'),
        ('parameter', 'SbVec4s', 'getValue', 'w'),
        ('parameter', 'SbVec4s', 'setValue', 'v'),
        ('parameter', 'SbVec4ub', '__init__', 'v'),
        ('parameter', 'SbVec4ub', 'getValue', 'w'),
        ('parameter', 'SbVec4ub', 'getValue', 'x'),
        ('parameter', 'SbVec4ub', 'getValue', 'y'),
        ('parameter', 'SbVec4ub', 'getValue', 'z'),
        ('parameter', 'SbVec4ub', 'setValue', 'v'),
        ('parameter', 'SbVec4ui32', '__init__', 'v'),
        ('parameter', 'SbVec4ui32', 'getValue', 'w'),
        ('parameter', 'SbVec4ui32', 'getValue', 'x'),
        ('parameter', 'SbVec4ui32', 'getValue', 'y'),
        ('parameter', 'SbVec4ui32', 'getValue', 'z'),
        ('parameter', 'SbVec4ui32', 'setValue', 'v'),
        ('parameter', 'SbVec4us', '__init__', 'v'),
        ('parameter', 'SbVec4us', 'getValue', 'w'),
        ('parameter', 'SbVec4us', 'getValue', 'x'),
        ('parameter', 'SbVec4us', 'getValue', 'y'),
        ('parameter', 'SbVec4us', 'getValue', 'z'),
        ('parameter', 'SbVec4us', 'setValue', 'v'),
        ('parameter', 'ScXMLDocument', 'readXMLData', 'xmldoc'),
        ('parameter', 'ScXMLEltReader', 'read', 'elt'),
        ('parameter', 'ScXMLEvent', 'getAssociationKeys', 'keys'),
        ('parameter', 'ScXMLStateMachine', 'setEnabledModulesList', 'modulenames'),
        ('parameter', 'SoActionMethodList', '__setitem__', 'value'),
        ('parameter', 'SoAuditorList', 'append', 'auditor'),
        ('parameter', 'SoAuditorList', 'find', 'auditor'),
        ('parameter', 'SoAuditorList', 'remove', 'auditor'),
        ('parameter', 'SoAuditorList', 'set', 'auditor'),
        ('parameter', 'SoBase', 'addAuditor', 'auditor'),
        ('parameter', 'SoBase', 'removeAuditor', 'auditor'),
        ('parameter', 'SoByteStream', 'copy', 'd'),
        ('parameter', 'SoChildList', 'traverseInPath', 'indices'),
        ('parameter', 'SoConvexDataCache', 'generate', 'coordindices'),
        ('parameter', 'SoConvexDataCache', 'generate', 'matindices'),
        ('parameter', 'SoConvexDataCache', 'generate', 'normindices'),
        ('parameter', 'SoConvexDataCache', 'generate', 'texindices'),
        ('parameter', 'SoDB', 'doSelect', 'exceptfds'),
        ('parameter', 'SoDB', 'doSelect', 'readfds'),
        ('parameter', 'SoDB', 'doSelect', 'writefds'),
        ('parameter', 'SoDB', 'getHeaderData', 'userdata'),
        ('parameter', 'SoDB', 'registerHeader', 'userdata'),
        ('parameter', 'SoEnvironmentElement', 'get', 'fogType'),
        ('parameter', 'SoEnvironmentElement', 'getDefault', 'fogType'),
        ('parameter', 'SoField', 'addAuditor', 'f'),
        ('parameter', 'SoField', 'removeAuditor', 'f'),
        ('parameter', 'SoFieldContainer', 'getFieldsMemorySize', 'managed'),
        ('parameter', 'SoFieldContainer', 'getFieldsMemorySize', 'unmanaged'),
        ('parameter', 'SoFieldContainer', 'setUserData', 'userdata'),
        ('parameter', 'SoFieldContainer', 'validateNewFieldValue', 'newval'),
        ('parameter', 'SoGLImage', 'setPBuffer', 'context'),
        ('parameter', 'SoGLLazyElement', 'sendVPPacked', 'pcolor'),
        ('parameter', 'SoGLLazyElement', 'setMaterialElt', 'transp'),
        ('parameter', 'SoGLLazyElement', 'setPackedElt', 'colors'),
        ('parameter', 'SoGLLazyElement', 'setTranspElt', 'transp'),
        ('parameter', 'SoGLLazyElement', 'updateColorVBO', 'vbo'),
        ('parameter', 'SoGLMultiTextureCoordinateElement', 'initRender', 'enabled'),
        ('parameter', 'SoGLMultiTextureImageElement', 'get', 'model'),
        ('parameter', 'SoGLRenderAction', 'setSortedObjectOrderStrategy', 'closure'),
        ('parameter', 'SoGLVBOElement', 'setColorVBO', 'vbo'),
        ('parameter', 'SoGLVBOElement', 'setNormalVBO', 'vbo'),
        ('parameter', 'SoGLVBOElement', 'setTexCoordVBO', 'vbo'),
        ('parameter', 'SoGLVBOElement', 'setVertexVBO', 'vbo'),
        ('parameter', 'SoHeightMapToNormalMap', 'convert', 'srcptr'),
        ('parameter', 'SoInput', 'read', 'i'),
        ('parameter', 'SoInput', 'read', 's'),
        ('parameter', 'SoInput', 'readByte', 'b'),
        ('parameter', 'SoInput', 'readHex', 'l'),
        ('parameter', 'SoLazyElement', 'setMaterials', 'transp'),
        ('parameter', 'SoLazyElement', 'setTransparency', 'transparency'),
        ('parameter', 'SoLinearProfile', 'getTrimCurve', 'knotvector'),
        ('parameter', 'SoLinearProfile', 'getTrimCurve', 'numknots'),
        ('parameter', 'SoLinearProfile', 'getTrimCurve', 'numpoints'),
        ('parameter', 'SoLinearProfile', 'getTrimCurve', 'points'),
        ('parameter', 'SoLinearProfile', 'getVertices', 'numvertices'),
        ('parameter', 'SoLockManager', 'SetUnlockString', 'unlockstr'),
        ('parameter', 'SoMFBool', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFColor', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFColorRGBA', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFDouble', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFFloat', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFInt32', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFShort', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFUInt32', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFUShort', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec2b', 'set1Value', 'xy'),
        ('parameter', 'SoMFVec2b', 'setValue', 'xy'),
        ('parameter', 'SoMFVec2b', 'setValues', 'xy'),
        ('parameter', 'SoMFVec2b', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec2d', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec2f', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec2i32', 'set1Value', 'xy'),
        ('parameter', 'SoMFVec2i32', 'setValue', 'xy'),
        ('parameter', 'SoMFVec2i32', 'setValues', 'xy'),
        ('parameter', 'SoMFVec2i32', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec2s', 'set1Value', 'xy'),
        ('parameter', 'SoMFVec2s', 'setValue', 'xy'),
        ('parameter', 'SoMFVec2s', 'setValues', 'xy'),
        ('parameter', 'SoMFVec2s', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec3b', 'set1Value', 'xyz'),
        ('parameter', 'SoMFVec3b', 'setValue', 'xyz'),
        ('parameter', 'SoMFVec3b', 'setValues', 'xyz'),
        ('parameter', 'SoMFVec3b', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec3d', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec3f', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec3i32', 'set1Value', 'xyz'),
        ('parameter', 'SoMFVec3i32', 'setValue', 'xyz'),
        ('parameter', 'SoMFVec3i32', 'setValues', 'xyz'),
        ('parameter', 'SoMFVec3i32', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec3s', 'set1Value', 'xyz'),
        ('parameter', 'SoMFVec3s', 'setValue', 'xyz'),
        ('parameter', 'SoMFVec3s', 'setValues', 'xyz'),
        ('parameter', 'SoMFVec3s', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4b', 'set1Value', 'xyzw'),
        ('parameter', 'SoMFVec4b', 'setValue', 'xyzw'),
        ('parameter', 'SoMFVec4b', 'setValues', 'xyzw'),
        ('parameter', 'SoMFVec4b', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4d', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4f', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4i32', 'set1Value', 'xyzw'),
        ('parameter', 'SoMFVec4i32', 'setValue', 'xyzw'),
        ('parameter', 'SoMFVec4i32', 'setValues', 'xyzw'),
        ('parameter', 'SoMFVec4i32', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4s', 'set1Value', 'xyzw'),
        ('parameter', 'SoMFVec4s', 'setValue', 'xyzw'),
        ('parameter', 'SoMFVec4s', 'setValues', 'xyzw'),
        ('parameter', 'SoMFVec4s', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4ub', 'set1Value', 'xyzw'),
        ('parameter', 'SoMFVec4ub', 'setValue', 'xyzw'),
        ('parameter', 'SoMFVec4ub', 'setValues', 'xyzw'),
        ('parameter', 'SoMFVec4ub', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4ui32', 'set1Value', 'xyzw'),
        ('parameter', 'SoMFVec4ui32', 'setValue', 'xyzw'),
        ('parameter', 'SoMFVec4ui32', 'setValues', 'xyzw'),
        ('parameter', 'SoMFVec4ui32', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMFVec4us', 'set1Value', 'xyzw'),
        ('parameter', 'SoMFVec4us', 'setValue', 'xyzw'),
        ('parameter', 'SoMFVec4us', 'setValues', 'xyzw'),
        ('parameter', 'SoMFVec4us', 'setValuesPointer', 'userdata'),
        ('parameter', 'SoMarkerSet', 'addMarker', 'string'),
        ('parameter', 'SoMultiTextureImageElement', 'get', 'model'),
        ('parameter', 'SoMultiTextureImageElement', 'get', 'wrapR'),
        ('parameter', 'SoMultiTextureImageElement', 'get', 'wrapS'),
        ('parameter', 'SoMultiTextureImageElement', 'get', 'wrapT'),
        ('parameter', 'SoNormalCache', 'generatePerFace', 'coordindices'),
        ('parameter', 'SoNormalCache', 'generatePerFaceStrip', 'coordindices'),
        ('parameter', 'SoNormalCache', 'generatePerStrip', 'coordindices'),
        ('parameter', 'SoNormalCache', 'generatePerVertex', 'coordindices'),
        ('parameter', 'SoNormalGenerator', 'generate', 'striplens'),
        ('parameter', 'SoNormalGenerator', 'generatePerStrip', 'striplens'),
        ('parameter', 'SoNurbsProfile', 'getTrimCurve', 'knotvector'),
        ('parameter', 'SoNurbsProfile', 'getTrimCurve', 'numknots'),
        ('parameter', 'SoNurbsProfile', 'getTrimCurve', 'numpoints'),
        ('parameter', 'SoNurbsProfile', 'getTrimCurve', 'points'),
        ('parameter', 'SoNurbsProfile', 'getVertices', 'numvertices'),
        ('parameter', 'SoPolygonOffsetElement', 'get', 'styles'),
        ('parameter', 'SoPolygonOffsetElement', 'getDefault', 'styles'),
        ('parameter', 'SoProfile', 'getTrimCurve', 'knotvector'),
        ('parameter', 'SoProfile', 'getTrimCurve', 'numknots'),
        ('parameter', 'SoProfile', 'getTrimCurve', 'numpoints'),
        ('parameter', 'SoProfile', 'getTrimCurve', 'points'),
        ('parameter', 'SoProfile', 'getVertices', 'numvertices'),
        ('parameter', 'SoReorganizeAction', '__init__', 'simplifier'),
        ('parameter', 'SoSFEnum', 'setEnums', 'vals'),
        ('parameter', 'SoSFVec2b', 'setValue', 'xy'),
        ('parameter', 'SoSFVec2i32', 'setValue', 'xy'),
        ('parameter', 'SoSFVec2s', 'setValue', 'xy'),
        ('parameter', 'SoSFVec3b', 'setValue', 'xyz'),
        ('parameter', 'SoSFVec3i32', 'setValue', 'xyz'),
        ('parameter', 'SoSFVec3s', 'setValue', 'xyz'),
        ('parameter', 'SoSFVec4b', 'setValue', 'xyzw'),
        ('parameter', 'SoSFVec4i32', 'setValue', 'xyzw'),
        ('parameter', 'SoSFVec4s', 'setValue', 'xyzw'),
        ('parameter', 'SoSFVec4ub', 'setValue', 'xyzw'),
        ('parameter', 'SoSFVec4ui32', 'setValue', 'xyzw'),
        ('parameter', 'SoSFVec4us', 'setValue', 'xyzw'),
        ('parameter', 'SoSensor', 'setData', 'callbackdata'),
        ('parameter', 'SoSensorManager', 'doSelect', 'exceptfds'),
        ('parameter', 'SoSensorManager', 'doSelect', 'readfds'),
        ('parameter', 'SoSensorManager', 'doSelect', 'writefds'),
        ('parameter', 'SoShaderParameter1f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter1i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter2f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter2i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter3f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter3i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter4f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameter4i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray1f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray1i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray2f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray2i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray3f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray3i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray4f', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterArray4i', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterMatrix', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderParameterMatrixArray', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShaderStateMatrixParameter', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoShapeHintsElement', 'get', 'faceType'),
        ('parameter', 'SoShapeHintsElement', 'get', 'shapeType'),
        ('parameter', 'SoShapeHintsElement', 'get', 'vertexOrdering'),
        ('parameter', 'SoTextureCombineElement', 'get', 'alphaoperation'),
        ('parameter', 'SoTextureCombineElement', 'get', 'rgboperation'),
        ('parameter', 'SoUniformShaderParameter', 'updateParameter', 'shaderObject'),
        ('parameter', 'SoVRMLAudioClip', 'close', 'datasource'),
        ('parameter', 'SoVRMLAudioClip', 'read', 'datasource'),
        ('parameter', 'SoVRMLAudioClip', 'seek', 'datasource'),
        ('parameter', 'SoVRMLAudioClip', 'setSubdirectories', 'subdirectories'),
        ('parameter', 'SoVRMLAudioClip', 'tell', 'datasource'),
        ('parameter', 'SoVRMLScript', 'setScriptEvaluateCB', 'closure'),
        ('parameter', 'SoVRMLSound', 'startPlaying', 'userdataptr'),
        ('parameter', 'SoVRMLSound', 'stopPlaying', 'userdataptr'),
        ('parameter', 'SoVectorizeAction', 'getPenDescription', 'widths'),
        ('parameter', 'SoVectorizeAction', 'setPenDescription', 'widths'),
        ('parameter', 'SoVertexAttributeElement', 'add', 'attribdata'),
        ('parameter', 'SoVertexAttributeElement', 'applyToAttributes', 'closure'),
        ('parameter', 'SoVertexAttributeElement', 'applyToAttributes', 'func'),
        ('parameter', 'SoWindowElement', 'get', 'context'),
        ('parameter', 'SoWindowElement', 'get', 'display'),
        ('parameter', 'SoWindowElement', 'get', 'window'),
        ('parameter', 'SoWindowElement', 'set', 'context'),
        ('parameter', 'SoWindowElement', 'set', 'display'),
        ('parameter', 'SoWindowElement', 'set', 'window'),
        ('return', 'SbBSPTree', 'getUserData', 'return'),
        ('return', 'SbByteBuffer', 'data', 'return'),
        ('return', 'SbClip', 'getVertexData', 'return'),
        ('return', 'SbHeap', 'extractMin', 'return'),
        ('return', 'SbHeap', 'getMin', 'return'),
        ('return', 'SbStorage', 'get', 'return'),
        ('return', 'SoActionMethodList', '__getitem__', 'return'),
        ('return', 'SoActionMethodList', 'get', 'return'),
        ('return', 'SoAuditorList', 'getObject', 'return'),
        ('return', 'SoByteStream', 'getData', 'return'),
        ('return', 'SoConvexDataCache', 'getCoordIndices', 'return'),
        ('return', 'SoConvexDataCache', 'getMaterialIndices', 'return'),
        ('return', 'SoConvexDataCache', 'getNormalIndices', 'return'),
        ('return', 'SoConvexDataCache', 'getTexIndices', 'return'),
        ('return', 'SoDebugError', 'getHandlerData', 'return'),
        ('return', 'SoError', 'getHandlerData', 'return'),
        ('return', 'SoFieldContainer', 'getUserData', 'return'),
        ('return', 'SoGLVBOElement', 'getColorVBO', 'return'),
        ('return', 'SoGLVBOElement', 'getNormalVBO', 'return'),
        ('return', 'SoGLVBOElement', 'getTexCoordVBO', 'return'),
        ('return', 'SoGLVBOElement', 'getVertexVBO', 'return'),
        ('return', 'SoGlyph', 'getBitmap', 'return'),
        ('return', 'SoGlyph', 'getEdgeIndices', 'return'),
        ('return', 'SoGlyph', 'getFaceIndices', 'return'),
        ('return', 'SoGlyph', 'getNextCCWEdge', 'return'),
        ('return', 'SoGlyph', 'getNextCWEdge', 'return'),
        ('return', 'SoLazyElement', 'getColorIndices', 'return'),
        ('return', 'SoLazyElement', 'getPackedPointer', 'return'),
        ('return', 'SoLockManager', 'GetUnlockString', 'return'),
        ('return', 'SoMFBool', 'startEditing', 'return'),
        ('return', 'SoMFDouble', 'startEditing', 'return'),
        ('return', 'SoMFEnum', 'startEditing', 'return'),
        ('return', 'SoMFFloat', 'startEditing', 'return'),
        ('return', 'SoMFInt32', 'startEditing', 'return'),
        ('return', 'SoMFShort', 'startEditing', 'return'),
        ('return', 'SoMFUInt32', 'startEditing', 'return'),
        ('return', 'SoMFUShort', 'startEditing', 'return'),
        ('return', 'SoMemoryError', 'getHandlerData', 'return'),
        ('return', 'SoMultiTextureEnabledElement', 'getEnabledUnits', 'return'),
        ('return', 'SoNormalCache', 'getIndices', 'return'),
        ('return', 'SoOffscreenRenderer', 'getDC', 'return'),
        ('return', 'SoReadError', 'getHandlerData', 'return'),
        ('return', 'SoReorganizeAction', 'getSimplifier', 'return'),
        ('return', 'SoSensor', 'getData', 'return'),
        ('return', 'SoSensor', 'getFunction', 'return'),
        ('return', 'SoShininessElement', 'getArrayPtr', 'return'),
        ('return', 'SoTransparencyElement', 'getArrayPtr', 'return'),
        ('return', 'SoVRMLAudioClip', 'open', 'return'),
    }
)


def classify_incomplete(
    *,
    kind: str,
    class_name: str,
    method_name: str | None,
    parameter_name: str,
    has_raw_pointer_note: bool,
) -> str:
    """Classify one incomplete site using the shared policy rules."""

    for rule in INCOMPLETE_RULES:
        if rule.matches(
            kind=kind,
            class_name=class_name,
            method_name=method_name,
            parameter_name=parameter_name,
            has_raw_pointer_note=has_raw_pointer_note,
        ):
            return rule.category
    key = (kind, class_name, method_name, parameter_name)
    if key in TRIAGED_INCOMPLETE_SITES:
        return "dynamic/runtime API"
    return "uncategorized"
