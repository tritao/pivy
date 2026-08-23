"""Declarative expectations for the Pivy stub validator."""

from dataclasses import dataclass
from enum import Enum
import os

from tools.pivy_stub_typing_policy import (
    FIELD_ATTRIBUTE_TYPE_POLICIES,
    multifield_component_sequence_types,
    multifield_iter_element_types,
    multifield_single_value_types,
    multifield_setvalues_types,
    MULTIFIELD_TYPE_POLICIES,
    operator_method_checks,
    sequence_method_checks,
    SENSOR_CALLBACK_CLASSES,
    SENSOR_CALLBACK_CONSTRUCTOR_TYPES,
    typedef_and_string_method_checks,
    vector_iter_element_types,
)
from tools.pivy_typing.callbacks import callback_method_checks

GENERATED_HEADER = (
    "# SPDX-License-Identifier: ISC\n"
    "# Generated from local Pivy stubgen output; lightly normalized for checker use.\n"
)


class StubKind(Enum):
    PUBLIC = "public"
    PRIVATE = "private"


@dataclass(frozen=True)
class StubSpec:
    relative_path: str
    kind: StubKind


RUNTIME_UNSUPPORTED_NOTE = (
    "NOTE: SWIG exposes raw C pointers here; keep Incomplete until a "
    "Python-level wrapper exists."
)
STUB_SPECS = (
    StubSpec("coin.pyi", StubKind.PUBLIC),
    StubSpec(os.path.join("gui", "soqt.pyi"), StubKind.PUBLIC),
    StubSpec("_coin.pyi", StubKind.PRIVATE),
    StubSpec(os.path.join("gui", "_soqt.pyi"), StubKind.PRIVATE),
)
REQUIRED_STUBS = tuple(spec.relative_path for spec in STUB_SPECS)
SOQT_COIN_SHARED_TYPES = {
    "SbDict",
    "SbIntList",
    "SbName",
    "SbPList",
    "SbString",
    "SbTime",
    "SbVec2f",
    "SbVec2s",
    "SoDebugError",
    "SoError",
    "SoErrorCallback",
    "SoEvent",
    "SoField",
    "SoMField",
    "SoNotList",
    "SoNotRec",
    "SoSField",
    "SoType",
}
POINTER_HELPER_TYPES = {
    "charp": "str",
    "intp": "int",
    "uintp": "int",
    "longp": "int",
    "floatp": "float",
    "doublep": "float",
}
ITER_CONTAINER_TYPES = {
    "SbIntList": "int",
    "SbName": "str",
    "SbPList": "object",
    "SbString": "str",
    "SbVec2d": "float",
    "SbVec2f": "float",
    "SbVec2s": "int",
    "SbVec3d": "float",
    "SbVec3f": "float",
    "SbVec3s": "int",
    "SbVec4d": "float",
    "SbVec4f": "float",
    "SoMField": "object",
    "SoBaseList": "SoBase",
    "SoGroup": "SoNode",
    "SoNodeList": "SoNode",
    "SoPath": "SoNode",
    "SoPathList": "SoPath",
}
ITER_CONTAINER_TYPES.update(multifield_iter_element_types())
ITER_CONTAINER_TYPES.update(vector_iter_element_types())
CALLBACK_METHOD_CHECKS = {
    "coin.pyi": callback_method_checks(module="coin.pyi"),
    os.path.join("gui", "soqt.pyi"): callback_method_checks(
        module=os.path.join("gui", "soqt.pyi")
    ),
}
ARRAY_METHOD_CHECKS = {"coin.pyi": sequence_method_checks()}
UNSUPPORTED_ARRAY_METHOD_CHECKS = {
    "coin.pyi": (
        ("SbMatrix", "LUDecomposition", "index", "Sequence[int]"),
        ("SbDPMatrix", "LUDecomposition", "index", "Sequence[int]"),
        ("SoSFVec2s", "setValue", "xy", "Sequence[int]"),
        ("SoSFVec3s", "setValue", "xyz", "Sequence[int]"),
    ),
}
RUNTIME_UNSUPPORTED_METHOD_CHECKS = {}
DEFERRED_RAW_METHOD_CHECKS = {
    "coin.pyi": (
        (
            "SoActionMethodList",
            "addMethod",
            {"node": "SoType", "method": "Incomplete"},
            "None",
        ),
        (
            "SoActionMethodList",
            "__setitem__",
            {"i": "int", "value": "Incomplete"},
            "None",
        ),
        (
            "SoActionMethodList",
            "__getitem__",
            {"i": "int"},
            "Incomplete",
        ),
        (
            "SoActionMethodList",
            "get",
            {"i": "int"},
            "Incomplete",
        ),
        (
            "SoInput",
            "setFilePointer",
            {"newFP": "Incomplete"},
            "None",
        ),
        (
            "SoInput",
            "getCurFile",
            {},
            "Incomplete",
        ),
        (
            "SoInput",
            "setBuffer",
            {"bufpointer": "Incomplete"},
            "None",
        ),
        (
            "SoInput",
            "readBinaryArray",
            {"c": "Incomplete", "length": "int"},
            "bool",
        ),
        (
            "SoInput",
            "readBinaryArray",
            {"l": "Incomplete", "length": "int"},
            "bool",
        ),
        (
            "SoInput",
            "readBinaryArray",
            {"f": "Incomplete", "length": "int"},
            "bool",
        ),
        (
            "SoInput",
            "readBinaryArray",
            {"d": "Incomplete", "length": "int"},
            "bool",
        ),
        (
            "SoOutput",
            "setFilePointer",
            {"newFP": "Incomplete"},
            "None",
        ),
        (
            "SoOutput",
            "getFilePointer",
            {},
            "Incomplete",
        ),
        (
            "SoOutput",
            "setBuffer",
            {
                "bufPointer": "Incomplete",
                "initSize": "int",
                "reallocFunc": "Incomplete",
                "offset": "int",
            },
            "None",
        ),
        (
            "SoOutput",
            "getBuffer",
            {"bufPointer": "Incomplete", "nBytes": "Incomplete"},
            "bool",
        ),
        (
            "SbImage",
            "__init__",
            {"bytes": "Incomplete"},
            "None",
        ),
        (
            "SbImage",
            "getValue",
            {},
            "tuple[bytes | None, SbVec2s | SbVec3s, int]",
        ),
        (
            "SoMultiTextureImageElement",
            "getDefault",
            {"size": "SbVec3s", "numComponents": "intp"},
            "Incomplete",
        ),
        (
            "SoMultiTextureImageElement",
            "set",
            {
                "state": "SoState",
                "node": "SoNode",
                "size": "SbVec2s",
                "numComponents": "int",
                "bytes": "Incomplete",
                "wrapS": "int",
                "wrapT": "int",
                "model": "int",
                "blendColor": "SbColor",
            },
            "None",
        ),
        (
            "SoMultiTextureImageElement",
            "get",
            {
                "state": "SoState",
                "size": "SbVec3s",
                "numComponents": "intp",
                "wrapS": "intp",
                "wrapT": "intp",
                "wrapR": "intp",
                "model": "intp",
                "blendColor": "SbColor",
            },
            "Incomplete",
        ),
        (
            "SbHeap",
            "add",
            {"obj": "Incomplete"},
            "int",
        ),
        (
            "SbHeap",
            "extractMin",
            {},
            "Incomplete",
        ),
        (
            "SbHeap",
            "buildHeap",
            {"progresscb": "Incomplete | None", "data": "Incomplete | None"},
            "bool",
        ),
        (
            "SbOctTree",
            "addItem",
            {"item": "Incomplete"},
            "None",
        ),
        (
            "SbOctTree",
            "findItems",
            {
                "sphere": "SbSphere",
                "destarray": "Incomplete",
                "removeduplicates": "bool",
            },
            "None",
        ),
    ),
    os.path.join("gui", "soqt.pyi"): (
        (
            "SoQt",
            "setFatalErrorHandler",
            {
                "cb": "SoQtFatalErrorCallback",
                "userdata": "object",
            },
            "SoQtFatalErrorCallback | None",
        ),
    ),
}
DEFERRED_RAW_ATTRIBUTE_CHECKS = {
    "coin.pyi": (
        ("SoMField", "values", "Incomplete"),
        ("SbHeapFuncs", "eval_func", "Incomplete"),
        ("SbHeapFuncs", "get_index_func", "Incomplete"),
        ("SbHeapFuncs", "set_index_func", "Incomplete"),
        ("SbOctTreeFuncs", "ptinsidefunc", "Incomplete"),
        ("SbOctTreeFuncs", "insideboxfunc", "Incomplete"),
        ("SbOctTreeFuncs", "insidespherefunc", "Incomplete"),
        ("SbOctTreeFuncs", "insideplanesfunc", "Incomplete"),
    ),
}
TYPEDEF_AND_STRING_METHOD_CHECKS = {
    "coin.pyi": typedef_and_string_method_checks(),
}
DOC_TYPED_METHOD_CHECKS = {
    "coin.pyi": (
        (
            "SoType",
            "getInstantiationMethod",
            {},
            "int",
        ),
        (
            "SoVectorizeAction",
            "setColorTranslationMethod",
            {"method": "int"},
            "None",
        ),
        (
            "SoVectorizeAction",
            "getColorTranslationMethod",
            {},
            "int",
        ),
        (
            "SoDepthBufferElement",
            "getFunction",
            {"state": "SoState"},
            "int",
        ),
    ),
    os.path.join("gui", "soqt.pyi"): (
        (
            "SoQt",
            "init",
            {
                "argc": "intp",
                "argv": "Sequence[str]",
                "appname": "str",
                "classname": "str",
            },
            "QWidget",
        ),
        (
            "SoQtViewer",
            "setAnaglyphStereoColorMasks",
            {"left": "Sequence[bool]", "right": "Sequence[bool]"},
            "None",
        ),
    ),
}
POINTER_HELPER_METHOD_CHECKS = {
    "coin.pyi": (
        (
            "SoDB",
            "getHeaderData",
            {
                "headerstring": "SbString",
                "isbinary": "intp",
                "ivversion": "floatp",
                "precallback": "Incomplete",
                "postcallback": "Incomplete",
                "userdata": "Incomplete",
                "substringok": "bool",
            },
            "bool",
        ),
        (
            "SoFieldData",
            "read",
            {
                "input": "SoInput",
                "object": "SoFieldContainer",
                "erroronunknownfield": "bool",
                "notbuiltin": "intp",
            },
            "bool",
        ),
        (
            "SoFieldData",
            "read",
            {
                "input": "SoInput",
                "object": "SoFieldContainer",
                "fieldname": "SbName",
                "foundname": "intp",
            },
            "bool",
        ),
        (
            "SoInput",
            "get",
            {"c": "charp"},
            "bool",
        ),
        (
            "SoInput",
            "getASCIIBuffer",
            {"c": "charp"},
            "bool",
        ),
        (
            "SoInput",
            "getASCIIFile",
            {"c": "charp"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"c": "charp"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"c": "charp", "skip": "bool"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"i": "intp"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"f": "floatp"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"d": "doublep"},
            "bool",
        ),
        (
            "SbColor",
            "setPackedValue",
            {"rgba": "int", "transparency": "floatp"},
            "SbColor",
        ),
        (
            "SoInput",
            "checkISReference",
            {"container": "SoFieldContainer", "fieldname": "SbName", "readok": "intp"},
            "bool",
        ),
        (
            "SoSearchAction",
            "getType",
            {"chkderived": "intp"},
            "SoType",
        ),
        (
            "SoModelMatrixElement",
            "get",
            {"state": "SoState", "isIdentity": "intp"},
            "SbMatrix",
        ),
        (
            "SoSceneManager",
            "getAntialiasing",
            {"smoothing": "intp", "numPasses": "intp"},
            "None",
        ),
        (
            "SoRenderManager",
            "getAntialiasing",
            {"smoothing": "intp", "numPasses": "intp"},
            "None",
        ),
        (
            "SbVec2i32",
            "getValue",
            {"x": "intp", "y": "intp"},
            "None",
        ),
        (
            "SbVec3i32",
            "getValue",
            {"x": "intp", "y": "intp", "z": "intp"},
            "None",
        ),
        (
            "SbVec4i32",
            "getValue",
            {"x": "intp", "y": "intp", "z": "intp", "w": "intp"},
            "None",
        ),
        (
            "SbBox2i32",
            "getSize",
            {"sizeX": "intp", "sizeY": "intp"},
            "None",
        ),
        (
            "SbBox3i32",
            "getSize",
            {"sizeX": "intp", "sizeY": "intp", "sizeZ": "intp"},
            "None",
        ),
        (
            "SoEnvironmentElement",
            "get",
            {
                "state": "SoState",
                "ambientIntensity": "floatp",
                "ambientColor": "SbColor",
                "attenuation": "SbVec3f",
                "fogType": "intp",
                "fogColor": "SbColor",
                "fogVisibility": "floatp",
                "fogStart": "floatp",
            },
            "None",
        ),
        (
            "SoEnvironmentElement",
            "getDefault",
            {
                "ambientIntensity": "floatp",
                "ambientColor": "SbColor",
                "attenuation": "SbVec3f",
                "fogType": "intp",
                "fogColor": "SbColor",
                "fogVisibility": "floatp",
                "fogNear": "floatp",
            },
            "None",
        ),
        (
            "SoProfile",
            "getTrimCurve",
            {
                "state": "SoState",
                "numpoints": "intp",
                "points": "Incomplete",
                "floatspervec": "intp",
                "numknots": "intp",
                "knotvector": "Incomplete",
            },
            "None",
        ),
        (
            "SoProfile",
            "getVertices",
            {"state": "SoState", "numvertices": "intp", "vertices": "SbVec2f"},
            "None",
        ),
        (
            "SoLinearProfile",
            "getTrimCurve",
            {
                "state": "SoState",
                "numpoints": "intp",
                "points": "Incomplete",
                "floatspervec": "intp",
                "numknots": "intp",
                "knotvector": "Incomplete",
            },
            "None",
        ),
        (
            "SoLinearProfile",
            "getVertices",
            {"state": "SoState", "numvertices": "intp", "vertices": "SbVec2f"},
            "None",
        ),
        (
            "SoNurbsProfile",
            "getTrimCurve",
            {
                "state": "SoState",
                "numpoints": "intp",
                "points": "Incomplete",
                "floatspervec": "intp",
                "numknots": "intp",
                "knotvector": "Incomplete",
            },
            "None",
        ),
        (
            "SoNurbsProfile",
            "getVertices",
            {"state": "SoState", "numvertices": "intp", "vertices": "SbVec2f"},
            "None",
        ),
    ),
    os.path.join("gui", "soqt.pyi"): (
        (
            "SoQt",
            "getVersionInfo",
            {"major": "intp | None", "minor": "intp | None", "micro": "intp | None"},
            "None",
        ),
        (
            "SoQtGLWidget",
            "getPointSizeLimits",
            {"range": "SbVec2f", "granularity": "floatp"},
            "None",
        ),
        (
            "SoQtGLWidget",
            "getLineWidthLimits",
            {"range": "SbVec2f", "granularity": "floatp"},
            "None",
        ),
        (
            "SoQtRenderArea",
            "getAntialiasing",
            {"smoothing": "intp", "numPasses": "intp"},
            "None",
        ),
    ),
}
UNSUPPORTED_REFERENCE_METHOD_CHECKS = {
    "coin.pyi": (
        (
            "SbTime",
            "getValue",
            {"sec": "Incomplete", "usec": "longp"},
            "None",
        ),
        (
            "SoInput",
            "readHex",
            {"l": "Incomplete"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"i": "Incomplete"},
            "bool",
        ),
        (
            "SoInput",
            "read",
            {"s": "Incomplete"},
            "bool",
        ),
        (
            "SoOutput",
            "getAvailableCompressionMethods",
            {"num": "uintp"},
            "SbName",
        ),
        (
            "SoPolygonOffsetElement",
            "get",
            {
                "state": "SoState",
                "factor": "floatp",
                "units": "floatp",
                "styles": "Incomplete",
                "on": "intp",
            },
            "None",
        ),
        (
            "SoPolygonOffsetElement",
            "getDefault",
            {
                "factor": "floatp",
                "units": "floatp",
                "styles": "Incomplete",
                "on": "intp",
            },
            "None",
        ),
        (
            "SoDepthBufferElement",
            "get",
            {
                "state": "SoState",
                "test_out": "intp",
                "write_out": "intp",
                "function_out": "intp",
                "range_out": "SbVec2f",
            },
            "None",
        ),
    ),
}
OPERATOR_METHOD_CHECKS = {"coin.pyi": operator_method_checks()}
def _policy_multifield_method_checks():
    checks = []
    setvalues_types = multifield_setvalues_types()
    component_types = multifield_component_sequence_types()
    single_value_types = multifield_single_value_types()
    component_names = {2: "xy", 3: "xyz", 4: "xyzw"}

    for class_name, (component_type, width) in component_types.items():
        for element_type in setvalues_types[class_name]:
            checks.append(
                (
                    class_name,
                    "setValues",
                    {
                        "start": "int",
                        "num": "int",
                        "values": "Sequence[%s]" % element_type,
                    },
                    "None",
                )
            )
        component_name = (
            MULTIFIELD_TYPE_POLICIES[class_name].component_parameter_name
            or component_names[width]
        )
        checks.extend(
            (
                (
                    class_name,
                    "set1Value",
                    {"idx": "int", component_name: component_type},
                    "None",
                ),
                (
                    class_name,
                    "setValue",
                    {component_name: component_type},
                    "None",
                ),
            )
        )

    for class_name, value_type in single_value_types.items():
        checks.extend(
            (
                (
                    class_name,
                    "find",
                    {"value": value_type, "addifnotfound": "bool"},
                    "int",
                ),
                (
                    class_name,
                    "set1Value",
                    {"idx": "int", "value": value_type},
                    "None",
                ),
                (
                    class_name,
                    "__setitem__",
                    {"i": "int", "value": value_type},
                    "None",
                ),
            )
        )

    return tuple(checks)


MULTIFIELD_METHOD_CHECKS = {
    "coin.pyi": (
        (
            "SoMFBool",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[bool]"},
            "None",
        ),
        (
            "SoMFColor",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbColor]"},
            "None",
        ),
        (
            "SoMFColor",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[Sequence[float]]"},
            "None",
        ),
        (
            "SoMFName",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbName | str]"},
            "None",
        ),
        (
            "SoMFNode",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SoNode]"},
            "None",
        ),
        (
            "SoMFRotation",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbRotation]"},
            "None",
        ),
        (
            "SoMFRotation",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[Sequence[float]]"},
            "None",
        ),
        (
            "SoMFString",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbString | str]"},
            "None",
        ),
        (
            "SoMFVec3f",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbVec3f]"},
            "None",
        ),
        (
            "SoMFVec3f",
            "setValues",
            {"start": "int", "num": "int", "values": "Sequence[Sequence[float]]"},
            "None",
        ),
    ) + _policy_multifield_method_checks(),
}
PYTHON_HELPER_METHOD_CHECKS = {
    "coin.pyi": (
        (
            "_SwigNonDynamicMeta",
            "__setattr__",
            {"name": "str", "value": "object"},
            "None",
        ),
        (
            "SoBase",
            "__nonzero__",
            {},
            "bool",
        ),
        (
            "SoFieldContainer",
            "__getattr__",
            {"name": "str"},
            "SoField",
        ),
        (
            "SoFieldContainer",
            "__setattr__",
            {"name": "str", "value": "object"},
            "None",
        ),
        (
            "SoFieldContainer",
            "__dir__",
            {},
            "list[str]",
        ),
        (
            "SoType",
            "fromName",
            {"name": "SbName | str"},
            "SoType",
        ),
        (
            "SoBaseKit",
            "__getattr__",
            {"name": "str"},
            "SoNode | SoField",
        ),
        (
            "SoBaseKit",
            "__setattr__",
            {"name": "str", "value": "object"},
            "None",
        ),
        (
            "SoEngine",
            "__getattr__",
            {"name": "str"},
            "SoField | SoEngineOutput",
        ),
        (
            "SoEngine",
            "__setattr__",
            {"name": "str", "value": "object"},
            "None",
        ),
        (
            "SoPath",
            "index",
            {},
            "Iterator[int]",
        ),
        (
            "SoNodeKitPath",
            "index",
            {},
            "Iterator[int]",
        ),
        (
            "SoGroup",
            "__iadd__",
            {"other": "SoNode | Sequence[SoNode]"},
            "SoGroup",
        ),
        (
            "SoGroup",
            "__isub__",
            {"other": "SoNode | Sequence[SoNode]"},
            "SoGroup",
        ),
        (
            "SoGroup",
            "__contains__",
            {"node": "SoNode"},
            "bool",
        ),
        (
            "SoGroup",
            "getByName",
            {"name": "SbName | str"},
            "SoNode | None",
        ),
    ),
    os.path.join("gui", "soqt.pyi"): (
        (
            "_SwigNonDynamicMeta",
            "__setattr__",
            {"name": "str", "value": "object"},
            "None",
        ),
    ),
}
EXTEND_HELPER_METHOD_CHECKS = {
    "coin.pyi": (
        ("SoEngine", "getByName", {"name": "SbName"}, "SoEngine | None"),
        ("SoNode", "getByName", {"name": "SbName | str"}, "SoNode | None"),
        (
            "SoNode",
            "getByName",
            {"name": "SbName | str", "l": "SoNodeList"},
            "int",
        ),
        ("SoPath", "getByName", {"name": "str"}, "SoPath | None"),
        (
            "SoPath",
            "getByName",
            {"name": "str", "l": "SoPathList"},
            "int",
        ),
        (
            "SoBase",
            "getNamedBase",
            {"name": "SbName | str", "type": "SoType"},
            "SoBase | None",
        ),
        (
            "SoFieldContainer",
            "getField",
            {"name": "SbName | str"},
            "SoField | None",
        ),
        (
            "SoFieldContainer",
            "getEventIn",
            {"name": "SbName | str"},
            "SoField | None",
        ),
        (
            "SoFieldContainer",
            "getEventOut",
            {"name": "SbName | str"},
            "SoField | None",
        ),
        (
            "SoCallbackAction",
            "getMaterial",
            {"index": "int"},
            "tuple[SbColor, SbColor, SbColor, SbColor, float, float]",
        ),
        (
            "SoFieldContainer",
            "getFieldName",
            {"field": "SoField"},
            "str | None",
        ),
        (
            "SoSensorManager",
            "isTimerSensorPending",
            {},
            "SbTime | None",
        ),
        (
            "SoType",
            "createInstance",
            {},
            "SoBase | SoField | SoPath | None",
        ),
        (
            "SbMatrix",
            "getTransform",
            {},
            "tuple[SbVec3f, SbRotation, SbVec3f, SbRotation]",
        ),
        (
            "SbMatrix",
            "getTransform",
            {"center": "SbVec3f"},
            "tuple[SbVec3f, SbRotation, SbVec3f, SbRotation]",
        ),
        ("SbMatrix", "multMatrixVec", {"src": "SbVec3f"}, "SbVec3f"),
        ("SbMatrix", "multDirMatrix", {"src": "SbVec3f"}, "SbVec3f"),
        ("SbMatrix", "multVecMatrix", {"src": "SbVec3f"}, "SbVec3f"),
        ("SbMatrix", "multVecMatrix", {"src": "SbVec4f"}, "SbVec4f"),
        ("SbRotation", "getAxisAngle", {}, "tuple[SbVec3f, float]"),
        ("SbRotation", "getMatrix", {}, "SbMatrix"),
        ("SbRotation", "multVec", {"src": "SbVec3f"}, "SbVec3f"),
        ("SbDPRotation", "getAxisAngle", {}, "tuple[SbVec3d, float]"),
        ("SbDPRotation", "getMatrix", {}, "SbDPMatrix"),
        (
            "SbViewVolume",
            "projectPointToLine",
            {"pt": "SbVec2f"},
            "tuple[SbVec3f, SbVec3f]",
        ),
        (
            "SbViewVolume",
            "projectToScreen",
            {"src": "SbVec3f"},
            "SbVec3f",
        ),
    ),
}
METHOD_RETURN_TYPE_CHECKS = {
    "coin.pyi": (),
    os.path.join("gui", "soqt.pyi"): (),
}
PROPERTY_ATTRIBUTE_CHECKS = {
    "coin.pyi": tuple(
        (class_name, attribute_name, attribute_type)
        for class_name, attributes in FIELD_ATTRIBUTE_TYPE_POLICIES.items()
        for attribute_name, attribute_type in attributes.items()
    ),
}
MYPY_SNIPPET = """
from typing import Any, Callable, Iterator, Sequence

from pivy.coin import (
    SbIntList,
    SbColor,
    SbColor4f,
    SbMatrix,
    SbName,
    SbPList,
    SbRotation,
    SbString,
    SbTime,
    SbVec2f,
    SbVec2s,
    SbVec3f,
    SbVec3s,
    SbViewportRegion,
    SbViewVolume,
    ScXMLStateMachine,
    SoAction,
    SoBase,
    SoBaseKit,
    SoCallback,
    SoCallbackAction,
    SoDB,
    SoDepthBufferElement,
    SoDragger,
    SoEngine,
    SoEngineOutput,
    SoEvent,
    SoEventCallback,
    SoField,
    SoFieldData,
    SoFieldContainer,
    SoGLRenderAction,
    SoGroup,
    SoIntersectionDetectionAction,
    SoIntersectingPrimitive,
    SoInput,
    SoMFBool,
    SoMFColor,
    SoMFName,
    SoMFNode,
    SoMFRotation,
    SoMFString,
    SoMFVec3f,
    SoModelMatrixElement,
    SoNode,
    SoNodeKitPath,
    SoNodeList,
    SoNormalBundle,
    SoNormalGenerator,
    SoPath,
    SoPickedPoint,
    SoPrimitiveVertex,
    SoRenderManager,
    SoSceneManager,
    SoSearchAction,
    SoSelection,
    SoSensorManager,
    SoState,
    SoTimerSensor,
    SoType,
    SoTypeList,
    SoVectorizeAction,
    charp,
    doublep,
    floatp,
    intp,
)
from pivy.gui.soqt import (
    QEvent,
    QWidget,
    SoQt,
    SoQtRenderArea,
    SoQtViewer,
    floatp as SoQtFloatp,
    intp as SoQtIntp,
)
from pivy._coin import cast as coin_cast
from pivy.gui._soqt import cast as soqt_cast

reveal_type(SoDB.init)
reveal_type(SbVec3f.dot)
reveal_type(SoQt.getWidgetSize)
reveal_type(coin_cast)
reveal_type(soqt_cast)

owned: bool = intp().thisown
raw: object = intp().cast()
text: str = charp().value()
number: int = intp().value()
ints: Iterator[int] = iter(SbIntList())
nodes: Iterator[SoNode] = iter(SoNodeList())
unknowns: Iterator[object] = iter(SbPList())

vec = SbVec3f([1.0, 2.0, 3.0])
vec.setValue([4.0, 5.0, 6.0])
vec_values: Sequence[float] = vec.getValue()
short_vec2 = SbVec2s([1, 2])
short_vec2.setValue([3, 4])
short_vec2_values: Sequence[int] = short_vec2.getValue()
short_vec3 = SbVec3s([1, 2, 3])
short_vec3.setValue([4, 5, 6])

matrix = SbMatrix(
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)
matrix_values: Sequence[Sequence[float]] = matrix.getValue()
matrix_row: Sequence[float] = matrix[0]
matrix_transform: tuple[SbVec3f, SbRotation, SbVec3f, SbRotation] = (
    matrix.getTransform()
)
matrix_transform_centered: tuple[SbVec3f, SbRotation, SbVec3f, SbRotation] = (
    matrix.getTransform(SbVec3f(0.0, 0.0, 0.0))
)

view_volume = SbViewVolume()
view_line: tuple[SbVec3f, SbVec3f] = view_volume.projectPointToLine(SbVec2f())
screen_point: SbVec3f = view_volume.projectToScreen(SbVec3f())
view_volume_type: int = view_volume.type
view_volume_projected_point: SbVec3f = view_volume.projPoint
view_volume_projected_direction: SbVec3f = view_volume.projDir
view_volume_near_distance: float = view_volume.nearDist
view_volume_near_to_far: float = view_volume.nearToFar
view_volume_lower_left: SbVec3f = view_volume.llf
view_volume_lower_right: SbVec3f = view_volume.lrf
view_volume_upper_left: SbVec3f = view_volume.ulf

color = SbColor([0.1, 0.2, 0.3])
color.setHSVValue([0.5, 0.6, 0.7])
color_hsv: Sequence[float] = color.getHSVValue()

rgba = SbColor4f([0.1, 0.2, 0.3, 0.4])
rgba_values: Sequence[float] = rgba.getValue()

rotation = SbRotation([0.0, 0.0, 0.0, 1.0])
rotation_values: Sequence[float] = rotation.getValue()
rotation_product: SbRotation = rotation.__imul__(SbRotation.identity())
packed_transparency = floatp()
packed_color: SbColor = SbColor().setPackedValue(0, packed_transparency)

vec_divided: SbVec3f = vec.__itruediv__(2.0)
time = SbTime(10.0)
time_ratio: float = time / SbTime(2.0)
time_divided: SbTime = time.__itruediv__(2.0)
reader = SoInput()
char_buffer = charp()
reader.get(char_buffer)
reader.getASCIIBuffer(char_buffer)
reader.getASCIIFile(char_buffer)
reader.read(char_buffer)
reader.read(char_buffer, True)
reader.read(intp())
reader.read(floatp())
reader.read(doublep())
field_data = SoFieldData()
field_container = SoFieldContainer()
field_not_builtin = intp()
field_data.read(reader, field_container, True, field_not_builtin)
field_found_name = intp()
field_data.read(reader, field_container, SbName("field"), field_found_name)
reader.checkISReference(field_container, SbName("field"), intp())
header_is_binary = intp()
header_version = floatp()
header_callback: Any = None
header_userdata: Any = None
SoDB.getHeaderData(
    SbString(""),
    header_is_binary,
    header_version,
    header_callback,
    header_callback,
    header_userdata,
)
model_matrix_with_identity: SbMatrix = SoModelMatrixElement.get(
    SoState(SoAction(), SoTypeList()), intp()
)
search_type_with_flag: SoType = SoSearchAction().getType(intp())
scene_smoothing = intp()
scene_num_passes = intp()
SoSceneManager().getAntialiasing(scene_smoothing, scene_num_passes)
render_smoothing = intp()
render_num_passes = intp()
SoRenderManager().getAntialiasing(render_smoothing, render_num_passes)

node_id: int = SoNode.getNextNodeId()
string_equal: bool = SbString("value") == "value"
string_not_equal: int = SbString("value").__nq__("other")
name_equal: bool = SbName("value") == "value"
name_not_equal: int = SbName("value").__nq__("other")
soqt_area = SoQtRenderArea()
soqt_type: SoType = soqt_area.getTypeId()
soqt_instantiation_method: int = SoType.badType().getInstantiationMethod()
soqt_area.sendSoEvent(SoEvent())
soqt_vec_divided: SbVec2f = SbVec2f(1.0, 2.0).__itruediv__(2.0)
soqt_time_ratio: float = SbTime(10.0) / SbTime(2.0)
soqt_argc = SoQtIntp()
soqt_widget: QWidget = SoQt.init(soqt_argc, ["pivy"], "Pivy")
soqt_version_major = SoQtIntp()
SoQt.getVersionInfo(soqt_version_major, None, None)
soqt_granularity = SoQtFloatp()
soqt_area.getPointSizeLimits(SbVec2f(), soqt_granularity)
soqt_area.getLineWidthLimits(SbVec2f(), soqt_granularity)
soqt_smoothing = SoQtIntp()
soqt_num_passes = SoQtIntp()
soqt_area.getAntialiasing(soqt_smoothing, soqt_num_passes)
SoQtViewer().setAnaglyphStereoColorMasks(
    [True, False, True], [False, True, False]
)

SoMFBool().setValues(0, 2, [True, False])
SoMFColor().setValues(0, 2, [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
SoMFName().setValues(0, 2, ["left", SbName("right")])
SoMFNode().setValues(0, 1, [SoNode()])
SoMFRotation().setValues(0, 1, [[0.0, 0.0, 0.0, 1.0]])
SoMFString().setValues(0, 2, ["left", SbString("right")])
SoMFVec3f().setValues(0, 2, [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

base: SoBase = SoNode()
created: SoBase | SoField | SoPath | None = SoType.badType().createInstance()
instantiation_method: int = SoType.badType().getInstantiationMethod()
vectorize_action = SoVectorizeAction()
vectorize_action.setColorTranslationMethod(SoVectorizeAction.AS_IS)
color_translation_method: int = vectorize_action.getColorTranslationMethod()
depth_write_function: int = SoDepthBufferElement.getFunction(
    SoState(SoCallbackAction(), SoTypeList())
)
base_alive: bool = base.__nonzero__()
path_indexes: Iterator[int] = SoPath().index()
nodekit_indexes: Iterator[int] = SoNodeKitPath().index()
group = SoGroup()
group += SoNode()
group += [SoNode()]
group -= (SoNode(),)
named_child: SoNode | None = group.getByName("child")
named_child_by_name: SoNode | None = group.getByName(SbName("child"))

field_container = SoFieldContainer()
field_value: SoField = field_container.__getattr__("field")
field_container.__setattr__("field", object())
field_names: list[str] = field_container.__dir__()
field_name: str | None = field_container.getFieldName(SoField())
basekit = SoBaseKit()
part_value: SoNode | SoField = basekit.__getattr__("part")
basekit.__setattr__("part", SoNode())
engine = SoEngine()
output_value: SoField | SoEngineOutput = engine.__getattr__("output")
engine.__setattr__("output", object())

sensor_manager: SoSensorManager = SoDB.getSensorManager()
next_timer: SbTime | None = sensor_manager.isTimerSensorPending()
material: tuple[SbColor, SbColor, SbColor, SbColor, float, float] = (
    SoCallbackAction().getMaterial()
)

def changed_callback(data: Any) -> None: ...
SoDB.getSensorManager().setChangedCallback(changed_callback, None)

def action_callback(data: Any, action: SoAction) -> None: ...
SoCallback().setCallback(action_callback, None)

def callback_action_node(
    data: Any, action: SoCallbackAction, node: SoNode
) -> int:
    return 0

def callback_action_triangle(
    data: Any,
    action: SoCallbackAction,
    v1: SoPrimitiveVertex,
    v2: SoPrimitiveVertex,
    v3: SoPrimitiveVertex,
) -> None: ...

def callback_action_line(
    data: Any,
    action: SoCallbackAction,
    v1: SoPrimitiveVertex,
    v2: SoPrimitiveVertex,
) -> None: ...

def callback_action_point(
    data: Any, action: SoCallbackAction, vertex: SoPrimitiveVertex
) -> None: ...

callback_action = SoCallbackAction()
callback_action.addPreCallback(SoType.badType(), callback_action_node, None)
callback_action.addPostCallback(SoType.badType(), callback_action_node, None)
callback_action.addPreTailCallback(callback_action_node, None)
callback_action.addPostTailCallback(callback_action_node, None)
callback_action.addTriangleCallback(
    SoType.badType(), callback_action_triangle, None
)
callback_action.addLineSegmentCallback(
    SoType.badType(), callback_action_line, None
)
callback_action.addPointCallback(SoType.badType(), callback_action_point, None)

def gl_pass_callback(data: Any) -> None: ...
def gl_abort_callback(data: Any) -> int:
    return 0

def gl_pre_render_callback(data: Any, action: SoGLRenderAction) -> None: ...

gl_action = SoGLRenderAction(SbViewportRegion())
gl_action.setPassCallback(gl_pass_callback, None)
gl_action.setAbortCallback(gl_abort_callback, None)
gl_action.addPreRenderCallback(gl_pre_render_callback, None)
gl_action.removePreRenderCallback(gl_pre_render_callback, None)

def visitation_callback(data: Any, path: SoPath) -> int:
    return 0

def intersection_filter(data: Any, left: SoPath, right: SoPath) -> bool:
    return True

def intersection_callback(
    data: Any,
    left: SoIntersectingPrimitive,
    right: SoIntersectingPrimitive,
) -> int:
    return 0

intersection_action = SoIntersectionDetectionAction()
intersection_action.addVisitationCallback(
    SoType.badType(), visitation_callback, None
)
intersection_action.removeVisitationCallback(
    SoType.badType(), visitation_callback, None
)
intersection_action.setFilterCallback(intersection_filter, None)
intersection_action.addIntersectionCallback(intersection_callback, None)
intersection_action.removeIntersectionCallback(intersection_callback, None)
intersecting_primitive = SoIntersectingPrimitive()
primitive_path: SoPath | None = intersecting_primitive.path
primitive_type: int = intersecting_primitive.type
primitive_vertex: SbVec3f = intersecting_primitive.vertex
primitive_xf_vertex: SbVec3f = intersecting_primitive.xf_vertex

def dragger_callback(data: Any, dragger: SoDragger) -> None: ...

dragger = SoDragger()
dragger.addStartCallback(dragger_callback, None)
dragger.removeStartCallback(dragger_callback, None)
dragger.addMotionCallback(dragger_callback, None)
dragger.removeMotionCallback(dragger_callback, None)
dragger.addFinishCallback(dragger_callback, None)
dragger.removeFinishCallback(dragger_callback, None)
dragger.addValueChangedCallback(dragger_callback, None)
dragger.removeValueChangedCallback(dragger_callback, None)
dragger.addOtherEventCallback(dragger_callback, None)
dragger.removeOtherEventCallback(dragger_callback, None)

def event_callback(data: Any, event: SoEventCallback) -> None: ...
event_node = SoEventCallback()
event_handle: tuple[Callable[[object, SoEventCallback], None], object] = (
    event_node.addEventCallback(SoType.badType(), event_callback, None)
)
event_node.removeEventCallback(SoType.badType(), event_handle)

def selection_callback(data: Any, path: SoPath) -> None: ...
def selection_class_callback(data: Any, selection: SoSelection) -> None: ...
def pick_filter_callback(data: Any, point: SoPickedPoint) -> SoPath:
    return SoPath()

SoSelection().addSelectionCallback(selection_callback, None)
selection = SoSelection()
selection.addSelectionCallback(selection_callback, None)
selection.removeSelectionCallback(selection_callback, None)
selection.addDeselectionCallback(selection_callback, None)
selection.removeDeselectionCallback(selection_callback, None)
selection.addStartCallback(selection_class_callback, None)
selection.removeStartCallback(selection_class_callback, None)
selection.addFinishCallback(selection_class_callback, None)
selection.removeFinishCallback(selection_class_callback, None)
selection.setPickFilterCallback(pick_filter_callback, None, 1)
selection.addChangeCallback(selection_class_callback, None)
selection.removeChangeCallback(selection_class_callback, None)

def scene_render_callback(data: Any, manager: SoSceneManager) -> None: ...
def render_callback(data: Any, manager: SoRenderManager) -> None: ...

SoSceneManager().setRenderCallback(scene_render_callback, None)
render_manager = SoRenderManager()
render_manager.setRenderCallback(render_callback, None)
render_manager.addPreRenderCallback(render_callback, None)
render_manager.removePreRenderCallback(render_callback, None)
render_manager.addPostRenderCallback(render_callback, None)
render_manager.removePostRenderCallback(render_callback, None)

search_during_all: bool = SoSearchAction().duringSearchAll
def normal_generator(bundle: SoNormalBundle) -> SoNormalGenerator | None:
    return bundle.generator

def scxml_delete_callback(data: Any, machine: ScXMLStateMachine) -> None: ...
def scxml_state_callback(
    data: Any,
    machine: ScXMLStateMachine,
    state: str,
    entered: bool,
    success: bool,
) -> None: ...

state_machine = ScXMLStateMachine()
state_machine.addDeleteCallback(scxml_delete_callback, None)
state_machine.removeDeleteCallback(scxml_delete_callback, None)
state_machine.addStateChangeCallback(scxml_state_callback, None)
state_machine.removeStateChangeCallback(scxml_state_callback, None)

def timer_callback(data: Any, sensor: SoTimerSensor) -> None: ...
timer = SoTimerSensor(timer_callback, None)

def qevent_callback(data: object, event: QEvent) -> object: ...
SoQtRenderArea().setEventCallback(qevent_callback, None)
"""
