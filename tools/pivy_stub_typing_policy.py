"""Shared, declarative policy for the generated Pivy typing surface."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from tools.pivy_factory_registry import (
        ENGINE_FACTORY_CLASS_NAMES,
        ENGINE_FACTORY_CLASSES,
        SCXML_FACTORY_CLASSES,
        SCXML_FACTORY_CLASS_NAMES,
    )
except ImportError:
    from pivy_factory_registry import (
        ENGINE_FACTORY_CLASS_NAMES,
        ENGINE_FACTORY_CLASSES,
        SCXML_FACTORY_CLASSES,
        SCXML_FACTORY_CLASS_NAMES,
    )


@dataclass(frozen=True)
class VectorTypePolicy:
    """Python-facing policy for one fixed-width Coin vector value."""

    scalar_cpp_type: str
    component_type: str
    width: int


@dataclass(frozen=True)
class PythonMethodPolicy:
    """Python-facing signature for a binding-added or normalized method."""

    parameters: str
    return_type: str


VECTOR_TYPE_POLICIES = {
    "SbVec2b": VectorTypePolicy("int8_t", "int", 2),
    "SbVec2s": VectorTypePolicy("short", "int", 2),
    "SbVec2i32": VectorTypePolicy("int32_t", "int", 2),
    "SbVec2f": VectorTypePolicy("float", "float", 2),
    "SbVec2d": VectorTypePolicy("double", "float", 2),
    "SbVec3b": VectorTypePolicy("int8_t", "int", 3),
    "SbVec3s": VectorTypePolicy("short", "int", 3),
    "SbVec3i32": VectorTypePolicy("int32_t", "int", 3),
    "SbVec3f": VectorTypePolicy("float", "float", 3),
    "SbVec3d": VectorTypePolicy("double", "float", 3),
    "SbVec4b": VectorTypePolicy("int8_t", "int", 4),
    "SbVec4ub": VectorTypePolicy("uint8_t", "int", 4),
    "SbVec4s": VectorTypePolicy("short", "int", 4),
    "SbVec4us": VectorTypePolicy("unsigned short", "int", 4),
    "SbVec4i32": VectorTypePolicy("int32_t", "int", 4),
    "SbVec4ui32": VectorTypePolicy("uint32_t", "int", 4),
    "SbVec4f": VectorTypePolicy("float", "float", 4),
    "SbVec4d": VectorTypePolicy("double", "float", 4),
}


def vector_sequence_array_parameters():
    """Return constructor/setter sequence policies for Coin vectors."""

    return {
        (class_name, method_name, "v"): (
            "Sequence[%s]" % policy.component_type,
            str(policy.width),
        )
        for class_name, policy in VECTOR_TYPE_POLICIES.items()
        for method_name in ("__init__", "setValue")
    }


def vector_value_return_types():
    """Return zero-argument getValue annotations for Coin vectors."""

    return {
        class_name: "Sequence[%s]" % policy.component_type
        for class_name, policy in VECTOR_TYPE_POLICIES.items()
    }


def vector_iter_element_types():
    """Return iterator component annotations for Coin vectors."""

    return {
        class_name: policy.component_type
        for class_name, policy in VECTOR_TYPE_POLICIES.items()
    }


def vector_output_parameter_types():
    """Return scalar pointer-helper parameters for vector output overloads."""

    pointer_types = {
        "float": "floatp",
        "double": "doublep",
    }
    return {
        class_name: tuple(
            "%s: %s" % (
                component,
                pointer_types.get(policy.scalar_cpp_type, "intp"),
            )
            for component in "xyzw"[: policy.width]
        )
        for class_name, policy in VECTOR_TYPE_POLICIES.items()
    }


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
    "uintp": "int",
    "longp": "int",
    "floatp": "float",
    "doublep": "float",
}
SCALAR_POINTER_HELPER_PARAMETERS = {
    ("SoQt", "getVersionInfo", "major"): "intp",
    ("SoQt", "getVersionInfo", "minor"): "intp",
    ("SoQt", "getVersionInfo", "micro"): "intp",
}
SCALAR_REFERENCE_HELPER_PARAMETERS = {
    ("SoDepthBufferElement", "get", "function_out"): "intp",
    ("SoOutput", "getAvailableCompressionMethods", "num"): "uintp",
}
SCALAR_REFERENCE_HELPER_TYPES = {
    "SbBool": "intp",
    "char": "charp",
    "double": "doublep",
    "float": "floatp",
    "int": "intp",
    "int32_t": "intp",
    "long": "longp",
}
SEQUENCE_POINTER_PARAMETERS = {
    ("SbColor", "__init__", "rgb"): "Sequence[float]",
    ("SbColor4f", "__init__", "rgba"): "Sequence[float]",
    ("SoGLColorIndexElement", "set", "indices"): "Sequence[int]",
    ("SoGLLazyElement", "setColorIndexElt", "indices"): "Sequence[int]",
    ("SoLazyElement", "setColorIndices", "indices"): "Sequence[int]",
    ("SoMFEnum", "setEnums", "values"): "Sequence[int]",
    ("SoMFEnum", "setEnums", "names"): "SbName | Sequence[SbName | str]",
    ("SoShininessElement", "set", "values"): "Sequence[float]",
    ("SoTransparencyElement", "set", "values"): "Sequence[float]",
    ("SoQt", "init", "argv"): "Sequence[str]",
}
SEQUENCE_ARRAY_PARAMETERS = {
    **vector_sequence_array_parameters(),
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
    **vector_value_return_types(),
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
PYTHON_HELPER_METHOD_POLICIES = {
    ("_SwigNonDynamicMeta", "__setattr__"): PythonMethodPolicy(
        "cls, name: str, value: Any",
        "None",
    ),
    ("SoBase", "__nonzero__"): PythonMethodPolicy("self", "bool"),
    ("SoBaseKit", "__getattr__"): PythonMethodPolicy(
        "self, name: str", "SoNode | SoField"
    ),
    ("SoBaseKit", "__setattr__"): PythonMethodPolicy(
        "self, name: str, value: Any", "None"
    ),
    ("SoEngine", "__getattr__"): PythonMethodPolicy(
        "self, name: str",
        "SoField | SoEngineOutput",
    ),
    ("SoEngine", "getOutput"): PythonMethodPolicy(
        "self, outputname: SbName | str",
        "SoEngineOutput | None",
    ),
    ("SoEngine", "getOutputNameValue"): PythonMethodPolicy(
        "self, output: SoEngineOutput",
        "tuple[bool, str]",
    ),
    ("SoCallbackAction", "getTextureImage2dValue"): PythonMethodPolicy(
        "self",
        "tuple[bytes | None, SbVec2s, int]",
    ),
    ("SoCallbackAction", "getTextureImage3dValue"): PythonMethodPolicy(
        "self",
        "tuple[bytes | None, SbVec3s, int]",
    ),
    ("SoSFImage", "getSubTextureValue"): PythonMethodPolicy(
        "self, idx: int",
        "tuple[bytes | None, SbVec2s, SbVec2s, int]",
    ),
    ("SoGlyph", "getBitmapValue"): PythonMethodPolicy(
        "self, antialiased: bool",
        "tuple[bytes | None, SbVec2s, SbVec2s]",
    ),
    ("SoEngine", "__setattr__"): PythonMethodPolicy(
        "self, name: str, value: Any", "None"
    ),
    ("SoFieldContainer", "__dir__"): PythonMethodPolicy("self", "list[str]"),
    ("SoFieldContainer", "__getattr__"): PythonMethodPolicy(
        "self, name: str", "SoField"
    ),
    ("SoFieldContainer", "__setattr__"): PythonMethodPolicy(
        "self, name: str, value: Any",
        "None",
    ),
    ("SoGroup", "__iadd__"): PythonMethodPolicy(
        "self, other: SoNode | Sequence[SoNode]", "SoGroup"
    ),
    ("SoGroup", "__isub__"): PythonMethodPolicy(
        "self, other: SoNode | Sequence[SoNode]", "SoGroup"
    ),
    ("SoGroup", "__contains__"): PythonMethodPolicy(
        "self, node: SoNode", "bool"
    ),
    ("SoGroup", "getByName"): PythonMethodPolicy(
        "self, name: SbName | str", "SoNode | None"
    ),
    ("SoNodeKitPath", "index"): PythonMethodPolicy("self", "Iterator[int]"),
    ("SoPath", "index"): PythonMethodPolicy("self", "Iterator[int]"),
    ("SoType", "fromName"): PythonMethodPolicy(
        "name: SbName | str", "SoType"
    ),
}
METHOD_RETURN_TYPE_OVERRIDES = {
    # The Python-level SbImage adapter snapshots the native pixel buffer, so
    # callers never receive a borrowed C pointer.  ``None`` represents an
    # image with no allocated pixel data.
    ("SbImage", "getValue"): "tuple[bytes | None, SbVec2s | SbVec3s, int]",
    # SoOffscreenRenderer's SWIG extension copies the borrowed render buffer
    # into a Python bytes object before returning it.
    ("SoOffscreenRenderer", "getBuffer"): "bytes",
    # SoColorPacker's SWIG extension snapshots the owned internal color array
    # using getSize(), so callers never receive a borrowed C pointer.
    ("SoColorPacker", "getPackedColors"): "bytes",
    # SoByteStream's SWIG extension snapshots its internal buffer using the
    # exact byte count returned by getNumBytes().
    ("SoByteStream", "getData"): "bytes",
    # SWIG's image typemaps expose the native pixel pointer together with the
    # dimensions and component count as a Python tuple.
    ("SoSFImage", "getValue"): "tuple[bytes, SbVec2s, int]",
    ("SoSFImage", "startEditing"): "tuple[bytes, SbVec2s, int]",
    ("SoSFImage3", "getValue"): "tuple[bytes, SbVec3s, int]",
    ("SoSFImage3", "startEditing"): "tuple[bytes, SbVec3s, int]",
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
PYTHON_PARAMETER_TYPE_OVERRIDES = {
    ("SoSFImage", "setValue", "pixels"): "str | bytes",
    ("SoSFImage3", "setValue", "bytes"): "str | bytes",
    ("SoSFImage3", "setValue", "pixels"): "str | bytes",
    ("SoSFEnum", "setEnums", "vals"): "Sequence[int]",
    ("SoSFEnum", "setEnums", "names"): "SbName | Sequence[SbName | str]",
    ("SoQtRenderArea", "setEventCallback", "user"): "object",
}

# Coin's element, engine, and field header macros expose these class-specific
# factories as ``void *``. The binding typemaps autocast and own the concrete
# object, so the generated Python contract can name the class returned by each
# factory.
ELEMENT_FACTORY_CLASSES = frozenset(
    {
        "SoDecimationTypeElement",
        "SoComplexityTypeElement",
        "SoDrawStyleElement",
        "SoLazyElement",
        "SoMaterialBindingElement",
        "SoNormalBindingElement",
        "SoPickStyleElement",
        "SoShapeHintsElement",
        "SoMultiTextureImageElement",
        "SoTextureCoordinateBindingElement",
        "SoMultiTextureCoordinateElement",
        "SoNormalElement",
        "SoGLNormalElement",
        "SoGLMultiTextureCoordinateElement",
        "SoGLLazyElement",
        "SoAmbientColorElement",
        "SoAnnoText3CharOrientElement",
        "SoAnnoText3FontSizeHintElement",
        "SoAnnoText3RenderPrintElement",
        "SoModelMatrixElement",
        "SoBBoxModelMatrixElement",
        "SoBumpMapCoordinateElement",
        "SoBumpMapElement",
        "SoBumpMapMatrixElement",
        "SoCacheElement",
        "SoClipPlaneElement",
        "SoComplexityElement",
        "SoCoordinateElement",
        "SoCreaseAngleElement",
        "SoCullElement",
        "SoDecimationPercentageElement",
        "SoDiffuseColorElement",
        "SoGLClipPlaneElement",
        "SoLightElement",
        "SoGLModelMatrixElement",
        "SoProfileElement",
        "SoMultiTextureMatrixElement",
        "SoGLMultiTextureMatrixElement",
        "SoGLDrawStyleElement",
        "SoGLLightIdElement",
        "SoMultiTextureEnabledElement",
        "SoGLMultiTextureEnabledElement",
        "SoLinePatternElement",
        "SoGLLinePatternElement",
        "SoSwitchElement",
        "SoTextOutlineEnabledElement",
        "SoUnitsElement",
        "SoFocalDistanceElement",
        "SoFontSizeElement",
        "SoLineWidthElement",
        "SoGLLineWidthElement",
        "SoPointSizeElement",
        "SoGLPointSizeElement",
        "SoTextureQualityElement",
        "SoTextureOverrideElement",
        "SoGLRenderPassElement",
        "SoGLUpdateAreaElement",
        "SoLocalBBoxMatrixElement",
        "SoOverrideElement",
        "SoPickRayElement",
        "SoGLCoordinateElement",
        "SoEnvironmentElement",
        "SoGLEnvironmentElement",
        "SoFontNameElement",
        "SoLightAttenuationElement",
        "SoPolygonOffsetElement",
        "SoGLPolygonOffsetElement",
        "SoProjectionMatrixElement",
        "SoGLProjectionMatrixElement",
        "SoProfileCoordinateElement",
        "SoGLMultiTextureImageElement",
        "SoViewingMatrixElement",
        "SoGLViewingMatrixElement",
        "SoViewVolumeElement",
        "SoGLShapeHintsElement",
        "SoShapeStyleElement",
        "SoViewportRegionElement",
        "SoGLViewportRegionElement",
        "SoWindowElement",
        "SoGLCacheContextElement",
        "SoGLColorIndexElement",
        "SoListenerPositionElement",
        "SoListenerOrientationElement",
        "SoListenerDopplerElement",
        "SoListenerGainElement",
        "SoSoundElement",
        "SoGLVBOElement",
        "SoDepthBufferElement",
        "SoGLDepthBufferElement",
        "SoVertexAttributeElement",
        "SoGLVertexAttributeElement",
        "SoVertexAttributeBindingElement",
        "SoSpecularColorElement",
        "SoEmissiveColorElement",
        "SoShininessElement",
        "SoTransparencyElement",
        "SoLightModelElement",
        "SoTextureCombineElement",
        "SoTextureUnitElement",
        "SoCacheHintElement",
    }
)

FIELD_FACTORY_CLASSES = frozenset(
    {
        "SoSFEnum",
        "SoSFFloat",
        "SoSFUShort",
        "SoSFInt32",
        "SoSFBool",
        "SoSFImage",
        "SoSFString",
        "SoSFColor",
        "SoSFNode",
        "SoSFName",
        "SoMFName",
        "SoSFVec3f",
        "SoSFRotation",
        "SoSFVec2f",
        "SoMFBool",
        "SoMFEnum",
        "SoMFFloat",
        "SoMFVec3f",
        "SoMFString",
        "SoMFVec2f",
        "SoMFVec4f",
        "SoMFRotation",
        "SoMFMatrix",
        "SoSFPath",
        "SoSFTrigger",
        "SoSFShort",
        "SoSFTime",
        "SoSFBitMask",
        "SoSFBox2s",
        "SoSFBox2i32",
        "SoSFBox2f",
        "SoSFBox2d",
        "SoSFBox3s",
        "SoSFBox3i32",
        "SoSFBox3f",
        "SoSFBox3d",
        "SoSFColorRGBA",
        "SoSFDouble",
        "SoSFEngine",
        "SoSFImage3",
        "SoSFMatrix",
        "SoSFPlane",
        "SoSFUInt32",
        "SoSFVec2b",
        "SoSFVec2s",
        "SoSFVec2i32",
        "SoSFVec2d",
        "SoSFVec3b",
        "SoSFVec3s",
        "SoSFVec3i32",
        "SoSFVec3d",
        "SoSFVec4b",
        "SoSFVec4ub",
        "SoSFVec4s",
        "SoSFVec4us",
        "SoSFVec4i32",
        "SoSFVec4ui32",
        "SoSFVec4f",
        "SoSFVec4d",
        "SoMFColor",
        "SoMFColorRGBA",
        "SoMFDouble",
        "SoMFEngine",
        "SoMFBitMask",
        "SoMFInt32",
        "SoMFNode",
        "SoMFPath",
        "SoMFPlane",
        "SoMFShort",
        "SoMFTime",
        "SoMFUInt32",
        "SoMFUShort",
        "SoMFVec2b",
        "SoMFVec2s",
        "SoMFVec2i32",
        "SoMFVec2d",
        "SoMFVec3b",
        "SoMFVec3s",
        "SoMFVec3i32",
        "SoMFVec3d",
        "SoMFVec4b",
        "SoMFVec4ub",
        "SoMFVec4s",
        "SoMFVec4us",
        "SoMFVec4i32",
        "SoMFVec4ui32",
        "SoMFVec4d",
    }
)

FACTORY_CLASSES = (
    ELEMENT_FACTORY_CLASSES
    | ENGINE_FACTORY_CLASSES
    | FIELD_FACTORY_CLASSES
    | SCXML_FACTORY_CLASSES
)


def factory_method_return_type(class_name, method_name):
    if method_name == "createInstance" and class_name in FACTORY_CLASSES:
        return class_name
    return None
EXTEND_HELPER_METHOD_TYPES = {
    ("SoOffscreenRenderer", "getBuffer", "self"): ("self", "bytes"),
    ("SoColorPacker", "getPackedColors", "self"): ("self", "bytes"),
    ("SoSensor", "getFunction", "self"): (
        "self",
        "SoSensorCallback[SoSensor] | None",
    ),
    ("SoSensor", "getData", "self"): ("self", "object | None"),
    ("SoError", "getHandlerCallback", ""): (
        "",
        "SoErrorCallback | None",
    ),
    ("SoError", "getHandlerData", ""): ("", "object | None"),
    ("SoDebugError", "getHandlerCallback", ""): (
        "",
        "SoErrorCallback | None",
    ),
    ("SoDebugError", "getHandlerData", ""): ("", "object | None"),
    ("SoMemoryError", "getHandlerCallback", ""): (
        "",
        "SoErrorCallback | None",
    ),
    ("SoMemoryError", "getHandlerData", ""): ("", "object | None"),
    ("SoReadError", "getHandlerCallback", ""): (
        "",
        "SoErrorCallback | None",
    ),
    ("SoReadError", "getHandlerData", ""): ("", "object | None"),
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
PYTHON_PROTOCOL_DEFINITIONS = (
    (
        "SoSensorCallback",
        ("SoSensor",),
        "_SensorT = TypeVar(\"_SensorT\", bound=SoSensor, contravariant=True)\n"
        "\n"
        "class SoSensorCallback(Protocol[_SensorT]):\n"
        "    def __call__(\n"
        "        self, data: object, sensor: _SensorT, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoErrorCallback",
        ("SoError",),
        "class SoErrorCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, error: SoError, /\n"
        "    ) -> None: ...",
    ),
    (
        "ScXMLStateMachineDeleteCallback",
        ("ScXMLStateMachine",),
        "class ScXMLStateMachineDeleteCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: Any, machine: ScXMLStateMachine, /\n"
        "    ) -> None: ...",
    ),
    (
        "ScXMLStateChangeCallback",
        ("ScXMLStateMachine",),
        "class ScXMLStateChangeCallback(Protocol):\n"
        "    def __call__(\n"
        "        self,\n"
        "        data: Any,\n"
        "        machine: ScXMLStateMachine,\n"
        "        stateidentifier: str,\n"
        "        enterstate: bool,\n"
        "        success: bool,\n"
        "        /,\n"
        "    ) -> None: ...",
    ),
    (
        "SoQtComponentCallback",
        ("SoQtComponent",),
        "class SoQtComponentCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, user: object, component: SoQtComponent, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoQtViewerCallback",
        ("SoQtViewer",),
        "class SoQtViewerCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, viewer: SoQtViewer, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoFieldContainerAccess",
        ("SoField", "SoFieldContainer"),
        "class SoFieldContainerAccess(Protocol):\n"
        "    def __getattr__(self, name: str) -> SoField: ...\n"
        "    def __dir__(self) -> list[str]: ...",
    ),
    (
        "SoEngineAccess",
        ("SoEngine", "SoEngineOutput", "SoField"),
        "class SoEngineAccess(Protocol):\n"
        "    def __getattr__(\n"
        "        self, name: str\n"
        "    ) -> SoField | SoEngineOutput: ...\n"
        "    def getOutput(\n"
        "        self, outputname: SbName | str\n"
        "    ) -> SoEngineOutput | None: ...",
    ),
    (
        "SoNodeKitAccess",
        ("SoBaseKit", "SoField", "SoNode"),
        "class SoNodeKitAccess(Protocol):\n"
        "    def __getattr__(self, name: str) -> SoNode | SoField: ...",
    ),
)
CALLBACK_TYPE_SIGNATURES = {
    "ScXMLStateChangeCB": "ScXMLStateChangeCallback",
    "ScXMLStateMachineDeleteCB": "ScXMLStateMachineDeleteCallback",
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
    "SoSensorCB": "SoSensorCallback[SoSensor]",
    "SoErrorCB": "SoErrorCallback",
    "SoQtRenderAreaEventCB": "Callable[[object, QEvent], object]",
    "SoQtFatalErrorCB": "Callable[[SbString, int, object], None]",
    "SoQtComponentCB": "SoQtComponentCallback",
    "SoQtViewerCB": "SoQtViewerCallback",
    "SoQtAutoClippingCB": "Callable[[object, SbVec2f], SbVec2f]",
    "SoQtMenuSelectionCallback": "Callable[[int, object], None]",
}


@dataclass(frozen=True)
class NativeCallbackBoundary:
    """Document a native callback that has no Python adapter yet."""

    native_signature: str
    python_surface: str = "native-only; keep Incomplete until adapted"


NATIVE_CALLBACK_BOUNDARY_METHODS = {
    ("SoDB", "getHeaderData"): NativeCallbackBoundary(
        "SoHeaderCB * precallback, SoHeaderCB * postcallback"
    ),
    ("SoCallbackAction", "getTextureImage"): NativeCallbackBoundary(
        "const unsigned char * return buffer"
    ),
    ("SoGLRenderAction", "getAbortCallback"): NativeCallbackBoundary(
        "SoGLRenderAbortCB ** callback and void ** userdata"
    ),
    ("SoGLImage", "setResizeCallback"): NativeCallbackBoundary(
        "SoGLImageResizeCB * callback, void * closure"
    ),
    ("SoWWWAnchor", "setFetchURLCallBack"): NativeCallbackBoundary(
        "SoWWWAnchorCB * callback, void * userdata"
    ),
    ("SoWWWAnchor", "setHighlightURLCallBack"): NativeCallbackBoundary(
        "SoWWWAnchorCB * callback, void * userdata"
    ),
    ("SoWWWInline", "setFetchURLCallBack"): NativeCallbackBoundary(
        "SoWWWInlineCB * callback, void * userdata"
    ),
    ("SbClip", "__init__"): NativeCallbackBoundary(
        "SbClipCB * callback, void * userdata"
    ),
    ("SbHeap", "buildHeap"): NativeCallbackBoundary(
        "SbBool (*)(float percentage, void * data)"
    ),
    ("SbTesselator", "setCallback"): NativeCallbackBoundary(
        "SbTesselatorCB * callback, void * userdata"
    ),
    ("SoVRMLAnchor", "setFetchURLCallBack"): NativeCallbackBoundary(
        "SoVRMLAnchorCB * callback, void * closure"
    ),
    ("SoVRMLAudioClip", "setCallbacks"): NativeCallbackBoundary(
        "open_func/read_func/seek_func/tell_func/close_func"
    ),
    ("SoVRMLImageTexture", "setPrequalifyFileCallBack"): NativeCallbackBoundary(
        "SoVRMLImageTextureCB * callback, void * closure"
    ),
    ("SoVRMLInline", "setFetchURLCallBack"): NativeCallbackBoundary(
        "SoVRMLInlineCB * callback, void * closure"
    ),
    ("SoVRMLScript", "setScriptEvaluateCB"): NativeCallbackBoundary(
        "SoVRMLScriptEvaluateCB * callback, void * closure"
    ),
}

NATIVE_FUNCTION_POINTER_BOUNDARY_METHODS = {
    ("SbDict", "applyToAll"): "void (*)(void *, void *)",
    ("SbDict", "setHashingFunction"): "uint32_t (*)(const void *)",
    ("SbString", "apply"): "void (*)(char *)",
    ("SoActionMethodList", "addMethod"): "SoActionMethod *",
    ("SoOutput", "setBuffer"): "void * (*reallocFunc)(void *, size_t)",
    ("SbStorage", "applyToAll"): "void (*)(void *, void *)",
}
NATIVE_FUNCTION_POINTER_BOUNDARY_CLASSES = frozenset(
    {"SbHeapFuncs", "SbOctTreeFuncs"}
)
NATIVE_FUNCTION_POINTER_ACTION_CLASSES = frozenset(
    {
        "SoAudioRenderAction",
        "SoBoxHighlightRenderAction",
        "SoCallbackAction",
        "SoGetBoundingBoxAction",
        "SoGetMatrixAction",
        "SoGetPrimitiveCountAction",
        "SoHandleEventAction",
        "SoIntersectionDetectionAction",
        "SoLineHighlightRenderAction",
        "SoPickAction",
        "SoRayPickAction",
        "SoReorganizeAction",
        "SoSearchAction",
        "SoSimplifyAction",
        "SoGLRenderAction",
        "SoToVRML2Action",
        "SoToVRMLAction",
        "SoVectorizeAction",
        "SoVectorizePSAction",
        "SoWriteAction",
    }
)


def native_callback_boundary(
    *, kind: str, class_name: str, method_name: str | None
) -> NativeCallbackBoundary | None:
    """Return the reviewed native callback boundary for one stub site."""

    if (class_name, method_name) in NATIVE_CALLBACK_BOUNDARY_METHODS:
        return NATIVE_CALLBACK_BOUNDARY_METHODS[(class_name, method_name)]
    if (
        method_name == "addMethod"
        and class_name in NATIVE_FUNCTION_POINTER_ACTION_CLASSES
    ):
        return NativeCallbackBoundary("SoActionMethod * method")
    if (class_name, method_name) in NATIVE_FUNCTION_POINTER_BOUNDARY_METHODS:
        return NativeCallbackBoundary(
            NATIVE_FUNCTION_POINTER_BOUNDARY_METHODS[(class_name, method_name)]
        )
    if class_name in NATIVE_FUNCTION_POINTER_BOUNDARY_CLASSES:
        return NativeCallbackBoundary("function-pointer member")
    return None
@dataclass(frozen=True)
class CallbackMethodPolicy:
    """Python contract for one callback-bearing Coin method."""

    parameter_types: tuple[tuple[str, str], ...]
    shadow_signature: tuple[str, str] | None = None
    validation_parameter_types: tuple[tuple[str, str], ...] | None = None

    def parameters(self) -> dict[str, str]:
        return dict(
            self.validation_parameter_types
            if self.validation_parameter_types is not None
            else self.parameter_types
        )


CALLBACK_METHOD_POLICIES = {
    ("SoQt", "setFatalErrorHandler"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[SbString, int, object], None]"),
            ("userdata", "object"),
        ),
        (
            "cb: Callable[[SbString, int, object], None], "
            "userdata: object",
            "Callable[[SbString, int, object], None] | None",
        ),
    ),
    ("SoQtComponent", "setWindowCloseCallback"): CallbackMethodPolicy(
        (
            ("func", "SoQtComponentCallback"),
            ("user", "object | None"),
        ),
        (
            "self, func: SoQtComponentCallback, user: object | None = ...",
            "None",
        ),
    ),
    ("SoQtViewer", "setAutoClippingStrategy"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, SbVec2f], SbVec2f] | None"),
            ("cbuserdata", "object | None"),
        ),
        (
            "self, strategy: int, value: float = ..., "
            "cb: Callable[[object, SbVec2f], SbVec2f] | None = ..., "
            "cbuserdata: object | None = ...",
            "None",
        ),
    ),
    ("SoQtPopupMenu", "addMenuSelectionCallback"): CallbackMethodPolicy(
        (
            ("callback", "Callable[[int, object], None]"),
            ("data", "object"),
        ),
        (
            "self, callback: Callable[[int, object], None], data: object",
            "None",
        ),
    ),
    ("SoQtPopupMenu", "removeMenuSelectionCallback"): CallbackMethodPolicy(
        (
            ("callback", "Callable[[int, object], None]"),
            ("data", "object"),
        ),
        (
            "self, callback: Callable[[int, object], None], data: object",
            "None",
        ),
    ),
    ("SoError", "setHandlerCallback"): CallbackMethodPolicy(
        (
            ("pyfunc", "SoErrorCallback"),
            ("data", "object"),
        ),
        (
            "pyfunc: SoErrorCallback, data: object",
            "None",
        ),
    ),
    ("SoDebugError", "setHandlerCallback"): CallbackMethodPolicy(
        (
            ("pyfunc", "SoErrorCallback"),
            ("data", "object"),
        ),
        (
            "pyfunc: SoErrorCallback, data: object",
            "None",
        ),
    ),
    ("SoMemoryError", "setHandlerCallback"): CallbackMethodPolicy(
        (
            ("pyfunc", "SoErrorCallback"),
            ("data", "object"),
        ),
        (
            "pyfunc: SoErrorCallback, data: object",
            "None",
        ),
    ),
    ("SoReadError", "setHandlerCallback"): CallbackMethodPolicy(
        (
            ("pyfunc", "SoErrorCallback"),
            ("data", "object"),
        ),
        (
            "pyfunc: SoErrorCallback, data: object",
            "None",
        ),
    ),
    ("SoCallbackList", "addCallback"): CallbackMethodPolicy(
        (
            ("f", "Callable[[object, object], None]"),
            ("userData", "object | None"),
        ),
        (
            "self, f: Callable[[object, object], None], "
            "userData: object | None = ...",
            "None",
        ),
    ),
    ("SoCallbackList", "removeCallback"): CallbackMethodPolicy(
        (
            ("f", "Callable[[object, object], None]"),
            ("userdata", "object | None"),
        ),
        (
            "self, f: Callable[[object, object], None], "
            "userdata: object | None = ...",
            "None",
        ),
    ),
    ("SoCallbackList", "clearCallbacks"): CallbackMethodPolicy(
        (), ("self", "None")
    ),
    ("SoCallbackList", "invokeCallbacks"): CallbackMethodPolicy(
        (("callbackdata", "object"),),
        ("self, callbackdata: object", "None"),
    ),
    ("SoContextHandler", "addContextDestructionCallback"): CallbackMethodPolicy(
        (
            ("func", "Callable[[object, int], None]"),
            ("userdata", "object | None"),
        ),
        (
            "func: Callable[[object, int], None], userdata: object | None = ...",
            "None",
        ),
    ),
    ("SoContextHandler", "removeContextDestructionCallback"): CallbackMethodPolicy(
        (
            ("func", "Callable[[object, int], None]"),
            ("userdata", "object | None"),
        ),
        (
            "func: Callable[[object, int], None], userdata: object | None = ...",
            "None",
        ),
    ),
    ("SoGLRenderAction", "setSortedObjectOrderStrategy"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, SoGLRenderAction], float] | None"),
            ("closure", "object | None"),
        ),
        (
            "self, strategy: int, "
            "cb: Callable[[object, SoGLRenderAction], float] | None = ..., "
            "closure: object | None = ...",
            "None",
        ),
        (
            ("strategy", "int"),
            ("cb", "Callable[[object, SoGLRenderAction], float] | None"),
            ("closure", "object | None"),
        ),
    ),
    ("SoGLCacheContextElement", "scheduleDeleteCallback"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, int], None]"),
            ("closure", "object | None"),
        ),
        (
            "contextid: int, "
            "cb: Callable[[object, int], None], "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SoGLImage", "setEndFrameCallback"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object], None] | None"),
            ("closure", "object | None"),
        ),
        (
            "self, cb: Callable[[object], None] | None, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SoShaderProgram", "setEnableCallback"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, SoState, bool], None] | None"),
            ("closure", "object | None"),
        ),
        (
            "self, cb: Callable[[object, SoState, bool], None] | None, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SoProto", "setFetchExternProtoCallback"): CallbackMethodPolicy(
        (
            (
                "cb",
                "Callable[[object, SoInput, list[SbString], int], "
                "SoProto | None] | None",
            ),
            ("closure", "object | None"),
        ),
        (
            "cb: Callable[[object, SoInput, list[SbString], int], "
            "SoProto | None] | None, closure: object | None = ...",
            "None",
        ),
    ),
    ("SbImage", "addReadImageCB"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, SbString, SbImage], bool]"),
            ("closure", "object | None"),
        ),
        (
            "cb: Callable[[object, SbString, SbImage], bool], "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SbImage", "removeReadImageCB"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, SbString, SbImage], bool]"),
            ("closure", "object | None"),
        ),
        (
            "cb: Callable[[object, SbString, SbImage], bool], "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SbImage", "scheduleReadFile"): CallbackMethodPolicy(
        (
            ("cb", "Callable[[object, SbString, SbImage], bool]"),
            ("closure", "object | None"),
        ),
        (
            "self, cb: Callable[[object, SbString, SbImage], bool], "
            "closure: object | None, filename: SbString, "
            "searchdirectories: SbString | None = ..., "
            "numdirectories: int = ...",
            "bool",
        ),
        (
            ("cb", "Callable[[object, SbString, SbImage], bool]"),
            ("closure", "object | None"),
            ("filename", "SbString"),
            ("searchdirectories", "SbString | None"),
            ("numdirectories", "int"),
        ),
    ),
    ("SoDB", "registerHeader"): CallbackMethodPolicy(
        (
            ("precallback", "Callable[[object, SoInput], None]"),
            ("postcallback", "Callable[[object, SoInput], None]"),
            ("userdata", "object | None"),
        ),
        (
            "headerstring: SbString, isbinary: bool, ivversion: float, "
            "precallback: Callable[[object, SoInput], None], "
            "postcallback: Callable[[object, SoInput], None], "
            "userdata: object | None = ...",
            "bool",
        ),
    ),
    ("SoDB", "addProgressCallback"): CallbackMethodPolicy(
        (
            ("func", "Callable[[object, SbName, float, bool], bool]"),
            ("userdata", "object | None"),
        ),
        (
            "func: Callable[[object, SbName, float, bool], bool], "
            "userdata: object | None",
            "None",
        ),
    ),
    ("SoDB", "removeProgressCallback"): CallbackMethodPolicy(
        (
            ("func", "Callable[[object, SbName, float, bool], bool]"),
            ("userdata", "object | None"),
        ),
        (
            "func: Callable[[object, SbName, float, bool], bool], "
            "userdata: object | None",
            "None",
        ),
    ),
    ("SoSensor", "setFunction"): CallbackMethodPolicy(
        (("callbackfunction", "SoSensorCallback[SoSensor]"),),
        (
            "self, callbackfunction: SoSensorCallback[SoSensor]",
            "None",
        ),
    ),
    ("SoDataSensor", "setDeleteCallback"): CallbackMethodPolicy(
        (
            ("function", "SoSensorCallback[SoSensor]"),
            ("data", "object | None"),
        ),
        (
            "self, function: SoSensorCallback[SoSensor], "
            "data: object | None = ...",
            "None",
        ),
    ),
}

for _dragger_callback_name in (
    "Start",
    "Motion",
    "Finish",
    "ValueChanged",
    "OtherEvent",
):
    for _dragger_callback_action in ("add", "remove"):
        CALLBACK_METHOD_POLICIES[
            (
                "SoDragger",
                "%s%sCallback" % (
                    _dragger_callback_action,
                    _dragger_callback_name,
                ),
            )
        ] = CallbackMethodPolicy(
            (
                ("pyfunc", "Callable[[object, SoDragger], None]"),
                ("data", "object | None"),
            ),
            (
                "self, pyfunc: Callable[[object, SoDragger], None], "
                "data: object | None = ...",
                "None",
            ),
        )

for _selection_callback_name in (
    "addSelectionCallback",
    "removeSelectionCallback",
    "addDeselectionCallback",
    "removeDeselectionCallback",
):
    CALLBACK_METHOD_POLICIES[("SoSelection", _selection_callback_name)] = (
        CallbackMethodPolicy(
            (
                ("pyfunc", "Callable[[object, SoPath], None]"),
                ("userdata", "object | None"),
            ),
            (
                "self, pyfunc: Callable[[object, SoPath], None], "
                "userdata: object | None = ...",
                "None",
            ),
        )
    )

for _selection_callback_name in (
    "addStartCallback",
    "removeStartCallback",
    "addFinishCallback",
    "removeFinishCallback",
    "addChangeCallback",
    "removeChangeCallback",
):
    CALLBACK_METHOD_POLICIES[("SoSelection", _selection_callback_name)] = (
        CallbackMethodPolicy(
            (
                ("pyfunc", "Callable[[object, SoSelection], None]"),
                ("userdata", "object | None"),
            ),
            (
                "self, pyfunc: Callable[[object, SoSelection], None], "
                "userdata: object | None = ...",
                "None",
            ),
        )
    )

CALLBACK_METHOD_POLICIES[("SoSelection", "setPickFilterCallback")] = (
    CallbackMethodPolicy(
        (
            ("pyfunc", "Callable[[object, SoPickedPoint], SoPath]"),
            ("userdata", "object | None"),
        ),
        (
            "self, pyfunc: Callable[[object, SoPickedPoint], SoPath], "
            "userdata: object | None = ..., callOnlyIfSelectable: int = ...",
            "None",
        ),
        (
            ("pyfunc", "Callable[[object, SoPickedPoint], SoPath]"),
            ("userdata", "object | None"),
            ("callOnlyIfSelectable", "int"),
        ),
    )
)

CALLBACK_METHOD_POLICIES.update(
    {
        ("SoExtSelection", "setLassoFilterCallback"): CallbackMethodPolicy(
            (
                (
                    "f",
                    "Callable[[object, SoPath], SoPath | None] | None",
                ),
                ("userdata", "object | None"),
                ("callonlyifselectable", "bool"),
            ),
            (
                "self, f: Callable[[object, SoPath], SoPath | None] | None, "
                "userdata: object | None = ..., "
                "callonlyifselectable: bool = ...",
                "None",
            ),
        ),
        (
            "SoExtSelection",
            "setTriangleFilterCallback",
        ): CallbackMethodPolicy(
            (
                (
                    "func",
                    "Callable[[object, SoCallbackAction, SoPrimitiveVertex, "
                    "SoPrimitiveVertex, SoPrimitiveVertex], bool] | None",
                ),
                ("userdata", "object | None"),
            ),
            (
                "self, func: Callable[[object, SoCallbackAction, "
                "SoPrimitiveVertex, SoPrimitiveVertex, SoPrimitiveVertex], "
                "bool] | None, userdata: object | None = ...",
                "None",
            ),
        ),
        (
            "SoExtSelection",
            "setLineSegmentFilterCallback",
        ): CallbackMethodPolicy(
            (
                (
                    "func",
                    "Callable[[object, SoCallbackAction, SoPrimitiveVertex, "
                    "SoPrimitiveVertex], bool] | None",
                ),
                ("userdata", "object | None"),
            ),
            (
                "self, func: Callable[[object, SoCallbackAction, "
                "SoPrimitiveVertex, SoPrimitiveVertex], bool] | None, "
                "userdata: object | None = ...",
                "None",
            ),
        ),
        ("SoExtSelection", "setPointFilterCallback"): CallbackMethodPolicy(
            (
                (
                    "func",
                    "Callable[[object, SoCallbackAction, SoPrimitiveVertex], "
                    "bool] | None",
                ),
                ("userdata", "object | None"),
            ),
            (
                "self, func: Callable[[object, SoCallbackAction, "
                "SoPrimitiveVertex], bool] | None, "
                "userdata: object | None = ...",
                "None",
            ),
        ),
    }
)

for _soqt_viewer_callback_name in (
    "addStartCallback",
    "removeStartCallback",
    "addFinishCallback",
    "removeFinishCallback",
):
    CALLBACK_METHOD_POLICIES[("SoQtViewer", _soqt_viewer_callback_name)] = (
        CallbackMethodPolicy(
            (
                ("func", "SoQtViewerCallback"),
                ("data", "object | None"),
            ),
            (
                "self, func: SoQtViewerCallback, data: object | None = ...",
                "None",
            ),
        )
    )


PYTHON_SHADOW_METHOD_TYPES = {
    key: policy.shadow_signature
    for key, policy in CALLBACK_METHOD_POLICIES.items()
    if policy.shadow_signature is not None
}
PYTHON_SHADOW_METHOD_TYPES[("SoMFEnum", "setEnums")] = (
    "self, num: int, vals: Sequence[int], "
    "names: SbName | Sequence[SbName | str]",
    "None",
)
PYTHON_SHADOW_METHOD_TYPES[("SoSFEnum", "setEnums")] = (
    "self, num: int, vals: Sequence[int], "
    "names: SbName | Sequence[SbName | str]",
    "None",
)
PYTHON_SHADOW_METHOD_TYPES[("SbByteBuffer", "data")] = ("self", "bytes")
for _box_class, _bounds_type, _origin_type in (
    ("SbBox2s", "tuple[int, int, int, int]", "tuple[int, int]"),
    ("SbBox3s", "tuple[int, int, int, int, int, int]", "tuple[int, int, int]"),
    ("SbBox2i32", "tuple[int, int, int, int]", "tuple[int, int]"),
    ("SbBox3i32", "tuple[int, int, int, int, int, int]", "tuple[int, int, int]"),
):
    PYTHON_SHADOW_METHOD_TYPES[(_box_class, "getBounds")] = (
        "self",
        _bounds_type,
    )
    PYTHON_SHADOW_METHOD_TYPES[(_box_class, "getOrigin")] = (
        "self",
        _origin_type,
    )
PYTHON_SHADOW_METHOD_TYPES[("SbBox2s", "getSize")] = ("self", "SbVec2s")
PYTHON_SHADOW_METHOD_TYPES[("SbBox3s", "getSize")] = ("self", "SbVec3s")
CALLBACK_PARAMETER_TYPE_OVERRIDES = {
    (class_name, method_name, parameter_name): annotation
    for (class_name, method_name), method_policy in CALLBACK_METHOD_POLICIES.items()
    for parameter_name, annotation in method_policy.parameter_types
}


def callback_method_checks(*, excluded_classes=()):
    """Return validator expectations derived from callback policy metadata."""

    return tuple(
        (
            class_name,
            method_name,
            method_policy.parameters(),
            method_policy.shadow_signature[1],
        )
        for (class_name, method_name), method_policy in CALLBACK_METHOD_POLICIES.items()
        if method_policy.shadow_signature is not None
        and class_name not in set(excluded_classes)
    )
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
SENSOR_CALLBACK_CONSTRUCTOR_TYPES = {
    class_name: (
        "SoSensorCallback[%s]" % class_name,
        "object | None",
    )
    for class_name in SENSOR_CALLBACK_CLASSES
}
KNOWN_ITER_ELEMENT_TYPES = {
    "SbIntList": "int",
    "SbName": "str",
    "SbPList": "Any",
    "SbString": "str",
    **vector_iter_element_types(),
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
        ("SoMFDouble", "getValues"),
        ("SoMFDouble", "setValues"),
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
INCOMPLETE_CATEGORY_ACTIONS = {
    "raw C pointers": "add a Python adapter or keep an explicit raw boundary",
    "callbacks": "model the callback signature and ownership contract",
    "unknown output parameters": "add a typed output helper",
    "function pointers": "expose a Callable or an explicit callback boundary",
    "dynamic/runtime API": "model the dynamic behavior or document the limit",
    "uncategorized": "triage and classify before merging",
}


@dataclass(frozen=True)
class IncompleteCategoryPolicy:
    """Disposition and rationale for one reviewed ``Incomplete`` category."""

    disposition: str
    rationale: str


INCOMPLETE_CATEGORY_POLICIES = {
    "raw C pointers": IncompleteCategoryPolicy(
        disposition="intentional",
        rationale=(
            "SWIG exposes a borrowed pointer or ABI-level pointer without a "
            "stable Python owner."
        ),
    ),
    "callbacks": IncompleteCategoryPolicy(
        disposition="intentional",
        rationale=(
            "The native callback boundary still needs an explicit Python "
            "lifecycle and ownership contract."
        ),
    ),
    "unknown output parameters": IncompleteCategoryPolicy(
        disposition="zero budget",
        rationale=(
            "Output parameters must be represented by a typed return tuple "
            "or helper before they are accepted."
        ),
    ),
    "function pointers": IncompleteCategoryPolicy(
        disposition="intentional",
        rationale=(
            "A native C function-pointer ABI is not directly callable as a "
            "safe Python value."
        ),
    ),
    "dynamic/runtime API": IncompleteCategoryPolicy(
        disposition="intentional",
        rationale=(
            "Dynamic factories, opaque objects, and runtime field storage "
            "cannot be recovered from a static declaration alone."
        ),
    ),
    "uncategorized": IncompleteCategoryPolicy(
        disposition="zero budget",
        rationale="Every remaining Incomplete site must have a reviewed category.",
    ),
}

DYNAMIC_RUNTIME_SUBCATEGORIES = (
    "runtime factory returns",
    "opaque pointer/object returns",
    "opaque parameter boundaries",
    "opaque field storage",
)


def classify_dynamic_runtime_site(*, kind: str, method_name: str | None) -> str:
    """Give reviewed dynamic/runtime sites a more useful next-action bucket."""

    if kind == "return" and method_name == "createInstance":
        return "runtime factory returns"
    if kind == "return":
        return "opaque pointer/object returns"
    if kind == "attribute":
        return "opaque field storage"
    return "opaque parameter boundaries"


@dataclass(frozen=True)
class OpaqueReturnAudit:
    """Review record for one intentionally opaque native return."""

    disposition: str
    rationale: str
    next_action: str


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
    get_values_type: str | None = None
    single_value_type: str | None = None
    component_sequence_type: str | None = None
    component_width: int | None = None
    component_parameter_name: str | None = None


def vector_multifield_type_policies():
    """Derive fixed-width numeric multifields from vector value policy."""

    return {
        "SoMF%s" % vector_name[2:]: MultifieldTypePolicy(
            element_type=vector_name,
            set_values_types=(
                vector_name,
                "Sequence[%s]" % vector_policy.component_type,
            ),
            get_values_type=vector_name,
            component_sequence_type="Sequence[%s]"
            % vector_policy.component_type,
            component_width=vector_policy.width,
        )
        for vector_name, vector_policy in VECTOR_TYPE_POLICIES.items()
    }


FIELD_TYPE_POLICIES = {
    "SoSFString": FieldTypePolicy(
        value_type="SbString",
        setter_argument_type="SbString",
        setter_value_type="SbString | str",
    ),
    "SoSFName": FieldTypePolicy(
        value_type="SbName",
        setter_argument_type="SbName",
        setter_value_type="SbName | str",
    ),
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
        get_values_type="str",
        single_value_type="SbName | str",
    ),
    "SoMFBool": MultifieldTypePolicy(
        element_type="bool",
        set_values_types=("bool",),
        get_values_type="bool",
    ),
    "SoMFEnum": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
        get_values_type="int",
    ),
    "SoMFBitMask": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
    ),
    "SoMFFloat": MultifieldTypePolicy(
        element_type="float",
        set_values_types=("float",),
        get_values_type="float",
    ),
    "SoMFString": MultifieldTypePolicy(
        element_type="SbString",
        set_values_types=("SbString | str",),
        get_values_type="str",
        single_value_type="SbString | str",
    ),
    "SoMFRotation": MultifieldTypePolicy(
        element_type="SbRotation",
        set_values_types=("SbRotation", "Sequence[float]"),
        get_values_type="SbRotation",
    ),
    "SoMFMatrix": MultifieldTypePolicy(
        element_type="SbMatrix",
        set_values_types=("SbMatrix",),
        get_values_type="SbMatrix",
    ),
    "SoMFColor": MultifieldTypePolicy(
        element_type="SbColor",
        set_values_types=("SbColor", "SbVec3f", "Sequence[float]"),
        get_values_type="SbColor",
    ),
    "SoMFColorRGBA": MultifieldTypePolicy(
        element_type="SbColor4f",
        set_values_types=("SbColor4f", "Sequence[float]"),
        get_values_type="SbColor4f",
        component_sequence_type="Sequence[float]",
        component_width=4,
        component_parameter_name="rgba",
    ),
    "SoMFDouble": MultifieldTypePolicy(element_type="float"),
    "SoMFEngine": MultifieldTypePolicy(
        element_type="SoEngine",
        set_values_types=("SoEngine",),
        get_values_type="SoEngine",
    ),
    "SoMFInt32": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
        get_values_type="int",
    ),
    "SoMFNode": MultifieldTypePolicy(
        element_type="SoNode",
        set_values_types=("SoNode",),
        get_values_type="SoNode",
    ),
    "SoMFPath": MultifieldTypePolicy(
        element_type="SoPath",
        set_values_types=("SoPath",),
        get_values_type="SoPath",
    ),
    "SoMFPlane": MultifieldTypePolicy(
        element_type="SbPlane",
        set_values_types=("SbPlane",),
        get_values_type="SbPlane",
    ),
    "SoMFShort": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
        get_values_type="int",
    ),
    "SoMFTime": MultifieldTypePolicy(
        element_type="SbTime",
        set_values_types=("SbTime",),
        get_values_type="SbTime",
    ),
    "SoMFUInt32": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
        get_values_type="int",
    ),
    "SoMFUShort": MultifieldTypePolicy(
        element_type="int",
        set_values_types=("int",),
        get_values_type="int",
    ),
    **vector_multifield_type_policies(),
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


def multifield_getvalues_types():
    """Return Python element types returned by wrapped ``getValues`` calls."""

    return {
        field_class: policy.get_values_type
        for field_class, policy in MULTIFIELD_TYPE_POLICIES.items()
        if policy.get_values_type
    }


def multifield_single_value_types():
    """Return Python input types for single-value multifield operations."""

    return {
        field_class: policy.single_value_type
        for field_class, policy in MULTIFIELD_TYPE_POLICIES.items()
        if policy.single_value_type
    }


def multifield_component_sequence_types():
    """Return component-array input types for vector multifield setters."""

    return {
        field_class: (policy.component_sequence_type, policy.component_width)
        for field_class, policy in MULTIFIELD_TYPE_POLICIES.items()
        if policy.component_sequence_type and policy.component_width
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
        # Coin exposes cross-width vector conversions for these legacy
        # wrappers, but the corresponding source vector types are not public
        # Pivy classes. Keep those overloads explicit until the conversion
        # surface is modelled as a first-class binding policy.
        ('parameter', 'SbVec2b', '__init__', 'v'),
        ('parameter', 'SbVec2b', 'setValue', 'v'),
        ('parameter', 'SbVec2i32', '__init__', 'v'),
        ('parameter', 'SbVec2i32', 'setValue', 'v'),
        ('parameter', 'SbVec2s', '__init__', 'v'),
        ('parameter', 'SbVec2s', 'setValue', 'v'),
        ('parameter', 'SbVec3b', '__init__', 'v'),
        ('parameter', 'SbVec3b', 'setValue', 'v'),
        ('parameter', 'SbVec3i32', '__init__', 'v'),
        ('parameter', 'SbVec3i32', 'setValue', 'v'),
        ('parameter', 'SbVec3s', '__init__', 'v'),
        ('parameter', 'SbVec3s', 'setValue', 'v'),
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
        ('parameter', 'SoLinearProfile', 'getTrimCurve', 'points'),
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
        ('parameter', 'SoNurbsProfile', 'getTrimCurve', 'points'),
        ('parameter', 'SoPolygonOffsetElement', 'get', 'styles'),
        ('parameter', 'SoPolygonOffsetElement', 'getDefault', 'styles'),
        ('parameter', 'SoProfile', 'getTrimCurve', 'knotvector'),
        ('parameter', 'SoProfile', 'getTrimCurve', 'points'),
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


def _opaque_return_audits(
    methods: tuple[tuple[str, str], ...],
    *,
    rationale: str,
    next_action: str,
) -> dict[tuple[str, str, str, str], OpaqueReturnAudit]:
    return {
        ("return", class_name, method_name, "return"): OpaqueReturnAudit(
            disposition="intentional native boundary",
            rationale=rationale,
            next_action=next_action,
        )
        for class_name, method_name in methods
    }


# Every current ``opaque pointer/object returns`` site has a concrete review
# record. Keep this separate from the broad triage inventory so a future site
# cannot silently inherit the category without an ownership/lifetime decision.
OPAQUE_RETURN_AUDIT = {
    **_opaque_return_audits(
        (
            ("SoAuditorList", "getObject"),
            ("SoActionMethodList", "__getitem__"),
            ("SoActionMethodList", "get"),
            ("SoFieldContainer", "getUserData"),
            ("SoLazyElement", "getColorIndices"),
            ("SoLazyElement", "getPackedPointer"),
            ("SoReorganizeAction", "getSimplifier"),
            ("SbBSPTree", "getUserData"),
            ("SoConvexDataCache", "getCoordIndices"),
            ("SoConvexDataCache", "getMaterialIndices"),
            ("SoConvexDataCache", "getNormalIndices"),
            ("SoConvexDataCache", "getTexIndices"),
            ("SoNormalCache", "getIndices"),
            ("SoMultiTextureEnabledElement", "getEnabledUnits"),
            ("SoGLVBOElement", "getVertexVBO"),
            ("SoGLVBOElement", "getNormalVBO"),
            ("SoGLVBOElement", "getColorVBO"),
            ("SoGLVBOElement", "getTexCoordVBO"),
            ("SoShininessElement", "getArrayPtr"),
            ("SoTransparencyElement", "getArrayPtr"),
            ("SoLockManager", "GetUnlockString"),
            ("SoOffscreenRenderer", "getDC"),
            ("SbHeap", "extractMin"),
            ("SbHeap", "getMin"),
            ("SbStorage", "get"),
            ("SoVRMLAudioClip", "open"),
        ),
        rationale=(
            "The wrapper returns a borrowed native object or pointer without "
            "a stable Python owner or lifetime contract."
        ),
        next_action=(
            "Add an owning or copying adapter after confirming native "
            "ownership and teardown semantics."
        ),
    ),
    **_opaque_return_audits(
        (
            ("SoMFBool", "startEditing"),
            ("SoMFEnum", "startEditing"),
            ("SoMFFloat", "startEditing"),
            ("SoMFDouble", "startEditing"),
            ("SoMFInt32", "startEditing"),
            ("SoMFShort", "startEditing"),
            ("SoMFUInt32", "startEditing"),
            ("SoMFUShort", "startEditing"),
        ),
        rationale=(
            "The return aliases mutable field storage whose validity ends "
            "with the native edit session."
        ),
        next_action=(
            "Expose an edit-session or snapshot wrapper before typing the "
            "buffer as a Python sequence."
        ),
    ),
    **_opaque_return_audits(
        (
            ("SoGlyph", "getFaceIndices"),
            ("SoGlyph", "getEdgeIndices"),
            ("SoGlyph", "getNextCWEdge"),
            ("SoGlyph", "getNextCCWEdge"),
            ("SoGlyph", "getBitmap"),
            ("SbClip", "getVertexData"),
        ),
        rationale=(
            "The return exposes geometry or bitmap storage owned by a "
            "native cache/object, not an independent Python value."
        ),
        next_action=(
            "Add a copying adapter or a lifetime-bound view with explicit "
            "ownership semantics."
        ),
    ),
}

# These are intentionally opaque pointer-to-pointer or platform-structure
# surfaces. Keep them visible in the report without pretending that the raw
# SWIG representation is a useful Python type.
INCOMPLETE_CATEGORY_OVERRIDES = {
    ("parameter", "SoAction", "getPathCode", "indices"): "raw C pointers",
    ("parameter", "SoAction", "usePathCode", "indices"): "raw C pointers",
    ("parameter", "SoFieldData", "getEnumData", "values"): "raw C pointers",
    ("parameter", "SoSensorManager", "doSelect", "userTimeOut"): "raw C pointers",
    ("parameter", "SoDB", "doSelect", "usertimeout"): "raw C pointers",
}


def classify_incomplete(
    *,
    kind: str,
    class_name: str,
    method_name: str | None,
    parameter_name: str,
    has_raw_pointer_note: bool,
) -> str:
    """Classify one incomplete site using the shared policy rules."""

    key = (kind, class_name, method_name, parameter_name)
    if key in INCOMPLETE_CATEGORY_OVERRIDES:
        return INCOMPLETE_CATEGORY_OVERRIDES[key]

    for rule in INCOMPLETE_RULES:
        if rule.matches(
            kind=kind,
            class_name=class_name,
            method_name=method_name,
            parameter_name=parameter_name,
            has_raw_pointer_note=has_raw_pointer_note,
        ):
            return rule.category
    if key in TRIAGED_INCOMPLETE_SITES:
        return "dynamic/runtime API"
    return "uncategorized"
