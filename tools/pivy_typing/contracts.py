"""Binding-owned method contracts shared by generation and validation."""

from __future__ import annotations

import ast

try:
    from tools.pivy_stub_typing_policy import (
        DOCUMENTED_METHOD_RULES,
        EXTEND_HELPER_METHOD_TYPES,
        MULTIFIELD_TYPE_POLICIES,
        MethodSignatureRule,
        OPERATOR_METHOD_RULES,
        PolicyTarget,
        PYTHON_HELPER_METHOD_POLICIES,
        SEQUENCE_METHOD_RULES,
        TYPEDEF_AND_STRING_METHOD_RULES,
        multifield_component_sequence_types,
        multifield_setvalues_types,
        multifield_single_value_types,
        policy_owner_for_target,
    )
except ImportError:
    from pivy_stub_typing_policy import (
        DOCUMENTED_METHOD_RULES,
        EXTEND_HELPER_METHOD_TYPES,
        MULTIFIELD_TYPE_POLICIES,
        MethodSignatureRule,
        OPERATOR_METHOD_RULES,
        PolicyTarget,
        PYTHON_HELPER_METHOD_POLICIES,
        SEQUENCE_METHOD_RULES,
        TYPEDEF_AND_STRING_METHOD_RULES,
        multifield_component_sequence_types,
        multifield_setvalues_types,
        multifield_single_value_types,
        policy_owner_for_target,
    )


def _method_rule(class_name, method_name, parameters, return_type, reason):
    target = PolicyTarget(class_name, method_name)
    return MethodSignatureRule(
        target=target,
        parameter_types=tuple(parameters.items()),
        return_type=return_type,
        reason=reason,
        source="tools/pivy_typing/contracts.py",
        owner=policy_owner_for_target(target),
    )


POINTER_HELPER_METHOD_RULES = (
    _method_rule(
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
        "Native output and callback helper parameters remain explicit",
    ),
    _method_rule(
        "SoFieldData",
        "read",
        {
            "input": "SoInput",
            "object": "SoFieldContainer",
            "erroronunknownfield": "bool",
            "notbuiltin": "intp",
        },
        "bool",
        "Native scalar output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoFieldData",
        "read",
        {
            "input": "SoInput",
            "object": "SoFieldContainer",
            "fieldname": "SbName",
            "foundname": "intp",
        },
        "bool",
        "Native scalar output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "get", {"c": "charp"}, "bool",
        "Native character output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "getASCIIBuffer", {"c": "charp"}, "bool",
        "Native character output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "getASCIIFile", {"c": "charp"}, "bool",
        "Native character output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"c": "charp"}, "bool",
        "Native character output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"c": "charp", "skip": "bool"}, "bool",
        "Native character output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"i": "intp"}, "bool",
        "Native integer output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"f": "floatp"}, "bool",
        "Native float output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"d": "doublep"}, "bool",
        "Native double output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"i": "uintp"}, "bool",
        "Native unsigned integer output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"s": "shortp"}, "bool",
        "Native short output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "read", {"s": "ushortp"}, "bool",
        "Native unsigned short output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "readHex", {"l": "uint32p"}, "bool",
        "Native hexadecimal output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "readByte", {"b": "int8p"}, "bool",
        "Native byte output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput", "readByte", {"b": "uint8p"}, "bool",
        "Native byte output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SbTime", "getValue", {"sec": "timep", "usec": "longp"}, "None",
        "Native time output helpers represented by Python pointer values",
    ),
    _method_rule(
        "SoFieldContainer",
        "getFieldsMemorySize",
        {"managed": "sizep", "unmanaged": "sizep"},
        "None",
        "Native size output helpers represented by Python pointer values",
    ),
    _method_rule(
        "SbColor",
        "setPackedValue",
        {"rgba": "int", "transparency": "floatp"},
        "SbColor",
        "Native transparency output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoInput",
        "checkISReference",
        {"container": "SoFieldContainer", "fieldname": "SbName", "readok": "intp"},
        "bool",
        "Native reference output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoSearchAction", "getType", {"chkderived": "intp"}, "SoType",
        "Native boolean output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoModelMatrixElement",
        "get",
        {"state": "SoState", "isIdentity": "intp"},
        "SbMatrix",
        "Native identity output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoSceneManager",
        "getAntialiasing",
        {"smoothing": "intp", "numPasses": "intp"},
        "None",
        "Native antialiasing outputs represented by Python pointer values",
    ),
    _method_rule(
        "SoRenderManager",
        "getAntialiasing",
        {"smoothing": "intp", "numPasses": "intp"},
        "None",
        "Native antialiasing outputs represented by Python pointer values",
    ),
    _method_rule(
        "SbVec2i32", "getValue", {"x": "intp", "y": "intp"}, "None",
        "Native vector outputs represented by Python pointer values",
    ),
    _method_rule(
        "SbVec3i32",
        "getValue",
        {"x": "intp", "y": "intp", "z": "intp"},
        "None",
        "Native vector outputs represented by Python pointer values",
    ),
    _method_rule(
        "SbVec4i32",
        "getValue",
        {"x": "intp", "y": "intp", "z": "intp", "w": "intp"},
        "None",
        "Native vector outputs represented by Python pointer values",
    ),
    _method_rule(
        "SbBox2i32",
        "getSize",
        {"sizeX": "intp", "sizeY": "intp"},
        "None",
        "Native box outputs represented by Python pointer values",
    ),
    _method_rule(
        "SbBox3i32",
        "getSize",
        {"sizeX": "intp", "sizeY": "intp", "sizeZ": "intp"},
        "None",
        "Native box outputs represented by Python pointer values",
    ),
    _method_rule(
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
        "Native environment outputs represented by Python pointer values",
    ),
    _method_rule(
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
        "Native environment outputs represented by Python pointer values",
    ),
    _method_rule(
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
        "Native curve buffers remain explicit raw boundaries",
    ),
    _method_rule(
        "SoProfile",
        "getVertices",
        {"state": "SoState", "numvertices": "intp", "vertices": "SbVec2f"},
        "None",
        "Native vertex output helper represented by a Python pointer value",
    ),
    _method_rule(
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
        "Native curve buffers remain explicit raw boundaries",
    ),
    _method_rule(
        "SoLinearProfile",
        "getVertices",
        {"state": "SoState", "numvertices": "intp", "vertices": "SbVec2f"},
        "None",
        "Native vertex output helper represented by a Python pointer value",
    ),
    _method_rule(
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
        "Native curve buffers remain explicit raw boundaries",
    ),
    _method_rule(
        "SoNurbsProfile",
        "getVertices",
        {"state": "SoState", "numvertices": "intp", "vertices": "SbVec2f"},
        "None",
        "Native vertex output helper represented by a Python pointer value",
    ),
    _method_rule(
        "SoQt",
        "getVersionInfo",
        {"major": "intp | None", "minor": "intp | None", "micro": "intp | None"},
        "None",
        "SoQt version outputs represented by optional Python pointer values",
    ),
    _method_rule(
        "SoQtGLWidget",
        "getPointSizeLimits",
        {"range": "SbVec2f", "granularity": "floatp"},
        "None",
        "SoQt range output helper represented by Python pointer values",
    ),
    _method_rule(
        "SoQtGLWidget",
        "getLineWidthLimits",
        {"range": "SbVec2f", "granularity": "floatp"},
        "None",
        "SoQt range output helper represented by Python pointer values",
    ),
    _method_rule(
        "SoQtRenderArea",
        "getAntialiasing",
        {"smoothing": "intp", "numPasses": "intp"},
        "None",
        "SoQt antialiasing outputs represented by Python pointer values",
    ),
)


def pointer_helper_method_checks(module):
    """Project pointer contracts into the validator's legacy shape."""

    if module.endswith("soqt.pyi"):
        rules = tuple(
            rule for rule in POINTER_HELPER_METHOD_RULES
            if rule.target.class_name.startswith("SoQt")
        )
    else:
        rules = tuple(
            rule for rule in POINTER_HELPER_METHOD_RULES
            if not rule.target.class_name.startswith("SoQt")
        )
    return tuple(rule.check for rule in rules)


RAW_BOUNDARY_METHOD_RULES = (
    _method_rule(
        "SoActionMethodList", "addMethod",
        {"node": "SoType", "method": "Incomplete"}, "None",
        "Native action-method callback ABI remains an explicit raw boundary",
    ),
    _method_rule(
        "SoActionMethodList", "__setitem__",
        {"i": "int", "value": "Incomplete"}, "None",
        "Native action-method callback ABI remains an explicit raw boundary",
    ),
    _method_rule(
        "SoActionMethodList", "__getitem__", {"i": "int"}, "Incomplete",
        "Native action-method callback ABI remains an explicit raw boundary",
    ),
    _method_rule(
        "SoActionMethodList", "get", {"i": "int"}, "Incomplete",
        "Native action-method callback ABI remains an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "setFilePointer", {"newFP": "Incomplete"}, "None",
        "Borrowed native file pointers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "getCurFile", {}, "Incomplete",
        "Borrowed native file pointers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "setBuffer", {"bufpointer": "Incomplete"}, "None",
        "Native input buffers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "readBinaryArray", {"c": "Incomplete", "length": "int"}, "bool",
        "Native binary buffers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "readBinaryArray", {"l": "Incomplete", "length": "int"}, "bool",
        "Native binary buffers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "readBinaryArray", {"f": "Incomplete", "length": "int"}, "bool",
        "Native binary buffers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoInput", "readBinaryArray", {"d": "Incomplete", "length": "int"}, "bool",
        "Native binary buffers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoOutput", "setFilePointer", {"newFP": "Incomplete"}, "None",
        "Borrowed native file pointers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoOutput", "getFilePointer", {}, "Incomplete",
        "Borrowed native file pointers remain an explicit raw boundary",
    ),
    _method_rule(
        "SoOutput", "setBuffer",
        {
            "bufPointer": "Incomplete",
            "initSize": "int",
            "reallocFunc": "Incomplete",
            "offset": "int",
        },
        "None",
        "Native output buffers and reallocators remain raw boundaries",
    ),
    _method_rule(
        "SoOutput", "getBuffer",
        {"bufPointer": "Incomplete", "nBytes": "sizep"}, "bool",
        "Native output buffers remain an explicit raw boundary",
    ),
    _method_rule(
        "SbImage", "__init__", {"bytes": "Incomplete"}, "None",
        "Native image storage remains an explicit raw boundary",
    ),
    _method_rule(
        "SbImage", "getValue", {},
        "tuple[bytes | None, SbVec2s | SbVec3s, int]",
        "Image data is exposed through the reviewed snapshot contract",
    ),
    _method_rule(
        "SoMultiTextureImageElement", "getDefault",
        {"size": "SbVec3s", "numComponents": "intp"}, "Incomplete",
        "Native texture image storage remains an explicit raw boundary",
    ),
    _method_rule(
        "SoMultiTextureImageElement", "set",
        {
            "state": "SoState", "node": "SoNode", "size": "SbVec2s",
            "numComponents": "int", "bytes": "Incomplete",
            "wrapS": "SoTextureWrap", "wrapT": "SoTextureWrap",
            "model": "SoTextureModel", "blendColor": "SbColor",
        },
        "None",
        "Native texture image storage remains an explicit raw boundary",
    ),
    _method_rule(
        "SoMultiTextureImageElement", "get",
        {
            "state": "SoState", "size": "SbVec3s", "numComponents": "intp",
            "wrapS": "intp", "wrapT": "intp", "wrapR": "intp",
            "model": "intp", "blendColor": "SbColor",
        },
        "Incomplete",
        "Native texture image storage remains an explicit raw boundary",
    ),
    _method_rule(
        "SbHeap", "add", {"obj": "Incomplete"}, "int",
        "Native heap userdata remains an explicit raw boundary",
    ),
    _method_rule(
        "SbHeap", "extractMin", {}, "Incomplete",
        "Native heap userdata remains an explicit raw boundary",
    ),
    _method_rule(
        "SbHeap", "buildHeap",
        {"progresscb": "Incomplete | None", "data": "Incomplete | None"}, "bool",
        "Native heap callback ABI remains an explicit raw boundary",
    ),
    _method_rule(
        "SbOctTree", "addItem", {"item": "Incomplete"}, "None",
        "Native octree userdata remains an explicit raw boundary",
    ),
    _method_rule(
        "SbOctTree", "findItems",
        {"sphere": "SbSphere", "destarray": "Incomplete", "removeduplicates": "bool"},
        "None",
        "Native octree output storage remains an explicit raw boundary",
    ),
    _method_rule(
        "SoQt", "setFatalErrorHandler",
        {
            "cb": "SoQtFatalErrorCallback[_SoQtFatalErrorDataT]",
            "userdata": "_SoQtFatalErrorDataT",
        },
        "SoQtFatalErrorCallback[object] | None",
        "SoQt fatal-error callback ownership is modeled separately from raw ABI data",
    ),
)


def raw_boundary_method_checks(module):
    if module.endswith("soqt.pyi"):
        rules = tuple(
            rule for rule in RAW_BOUNDARY_METHOD_RULES
            if rule.target.class_name.startswith("SoQt")
        )
    else:
        rules = tuple(
            rule for rule in RAW_BOUNDARY_METHOD_RULES
            if not rule.target.class_name.startswith("SoQt")
        )
    return tuple(rule.check for rule in rules)


RAW_BOUNDARY_ATTRIBUTE_CHECKS = {
    "coin.pyi": (
        ("SbHeapFuncs", "eval_func", "Incomplete"),
        ("SbHeapFuncs", "get_index_func", "Incomplete"),
        ("SbHeapFuncs", "set_index_func", "Incomplete"),
        ("SbOctTreeFuncs", "ptinsidefunc", "Incomplete"),
        ("SbOctTreeFuncs", "insideboxfunc", "Incomplete"),
        ("SbOctTreeFuncs", "insidespherefunc", "Incomplete"),
        ("SbOctTreeFuncs", "insideplanesfunc", "Incomplete"),
    ),
}


def _multifield_method_rules():
    rules = [
        _method_rule(
            "SoMFBool", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[bool]"}, "None",
            "Multifield sequence values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFColor", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbColor]"}, "None",
            "Multifield color values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFColor", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[Sequence[float]]"}, "None",
            "Multifield color values are accepted as component sequences",
        ),
        _method_rule(
            "SoMFName", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbName | str]"}, "None",
            "Multifield name values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFNode", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SoNode | None]"}, "None",
            "Multifield node values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFRotation", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbRotation]"}, "None",
            "Multifield rotation values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFRotation", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[Sequence[float]]"}, "None",
            "Multifield rotation values are accepted as component sequences",
        ),
        _method_rule(
            "SoMFString", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbString | str]"}, "None",
            "Multifield string values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFVec3f", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[SbVec3f]"}, "None",
            "Multifield vector values are accepted as Python sequences",
        ),
        _method_rule(
            "SoMFVec3f", "setValues",
            {"start": "int", "num": "int", "values": "Sequence[Sequence[float]]"}, "None",
            "Multifield vector values are accepted as component sequences",
        ),
    ]
    component_names = {2: "xy", 3: "xyz", 4: "xyzw"}
    for class_name, (component_type, width) in multifield_component_sequence_types().items():
        policy = MULTIFIELD_TYPE_POLICIES[class_name]
        component_name = policy.component_parameter_name or component_names[width]
        for element_type in multifield_setvalues_types()[class_name]:
            rules.append(
                _method_rule(
                    class_name,
                    "setValues",
                    {"start": "int", "num": "int", "values": "Sequence[%s]" % element_type},
                    "None",
                    "Multifield sequence values are derived from field policy",
                )
            )
        rules.extend(
            (
                _method_rule(
                    class_name, "set1Value", {"idx": "int", component_name: component_type}, "None",
                    "Multifield component values are derived from field policy",
                ),
                _method_rule(
                    class_name, "setValue", {component_name: component_type}, "None",
                    "Multifield component values are derived from field policy",
                ),
            )
        )
    for class_name, value_type in multifield_single_value_types().items():
        rules.extend(
            (
                _method_rule(
                    class_name, "find", {"value": value_type, "addifnotfound": "bool"}, "int",
                    "Multifield scalar lookup is derived from field policy",
                ),
                _method_rule(
                    class_name, "set1Value", {"idx": "int", "value": value_type}, "None",
                    "Multifield scalar values are derived from field policy",
                ),
                _method_rule(
                    class_name, "__setitem__", {"i": "int", "value": value_type}, "None",
                    "Multifield scalar values are derived from field policy",
                ),
            )
        )
    for class_name in ("SoMFEngine", "SoMFNode", "SoMFPath"):
        value_type = multifield_single_value_types()[class_name]
        rules.append(
            _method_rule(
                class_name,
                "setValue",
                {"value": value_type},
                "None",
                "Nullable multifield values are accepted by setValue",
            )
        )
    return tuple(rules)


MULTIFIELD_METHOD_RULES = _multifield_method_rules()


def multifield_method_checks():
    return tuple(rule.check for rule in MULTIFIELD_METHOD_RULES)


def _parameter_types_from_text(parameters):
    if not parameters:
        return ()
    function = ast.parse("def _contract(%s): ..." % parameters).body[0]
    values = []
    positional = [*function.args.posonlyargs, *function.args.args]
    for argument in positional:
        if argument.arg in {"self", "cls"}:
            continue
        annotation = (
            ast.unparse(argument.annotation) if argument.annotation else "object"
        )
        values.append((argument.arg, annotation))
    if function.args.vararg is not None:
        argument = function.args.vararg
        annotation = ast.unparse(argument.annotation) if argument.annotation else "object"
        values.append((argument.arg, annotation))
    if function.args.kwarg is not None:
        argument = function.args.kwarg
        annotation = ast.unparse(argument.annotation) if argument.annotation else "object"
        values.append((argument.arg, annotation))
    return tuple(values)


def _python_helper_method_rules():
    return tuple(
        _method_rule(
            class_name,
            method_name,
            dict(_parameter_types_from_text(policy.parameters)),
            policy.return_type,
            "Python-owned helper signature derived from generation policy",
        )
        for (class_name, method_name), policy in PYTHON_HELPER_METHOD_POLICIES.items()
    )


PYTHON_HELPER_METHOD_RULES = _python_helper_method_rules()


def python_helper_method_checks(module):
    rules = PYTHON_HELPER_METHOD_RULES
    if module.endswith("soqt.pyi"):
        rules = tuple(
            rule for rule in rules
            if rule.target.class_name == "_SwigNonDynamicMeta"
        )
    return tuple(rule.check for rule in rules)


def _extend_helper_method_rules():
    rules = []
    for (class_name, method_name, _), (parameters, return_type) in (
        EXTEND_HELPER_METHOD_TYPES.items()
    ):
        rules.append(
            _method_rule(
                class_name,
                method_name,
                dict(_parameter_types_from_text(parameters)),
                return_type,
                "Python extension helper signature derived from generation policy",
            )
        )
    return tuple(rules)


EXTEND_HELPER_METHOD_RULES = _extend_helper_method_rules()


def extend_helper_method_checks(module):
    if module.endswith("soqt.pyi"):
        return ()
    return tuple(rule.check for rule in EXTEND_HELPER_METHOD_RULES)


METHOD_CONTRACT_RULES = (
    *SEQUENCE_METHOD_RULES,
    *TYPEDEF_AND_STRING_METHOD_RULES,
    *OPERATOR_METHOD_RULES,
    *DOCUMENTED_METHOD_RULES,
    *POINTER_HELPER_METHOD_RULES,
    *RAW_BOUNDARY_METHOD_RULES,
    *MULTIFIELD_METHOD_RULES,
    *PYTHON_HELPER_METHOD_RULES,
    *EXTEND_HELPER_METHOD_RULES,
)


def method_contracts_for_classes(class_names):
    """Return all resolved contracts whose class exists in one module."""

    return tuple(
        rule for rule in METHOD_CONTRACT_RULES
        if rule.target.class_name in class_names
    )


__all__ = [
    "POINTER_HELPER_METHOD_RULES",
    "pointer_helper_method_checks",
    "RAW_BOUNDARY_METHOD_RULES",
    "raw_boundary_method_checks",
    "RAW_BOUNDARY_ATTRIBUTE_CHECKS",
    "MULTIFIELD_METHOD_RULES",
    "multifield_method_checks",
    "PYTHON_HELPER_METHOD_RULES",
    "python_helper_method_checks",
    "EXTEND_HELPER_METHOD_RULES",
    "extend_helper_method_checks",
    "METHOD_CONTRACT_RULES",
    "method_contracts_for_classes",
]
