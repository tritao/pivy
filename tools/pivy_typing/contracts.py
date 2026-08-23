"""Binding-owned method contracts shared by generation and validation."""

from __future__ import annotations

from tools.pivy_stub_typing_policy import (
    MethodSignatureRule,
    PolicyTarget,
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


__all__ = [
    "POINTER_HELPER_METHOD_RULES",
    "pointer_helper_method_checks",
]
