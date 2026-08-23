"""Shared, declarative policy for the generated Pivy typing surface."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

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


@dataclass(frozen=True)
class PolicyTarget:
    """A binding symbol addressed by a structured typing rule."""

    class_name: str
    method_name: str
    parameter_name: str | None = None

    @property
    def key(self) -> tuple[str, ...]:
        if self.parameter_name is None:
            return (self.class_name, self.method_name)
        return (self.class_name, self.method_name, self.parameter_name)


class PolicyOwner(Enum):
    """Binding domain that owns an exceptional typing rule."""

    COIN = "coin"
    SOQT = "soqt"
    GENERIC = "generic"


def policy_owner_for_target(target: PolicyTarget) -> PolicyOwner:
    """Assign the current ownership boundary without changing semantics."""

    if target.class_name.startswith("SoQt"):
        return PolicyOwner.SOQT
    return PolicyOwner.COIN


@dataclass(frozen=True)
class OverrideRule:
    """One Python-facing override with reviewable provenance."""

    target: PolicyTarget
    python_type: object
    reason: str
    source: str = "tools/pivy_stub_typing_policy.py"
    owner: PolicyOwner = PolicyOwner.COIN


@dataclass(frozen=True)
class MethodSignatureRule:
    """One complete Python-facing method signature contract."""

    target: PolicyTarget
    parameter_types: tuple[tuple[str, str], ...]
    return_type: str
    reason: str
    source: str = "tools/pivy_stub_typing_policy.py"
    owner: PolicyOwner = PolicyOwner.COIN

    @property
    def check(self):
        """Return the legacy validator shape during the migration."""

        return (
            self.target.class_name,
            self.target.method_name,
            dict(self.parameter_types),
            self.return_type,
        )


def _rules_from_mapping(mapping, reason):
    return tuple(
        OverrideRule(
            target=PolicyTarget(*target),
            python_type=python_type,
            reason=reason,
            owner=policy_owner_for_target(PolicyTarget(*target)),
        )
        for target, python_type in mapping.items()
    )


def _mapping_from_rules(rules):
    return {rule.target.key: rule.python_type for rule in rules}


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
    "shortp": "int",
    "ushortp": "int",
    "intp": "int",
    "uintp": "int",
    "int8p": "int",
    "uint8p": "int",
    "uint32p": "int",
    "longp": "int",
    "sizep": "int",
    "timep": "int",
    "floatp": "float",
    "doublep": "float",
}
_SCALAR_POINTER_HELPER_PARAMETERS = {
    ("SoQt", "getVersionInfo", "major"): "intp",
    ("SoQt", "getVersionInfo", "minor"): "intp",
    ("SoQt", "getVersionInfo", "micro"): "intp",
}
_SCALAR_REFERENCE_HELPER_PARAMETERS = {
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
    "short": "shortp",
    "unsigned short": "ushortp",
    "unsigned int": "uintp",
    "int8_t": "int8p",
    "uint8_t": "uint8p",
    "uint32_t": "uint32p",
    "size_t": "sizep",
    "time_t": "timep",
}
_SEQUENCE_POINTER_PARAMETERS = {
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
    ("SoConvexDataCache", "generate", "coordindices"): "Sequence[int]",
    ("SoConvexDataCache", "generate", "matindices"): "Sequence[int]",
    ("SoConvexDataCache", "generate", "normindices"): "Sequence[int]",
    ("SoConvexDataCache", "generate", "texindices"): "Sequence[int]",
}
SEQUENCE_ARRAY_PARAMETERS = {
    **vector_sequence_array_parameters(),
}
_BOOL_SEQUENCE_ARRAY_PARAMETERS = {
    ("SoQtViewer", "setAnaglyphStereoColorMasks", "left"): (
        "Sequence[bool]",
        "3",
    ),
    ("SoQtViewer", "setAnaglyphStereoColorMasks", "right"): (
        "Sequence[bool]",
        "3",
    ),
}
_MATRIX_SEQUENCE_PARAMETERS = {
    ("SbDPMatrix", "__init__", "matrix"): "Sequence[Sequence[float]]",
    ("SbDPMatrix", "setValue", "m"): "Sequence[Sequence[float]]",
    ("SbMatrix", "__init__", "matrix"): "Sequence[Sequence[float]]",
    ("SbMatrix", "setValue", "m"): "Sequence[Sequence[float]]",
}
SCALAR_POINTER_HELPER_RULES = _rules_from_mapping(
    _SCALAR_POINTER_HELPER_PARAMETERS,
    "Native scalar output helper represented by a Python pointer value",
)
SCALAR_POINTER_HELPER_PARAMETERS = _mapping_from_rules(SCALAR_POINTER_HELPER_RULES)
SCALAR_REFERENCE_HELPER_RULES = _rules_from_mapping(
    _SCALAR_REFERENCE_HELPER_PARAMETERS,
    "Native scalar reference output helper represented by a Python pointer value",
)
SCALAR_REFERENCE_HELPER_PARAMETERS = _mapping_from_rules(
    SCALAR_REFERENCE_HELPER_RULES
)
SEQUENCE_POINTER_RULES = _rules_from_mapping(
    _SEQUENCE_POINTER_PARAMETERS,
    "Native array input exposed as a Python sequence",
)
SEQUENCE_POINTER_PARAMETERS = _mapping_from_rules(SEQUENCE_POINTER_RULES)
BOOL_SEQUENCE_ARRAY_RULES = _rules_from_mapping(
    _BOOL_SEQUENCE_ARRAY_PARAMETERS,
    "Fixed-width native boolean array exposed as a Python sequence",
)
BOOL_SEQUENCE_ARRAY_PARAMETERS = _mapping_from_rules(BOOL_SEQUENCE_ARRAY_RULES)
MATRIX_SEQUENCE_RULES = _rules_from_mapping(
    _MATRIX_SEQUENCE_PARAMETERS,
    "Native matrix input exposed as nested Python sequences",
)
MATRIX_SEQUENCE_PARAMETERS = _mapping_from_rules(MATRIX_SEQUENCE_RULES)
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


def _method_signature_rule(
    class_name,
    method_name,
    parameter_types,
    return_type,
    reason,
):
    target = PolicyTarget(class_name, method_name)
    return MethodSignatureRule(
        target=target,
        parameter_types=tuple(parameter_types),
        return_type=return_type,
        reason=reason,
        owner=policy_owner_for_target(target),
    )


def _sequence_method_rules():
    rules = []
    for (class_name, method_name, parameter_name), (python_type, _) in (
        SEQUENCE_ARRAY_PARAMETERS.items()
    ):
        rules.append(
            _method_signature_rule(
                class_name,
                method_name,
                ((parameter_name, python_type),),
                "None" if method_name == "__init__" else class_name,
                "Fixed-width native array exposed as a Python sequence",
            )
        )

    for class_name, python_type in SEQUENCE_VALUE_RETURN_TYPES.items():
        if class_name == "SbColor":
            # SbColor exposes getHSVValue but inherits getValue from
            # SbVec3f; the generated class body has no separate getValue
            # declaration for the validator to check.
            continue
        rules.append(
            _method_signature_rule(
                class_name,
                "getValue",
                (),
                python_type,
                "Native vector value exposed as a Python sequence",
            )
        )

    for class_name in ("SbColor", "SbColor4f"):
        rules.append(
            _method_signature_rule(
                class_name,
                "getHSVValue",
                (),
                SEQUENCE_VALUE_RETURN_TYPES[class_name],
                "Native color value exposed as a Python sequence",
            )
        )

    for class_name, python_type in MATRIX_VALUE_RETURN_TYPES.items():
        rules.append(
            _method_signature_rule(
                class_name,
                "getValue",
                (),
                python_type,
                "Native matrix value exposed as nested Python sequences",
            )
        )

    for class_name, python_type in MATRIX_ROW_RETURN_TYPES.items():
        rules.append(
            _method_signature_rule(
                class_name,
                "__getitem__",
                (("i", "int"),),
                python_type,
                "Native matrix row exposed as a Python sequence",
            )
        )

    rules.extend(
        (
            _method_signature_rule(
                "SoSFEnum",
                "setEnums",
                (
                    ("num", "int"),
                    ("vals", "Sequence[int]"),
                    ("names", "SbName | Sequence[SbName | str]"),
                ),
                "None",
                "Enum arrays exposed as Python sequences",
            ),
            _method_signature_rule(
                "SbColor",
                "setHSVValue",
                (("hsv", "Sequence[float]"),),
                "SbColor",
                "Color components exposed as a Python sequence",
            ),
            _method_signature_rule(
                "SbColor4f",
                "setHSVValue",
                (("hsv", "Sequence[float]"),),
                "SbColor4f",
                "Color components exposed as a Python sequence",
            ),
            _method_signature_rule(
                "SoMFColor",
                "setHSVValues",
                (
                    ("start", "int"),
                    ("num", "int"),
                    ("hsv", "Sequence[Sequence[float]]"),
                ),
                "None",
                "Color arrays exposed as nested Python sequences",
            ),
            _method_signature_rule(
                "SoConvexDataCache",
                "generate",
                (
                    ("coordindices", "Sequence[int]"),
                    ("matindices", "Sequence[int]"),
                    ("normindices", "Sequence[int]"),
                    ("texindices", "Sequence[int]"),
                ),
                "SbMatrix",
                "Convex-cache index arrays are copied from Python sequences",
            ),
        )
    )
    return tuple(rules)


SEQUENCE_METHOD_RULES = _sequence_method_rules()


def sequence_method_checks():
    """Return compatibility checks derived from sequence method policy."""

    return method_signature_checks(SEQUENCE_METHOD_RULES)


SEQUENCE_PARAMETER_TYPE_OVERRIDES = {
    (rule.target.class_name, rule.target.method_name, parameter_name): parameter_type
    for rule in SEQUENCE_METHOD_RULES
    for parameter_name, parameter_type in rule.parameter_types
    if rule.target.method_name not in {"__init__", "setValue", "getValue"}
}


STRING_POINTER_PARAMETERS = {
    ("SbName", "__eq__", "u"),
    ("SbName", "__nq__", "u"),
    ("SbString", "__eq__", "u"),
    ("SbString", "__nq__", "u"),
}
INPLACE_DIVISION_METHODS = {"__idiv__", "__itruediv__"}


def method_signature_checks(rules):
    """Return legacy validator tuples for structured method rules."""

    return tuple(rule.check for rule in rules)


def _typedef_and_string_method_rules():
    rules = []
    for class_name, method_name, _ in sorted(STRING_POINTER_PARAMETERS):
        rules.append(
            _method_signature_rule(
                class_name,
                method_name,
                (("u", "str"),),
                "bool" if method_name == "__eq__" else "int",
                "Native string comparison exposed as Python text",
            )
        )
    rules.extend(
        (
            _method_signature_rule(
                "SoNotList",
                "getTimeStamp",
                (),
                "int",
                "Native timestamp typedef normalized to int",
            ),
            _method_signature_rule(
                "SoNode",
                "getNodeId",
                (),
                "int",
                "Native identifier typedef normalized to int",
            ),
            _method_signature_rule(
                "SoNode",
                "getNextNodeId",
                (),
                "int",
                "Native identifier typedef normalized to int",
            ),
            _method_signature_rule(
                "SoColorPacker",
                "diffuseMatch",
                (("nodeid", "int"),),
                "bool",
                "Native identifier parameter normalized to int",
            ),
            _method_signature_rule(
                "SoColorPacker",
                "getDiffuseId",
                (),
                "int",
                "Native identifier typedef normalized to int",
            ),
        )
    )
    return tuple(rules)


TYPEDEF_AND_STRING_METHOD_RULES = _typedef_and_string_method_rules()


def typedef_and_string_method_checks():
    return method_signature_checks(TYPEDEF_AND_STRING_METHOD_RULES)


def _operator_method_rules():
    rules = []
    for class_name in (*VECTOR_TYPE_POLICIES, "SbColor4f"):
        for method_name in INPLACE_DIVISION_METHODS:
            rules.append(
                _method_signature_rule(
                    class_name,
                    method_name,
                    (("d", "float"),),
                    class_name,
                    "Binding-generated in-place scalar division operator",
                )
            )
    rules.extend(
        (
            _method_signature_rule(
                "SbTime",
                "__itruediv__",
                (("d", "float"),),
                "SbTime",
                "Binding-generated in-place time division operator",
            ),
            _method_signature_rule(
                "SbTime",
                "__truediv__",
                (("tm", "SbTime"),),
                "float",
                "Binding-generated time division overload",
            ),
            _method_signature_rule(
                "SbTime",
                "__truediv__",
                (("d", "float"),),
                "float",
                "Binding-generated time division overload",
            ),
            _method_signature_rule(
                "SbRotation",
                "__imul__",
                (("other", "SbRotation"),),
                "SbRotation",
                "Binding-generated rotation multiplication operator",
            ),
        )
    )
    return tuple(rules)


OPERATOR_METHOD_RULES = _operator_method_rules()


def operator_method_checks():
    return method_signature_checks(OPERATOR_METHOD_RULES)


DOCUMENTED_METHOD_RULES = (
    _method_signature_rule(
        "SoType",
        "getInstantiationMethod",
        (),
        "int",
        "Coin documentation identifies the instantiation method enum",
    ),
    _method_signature_rule(
        "SoVectorizeAction",
        "setColorTranslationMethod",
        (("method", "int"),),
        "None",
        "Coin documentation identifies the color translation enum",
    ),
    _method_signature_rule(
        "SoVectorizeAction",
        "getColorTranslationMethod",
        (),
        "int",
        "Coin documentation identifies the color translation enum",
    ),
    _method_signature_rule(
        "SoDepthBufferElement",
        "getFunction",
        (("state", "SoState"),),
        "int",
        "Coin documentation identifies the depth function enum",
    ),
    _method_signature_rule(
        "SoQt",
        "init",
        (
            ("argc", "intp"),
            ("argv", "Sequence[str]"),
            ("appname", "str"),
            ("classname", "str"),
        ),
        "QWidget",
        "SoQt documentation defines the application initialization contract",
    ),
    _method_signature_rule(
        "SoQtViewer",
        "setAnaglyphStereoColorMasks",
        (("left", "Sequence[bool]"), ("right", "Sequence[bool]")),
        "None",
        "SoQt documentation defines fixed-width stereo color masks",
    ),
)


def documented_method_checks(module=None):
    rules = DOCUMENTED_METHOD_RULES
    if module == "coin.pyi":
        rules = tuple(
            rule for rule in rules if not rule.target.class_name.startswith("SoQt")
        )
    elif module and module.endswith("soqt.pyi"):
        rules = tuple(
            rule for rule in rules if rule.target.class_name.startswith("SoQt")
        )
    return method_signature_checks(rules)


def _parameter_overrides_from_method_rules(rules):
    return {
        (rule.target.class_name, rule.target.method_name, parameter_name): parameter_type
        for rule in rules
        for parameter_name, parameter_type in rule.parameter_types
    }


DOCUMENTED_PARAMETER_TYPE_OVERRIDES = _parameter_overrides_from_method_rules(
    DOCUMENTED_METHOD_RULES
)
PYTHON_HELPER_METHOD_POLICIES = {
    ("_SwigNonDynamicMeta", "__setattr__"): PythonMethodPolicy(
        "cls, name: str, value: object",
        "None",
    ),
    ("SoBase", "__nonzero__"): PythonMethodPolicy("self", "bool"),
    ("SoBaseKit", "__getattr__"): PythonMethodPolicy(
        "self, name: str", "SoNode | SoField"
    ),
    ("SoBaseKit", "__setattr__"): PythonMethodPolicy(
        "self, name: str, value: object", "None"
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
    ("SoEngine", "__setattr__"): PythonMethodPolicy(
        "self, name: str, value: object", "None"
    ),
    ("SoFieldContainer", "__dir__"): PythonMethodPolicy("self", "list[str]"),
    ("SoFieldContainer", "__getattr__"): PythonMethodPolicy(
        "self, name: str", "SoField"
    ),
    ("SoFieldContainer", "__setattr__"): PythonMethodPolicy(
        "self, name: str, value: object",
        "None",
    ),
    # The native enum-reference overload is replaced by a Pivy-owned tuple
    # adapter.  Keeping the contract here makes the generated stub and the
    # structural validator agree on the Python-facing API.
    ("SoShapeHintsElement", "get"): PythonMethodPolicy(
        "state: SoState",
        "tuple[int, int, int]",
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

# Some toolkit classes are intentionally only lightly represented by SWIG.
# Keep their Python-level methods in the policy rather than editing generated
# stubs by hand.  These methods are part of the stable widget contract used by
# SoQt and SoGui, even though stubgen does not discover them from the proxy
# class declaration.
PYTHON_CLASS_METHOD_POLICIES = {
    "QEvent": {
        "accept": PythonMethodPolicy("self", "None"),
        "ignore": PythonMethodPolicy("self", "None"),
        "isAccepted": PythonMethodPolicy("self", "bool"),
        "setAccepted": PythonMethodPolicy("self, accepted: bool", "None"),
        "spontaneous": PythonMethodPolicy("self", "bool"),
        "type": PythonMethodPolicy("self", "int"),
    },
    "QWidget": {
        "show": PythonMethodPolicy("self", "None"),
        "hide": PythonMethodPolicy("self", "None"),
        "isVisible": PythonMethodPolicy("self", "bool"),
        "setVisible": PythonMethodPolicy("self, visible: bool", "None"),
        "setWindowTitle": PythonMethodPolicy("self, title: str", "None"),
        "windowTitle": PythonMethodPolicy("self", "str"),
        "resize": PythonMethodPolicy(
            "self, width: int, height: int", "None"
        ),
        "width": PythonMethodPolicy("self", "int"),
        "height": PythonMethodPolicy("self", "int"),
    },
}

# These aliases describe stable native enum domains.  They are intentionally
# small: an alias is useful only when the binding's accepted values are both
# documented and runtime-proven.  The generator applies them to constants and
# selected toolkit methods below; arbitrary integer APIs remain ``int``.
PYTHON_TYPE_ALIAS_DEFINITIONS = {
    "pivy.coin": (
        "SoDrawStyleValue = Literal[0, 1, 2, 3]",
        "SoMaterialBindingValue = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]",
        "SoComplexityValue = Literal[0, 1, 2]",
        "SoLightModelValue = Literal[0, 1]",
        "SoPickStyleValue = Literal[0, 1, 2, 3, 4, 5]",
        "SoShapeHintsOrdering = Literal[0, 1, 2]",
        "SoShapeHintsShapeType = Literal[0, 1]",
        "SoShapeHintsFaceType = Literal[0, 1]",
        "SoShapeHintsWindingType = Literal[0]",
        # Coin uses OpenGL enum values for texture model and wrap modes.
        "SoTextureModel = Literal[3042, 7681, 8448, 8449]",
        "SoTextureWrap = Literal[10496, 10497, 33069]",
        # SoGLImage has a separate wrap enum with binding-local values.
        "SoGLImageWrap = Literal[0, 1, 2, 3]",
        "SoUnitsValue = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]",
        "SoSearchFind = Literal[1, 2, 4]",
        "SoSearchInterest = Literal[0, 1, 2]",
    ),
    "pivy.gui.soqt": (
        "SoQtViewerType = Literal[0, 1]",
        "SoQtBuildFlag = Literal[0, 1, 2, 3]",
        "SoQtDrawType = Literal[0, 1]",
        "SoQtViewStyle = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
        "SoQtBufferMode = Literal[0, 1, 2]",
        "SoQtNearPlaneMode = Literal[0, 1]",
        "SoQtStereoType = Literal[0, 1, 2, 3, 4]",
    ),
}

PYTHON_ENUM_CONSTANT_TYPES = {
    "pivy.coin": {
        **{
            (class_name, constant): "SoDrawStyleValue"
            for class_name in ("SoDrawStyleElement", "SoDrawStyle")
            for constant in ("FILLED", "LINES", "POINTS", "INVISIBLE")
        },
        **{
            (class_name, constant): "SoMaterialBindingValue"
            for class_name in ("SoMaterialBindingElement", "SoMaterialBinding")
            for constant in (
                "OVERALL",
                "PER_PART",
                "PER_PART_INDEXED",
                "PER_FACE",
                "PER_FACE_INDEXED",
                "PER_VERTEX",
                "PER_VERTEX_INDEXED",
                "DEFAULT",
                "NONE",
            )
        },
        **{
            (class_name, constant): "SoComplexityValue"
            for class_name in ("SoComplexity",)
            for constant in ("OBJECT_SPACE", "SCREEN_SPACE", "BOUNDING_BOX")
        },
        **{
            (class_name, constant): "SoLightModelValue"
            for class_name in ("SoLightModel",)
            for constant in ("BASE_COLOR", "PHONG")
        },
        **{
            (class_name, constant): "SoPickStyleValue"
            for class_name in ("SoPickStyle",)
            for constant in (
                "SHAPE",
                "BOUNDING_BOX",
                "UNPICKABLE",
                "SHAPE_ON_TOP",
                "BOUNDING_BOX_ON_TOP",
                "SHAPE_FRONTFACES",
            )
        },
        **{
            ("SoShapeHints", constant): alias
            for constant, alias in (
                ("UNKNOWN_ORDERING", "SoShapeHintsOrdering"),
                ("CLOCKWISE", "SoShapeHintsOrdering"),
                ("COUNTERCLOCKWISE", "SoShapeHintsOrdering"),
                ("UNKNOWN_SHAPE_TYPE", "SoShapeHintsShapeType"),
                ("SOLID", "SoShapeHintsShapeType"),
                ("UNKNOWN_FACE_TYPE", "SoShapeHintsFaceType"),
                ("CONVEX", "SoShapeHintsFaceType"),
                ("NO_WINDING_TYPE", "SoShapeHintsWindingType"),
            )
        },
        **{
            ("SoUnits", constant): "SoUnitsValue"
            for constant in (
                "METERS",
                "CENTIMETERS",
                "MILLIMETERS",
                "MICROMETERS",
                "MICRONS",
                "NANOMETERS",
                "ANGSTROMS",
                "KILOMETERS",
                "FEET",
                "INCHES",
                "POINTS",
                "YARDS",
                "MILES",
                "NAUTICAL_MILES",
            )
        },
        **{
            ("SoSearchAction", constant): "SoSearchFind"
            for constant in ("NODE", "TYPE", "NAME")
        },
        **{
            ("SoSearchAction", constant): "SoSearchInterest"
            for constant in ("FIRST", "LAST", "ALL")
        },
        **{
            (class_name, constant): "SoTextureModel"
            for class_name in (
                "SoTexture2",
                "SoTexture3",
                "SoMultiTextureImageElement",
            )
            for constant in ("MODULATE", "DECAL", "BLEND", "REPLACE")
            if not (class_name == "SoTexture3" and constant == "REPLACE")
        },
        **{
            (class_name, constant): "SoTextureWrap"
            for class_name in (
                "SoTexture2",
                "SoTexture3",
                "SoMultiTextureImageElement",
            )
            for constant in ("REPEAT", "CLAMP", "CLAMP_TO_BORDER")
            if not (
                class_name in ("SoTexture2", "SoTexture3")
                and constant == "CLAMP_TO_BORDER"
            )
        },
        **{
            ("SoGLImage", constant): "SoGLImageWrap"
            for constant in ("REPEAT", "CLAMP", "CLAMP_TO_EDGE", "CLAMP_TO_BORDER")
        },
    },
    "pivy.gui.soqt": {
        ("SoQtPlaneViewer", "BROWSER"): "SoQtViewerType",
        ("SoQtPlaneViewer", "EDITOR"): "SoQtViewerType",
        ("SoQtViewer", "BROWSER"): "SoQtViewerType",
        ("SoQtViewer", "EDITOR"): "SoQtViewerType",
        **{
            ("SoQtFullViewer", constant): "SoQtBuildFlag"
            for constant in (
                "BUILD_NONE",
                "BUILD_DECORATION",
                "BUILD_POPUP",
                "BUILD_ALL",
            )
        },
        **{
            ("SoQtViewer", constant): "SoQtViewStyle"
            for constant in (
                "VIEW_AS_IS",
                "VIEW_HIDDEN_LINE",
                "VIEW_NO_TEXTURE",
                "VIEW_LOW_COMPLEXITY",
                "VIEW_LINE",
                "VIEW_POINT",
                "VIEW_BBOX",
                "VIEW_LOW_RES_LINE",
                "VIEW_LOW_RES_POINT",
                "VIEW_SAME_AS_STILL",
                "VIEW_WIREFRAME_OVERLAY",
            )
        },
        ("SoQtViewer", "STILL"): "SoQtDrawType",
        ("SoQtViewer", "INTERACTIVE"): "SoQtDrawType",
        ("SoQtViewer", "BUFFER_SINGLE"): "SoQtBufferMode",
        ("SoQtViewer", "BUFFER_DOUBLE"): "SoQtBufferMode",
        ("SoQtViewer", "BUFFER_INTERACTIVE"): "SoQtBufferMode",
        ("SoQtViewer", "VARIABLE_NEAR_PLANE"): "SoQtNearPlaneMode",
        ("SoQtViewer", "CONSTANT_NEAR_PLANE"): "SoQtNearPlaneMode",
        ("SoQtViewer", "STEREO_NONE"): "SoQtStereoType",
        ("SoQtViewer", "STEREO_ANAGLYPH"): "SoQtStereoType",
        ("SoQtViewer", "STEREO_QUADBUFFER"): "SoQtStereoType",
        ("SoQtViewer", "STEREO_INTERLEAVED_ROWS"): "SoQtStereoType",
        ("SoQtViewer", "STEREO_INTERLEAVED_COLUMNS"): "SoQtStereoType",
    },
}
_METHOD_RETURN_TYPE_OVERRIDES = {
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
    # SWIG materializes Coin's const-reference matrix parameter as an owned
    # Python result for this existing binding method.
    ("SoConvexDataCache", "generate"): "SbMatrix",
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
    ("SoMultiTextureImageElement", "getModel"): "SoTextureModel",
    ("SoMultiTextureImageElement", "getWrapS"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "getWrapT"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "getWrapR"): "SoTextureWrap",
    ("SoGLImage", "getWrapS"): "SoGLImageWrap",
    ("SoGLImage", "getWrapT"): "SoGLImageWrap",
    ("SoGLImage", "getWrapR"): "SoGLImageWrap",
    # These adapter return types were formerly repeated in the validator's
    # handwritten structural-check table.  Keep them in the canonical policy
    # so generation and validation cannot silently diverge.
    ("SbByteBuffer", "data"): "bytes",
    ("SbBox2i32", "getBounds"): "tuple[int, int, int, int]",
    ("SbBox2i32", "getOrigin"): "tuple[int, int]",
    ("SbBox2s", "getBounds"): "tuple[int, int, int, int]",
    ("SbBox2s", "getOrigin"): "tuple[int, int]",
    ("SbBox2s", "getSize"): "SbVec2s",
    ("SbBox3i32", "getBounds"): "tuple[int, int, int, int, int, int]",
    ("SbBox3i32", "getOrigin"): "tuple[int, int, int]",
    ("SbBox3s", "getBounds"): "tuple[int, int, int, int, int, int]",
    ("SbBox3s", "getOrigin"): "tuple[int, int, int]",
    ("SbBox3s", "getSize"): "SbVec3s",
    ("SoCallbackAction", "getTextureImage2dValue"): (
        "tuple[bytes | None, SbVec2s, int]"
    ),
    ("SoCallbackAction", "getTextureImage3dValue"): (
        "tuple[bytes | None, SbVec3s, int]"
    ),
    ("SoEngine", "getOutputNameValue"): "tuple[bool, str]",
    ("SoSFImage", "getSubTextureValue"): (
        "tuple[bytes | None, SbVec2s, SbVec2s, int]"
    ),
}

METHOD_RETURN_RULES = tuple(
    OverrideRule(
        target=PolicyTarget(class_name, method_name),
        python_type=python_type,
        reason="Python-facing return type for a binding-specific API surface",
        owner=policy_owner_for_target(PolicyTarget(class_name, method_name)),
    )
    for (class_name, method_name), python_type in _METHOD_RETURN_TYPE_OVERRIDES.items()
)
METHOD_RETURN_TYPE_OVERRIDES = {
    rule.target.key: rule.python_type for rule in METHOD_RETURN_RULES
}

_PYTHON_PARAMETER_TYPE_OVERRIDES = {
    ("SoSFImage", "setValue", "pixels"): "str | bytes",
    ("SoSFImage3", "setValue", "bytes"): "str | bytes",
    ("SoSFImage3", "setValue", "pixels"): "str | bytes",
    ("SoSFEnum", "setEnums", "vals"): "Sequence[int]",
    ("SoSFEnum", "setEnums", "names"): "SbName | Sequence[SbName | str]",
    ("SoQtRenderArea", "setEventCallback", "user"): "object",
    # SoSensor stores and returns an arbitrary Python callback payload.  The
    # getter is already object-valued; keep the setter symmetric.
    ("SoSensor", "setData", "callbackdata"): "object",
    # Texture image APIs use two distinct native enum domains: Coin's
    # OpenGL-backed texture modes/wraps and SoGLImage's local wrap values.
    ("SoMultiTextureImageElement", "setElt", "wrapS"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "setElt", "wrapT"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "setElt", "wrapR"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "setElt", "model"): "SoTextureModel",
    ("SoMultiTextureImageElement", "set", "wrapS"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "set", "wrapT"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "set", "wrapR"): "SoTextureWrap",
    ("SoMultiTextureImageElement", "set", "model"): "SoTextureModel",
    ("SoGLMultiTextureImageElement", "set", "model"): "SoTextureModel",
    ("SoGLImage", "setGLDisplayList", "wraps"): "SoGLImageWrap",
    ("SoGLImage", "setGLDisplayList", "wrapt"): "SoGLImageWrap",
    ("SoGLImage", "setPBuffer", "wraps"): "SoGLImageWrap",
    ("SoGLImage", "setPBuffer", "wrapt"): "SoGLImageWrap",
    ("SoGLImage", "setData", "wraps"): "SoGLImageWrap",
    ("SoGLImage", "setData", "wrapt"): "SoGLImageWrap",
    ("SoGLImage", "setData", "wrapr"): "SoGLImageWrap",
    **SEQUENCE_PARAMETER_TYPE_OVERRIDES,
    **DOCUMENTED_PARAMETER_TYPE_OVERRIDES,
}
PYTHON_PARAMETER_RULES = tuple(
    OverrideRule(
        target=PolicyTarget(class_name, method_name, parameter_name),
        python_type=python_type,
        reason="Python-facing parameter type for a binding-specific API surface",
        owner=policy_owner_for_target(
            PolicyTarget(class_name, method_name, parameter_name)
        ),
    )
    for (class_name, method_name, parameter_name), python_type
    in _PYTHON_PARAMETER_TYPE_OVERRIDES.items()
)
PYTHON_PARAMETER_TYPE_OVERRIDES = {
    rule.target.key: rule.python_type for rule in PYTHON_PARAMETER_RULES
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
        "SoSensorCallback[SoSensor, object] | None",
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
        "SoCallbackListCallback",
        ("SoCallbackList",),
        "_CallbackDataT = TypeVar(\"_CallbackDataT\", contravariant=True)\n"
        "\n"
        "class SoCallbackListCallback(Protocol[_CallbackDataT]):\n"
        "    def __call__(\n"
        "        self, data: _CallbackDataT, callbackdata: object, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoCallbackListAPI",
        ("SoCallbackList",),
        "class SoCallbackListAPI(Protocol[_CallbackDataT]):\n"
        "    def addCallback(\n"
        "        self, f: SoCallbackListCallback[_CallbackDataT], "
        "userData: _CallbackDataT | None = ..., /\n"
        "    ) -> None: ...\n"
        "    def removeCallback(\n"
        "        self, f: SoCallbackListCallback[_CallbackDataT], "
        "userdata: _CallbackDataT | None = ..., /\n"
        "    ) -> None: ...\n"
        "    def clearCallbacks(self) -> None: ...\n"
        "    def getNumCallbacks(self) -> int: ...\n"
        "    def invokeCallbacks(self, callbackdata: object, /) -> None: ...",
    ),
    (
        "SoContextDestructionCallback",
        ("SoContextHandler",),
        "class SoContextDestructionCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, contextid: int, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoDBProgressCallback",
        ("SbName", "SoDB"),
        "_ProgressDataT = TypeVar(\"_ProgressDataT\", contravariant=True)\n"
        "\n"
        "class SoDBProgressCallback(Protocol[_ProgressDataT]):\n"
        "    def __call__(\n"
        "        self, data: _ProgressDataT, itemid: SbName, fraction: float,\n"
        "        interruptible: bool, /\n"
        "    ) -> bool: ...",
    ),
    (
        "SoSensorCallback",
        ("SoSensor",),
        "_SensorT = TypeVar(\"_SensorT\", bound=SoSensor, contravariant=True)\n"
        "_SensorDataT = TypeVar(\"_SensorDataT\", contravariant=True)\n"
        "\n"
        "class SoSensorCallback(Protocol[_SensorT, _SensorDataT]):\n"
        "    def __call__(\n"
        "        self, data: _SensorDataT, sensor: _SensorT, /\n"
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
        "SoSensorManagerChangedCallback",
        (),
        "class SoSensorManagerChangedCallback(Protocol):\n"
        "    def __call__(self, data: object, /) -> None: ...",
    ),
    (
        "SoDBHeaderCallback",
        ("SoInput",),
        "class SoDBHeaderCallback(Protocol):\n"
        "    def __call__(self, data: object, input: SoInput, /) -> None: ...",
    ),
    (
        "SoGLSortedObjectOrderCallback",
        ("SoGLRenderAction",),
        "class SoGLSortedObjectOrderCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoGLRenderAction, /\n"
        "    ) -> float: ...",
    ),
    (
        "SoGLImageEndFrameCallback",
        (),
        "class SoGLImageEndFrameCallback(Protocol):\n"
        "    def __call__(self, data: object, /) -> None: ...",
    ),
    (
        "SoShaderEnableCallback",
        ("SoState",),
        "class SoShaderEnableCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, state: SoState, enable: bool, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoProtoFetchExternProtoCallback",
        ("SoInput", "SoProto", "SbString"),
        "class SoProtoFetchExternProtoCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, input: SoInput, urls: list[SbString],\n"
        "        numurls: int, /\n"
        "    ) -> SoProto | None: ...",
    ),
    (
        "SbImageReadImageCallback",
        ("SbImage", "SbString"),
        "class SbImageReadImageCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, filename: SbString, image: SbImage, /\n"
        "    ) -> bool: ...",
    ),
    (
        "ScXMLStateMachineDeleteCallback",
        ("ScXMLStateMachine",),
        "class ScXMLStateMachineDeleteCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, machine: ScXMLStateMachine, /\n"
        "    ) -> None: ...",
    ),
    (
        "ScXMLStateChangeCallback",
        ("ScXMLStateMachine",),
        "class ScXMLStateChangeCallback(Protocol):\n"
        "    def __call__(\n"
        "        self,\n"
        "        data: object,\n"
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
        "    def __setattr__(self, name: str, value: object) -> None: ...\n"
        "    def __dir__(self) -> list[str]: ...\n"
        "    def getField(self, name: SbName | str) -> SoField | None: ...\n"
        "    def getEventIn(self, name: SbName | str) -> SoField | None: ...\n"
        "    def getEventOut(self, name: SbName | str) -> SoField | None: ...",
    ),
    (
        "SoBaseAccess",
        ("SoBase", "SoType"),
        "class SoBaseAccess(Protocol):\n"
        "    def ref(self) -> None: ...\n"
        "    def unref(self) -> None: ...\n"
        "    def unrefNoDelete(self) -> None: ...\n"
        "    def getRefCount(self) -> int: ...\n"
        "    def getTypeId(self) -> SoType: ...\n"
        "    def isOfType(self, type: SoType) -> bool: ...",
    ),
    (
        "SoFieldAccess",
        ("SoField", "SoFieldContainer", "SoFieldList"),
        "class SoFieldAccess(Protocol):\n"
        "    def getContainer(self) -> SoFieldContainer: ...\n"
        "    def getNumConnections(self) -> int: ...\n"
        "    def getConnections(self, masterlist: SoFieldList) -> int: ...\n"
        "    def getForwardConnections(self, slavelist: SoFieldList) -> int: ...",
    ),
    (
        "SoSingleFieldReader",
        ("SoSField",),
        "_SoFieldValueT_co = TypeVar(\"_SoFieldValueT_co\", covariant=True)\n"
        "\n"
        "class SoSingleFieldReader(Protocol[_SoFieldValueT_co]):\n"
        "    def getValue(self) -> _SoFieldValueT_co: ...",
    ),
    (
        "SoMultiFieldReader",
        ("SoMField",),
        "_SoMultiFieldValueT_co = TypeVar(\"_SoMultiFieldValueT_co\", covariant=True)\n"
        "\n"
        "class SoMultiFieldReader(Protocol[_SoMultiFieldValueT_co]):\n"
        "    def __len__(self) -> int: ...\n"
        "    def __iter__(self) -> Iterator[_SoMultiFieldValueT_co]: ...\n"
        "    def getValuesSnapshot(self) -> list[_SoMultiFieldValueT_co]: ...",
    ),
    (
        "SoNodeAccess",
        ("SoNode", "SoType"),
        "class SoNodeAccess(Protocol):\n"
        "    def getNodeType(self) -> int: ...\n"
        "    def setNodeType(self, type: int) -> None: ...\n"
        "    def affectsState(self) -> bool: ...\n"
        "    def isOfType(self, type: SoType) -> bool: ...",
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
    (
        "SoCallbackActionNodeCallback",
        ("SoCallbackAction", "SoNode"),
        "class SoCallbackActionNodeCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction, node: SoNode, /\n"
        "    ) -> int: ...",
    ),
    (
        "SoActionCallback",
        ("SoAction",),
        "class SoActionCallback(Protocol):\n"
        "    def __call__(self, data: object, action: SoAction, /) -> None: ...",
    ),
    (
        "SoDraggerCallback",
        ("SoDragger",),
        "_DraggerDataT = TypeVar(\"_DraggerDataT\", contravariant=True)\n"
        "\n"
        "class SoDraggerCallback(Protocol[_DraggerDataT]):\n"
        "    def __call__(\n"
        "        self, data: _DraggerDataT, dragger: SoDragger, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoEventCallbackHandler",
        ("SoEventCallback",),
        "class SoEventCallbackHandler(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, eventcallback: SoEventCallback, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoGLPreRenderCallback",
        ("SoGLRenderAction",),
        "class SoGLPreRenderCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoGLRenderAction, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoGLRenderAbortCallback",
        (),
        "class SoGLRenderAbortCallback(Protocol):\n"
        "    def __call__(self, data: object, /) -> int: ...",
    ),
    (
        "SoGLRenderPassCallback",
        (),
        "class SoGLRenderPassCallback(Protocol):\n"
        "    def __call__(self, data: object, /) -> None: ...",
    ),
    (
        "SoIntersectionCallback",
        ("SoIntersectingPrimitive",),
        "class SoIntersectionCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, first: SoIntersectingPrimitive,\n"
        "        second: SoIntersectingPrimitive, /\n"
        "    ) -> int: ...",
    ),
    (
        "SoIntersectionFilterCallback",
        ("SoPath",),
        "class SoIntersectionFilterCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, first: SoPath, second: SoPath, /\n"
        "    ) -> bool: ...",
    ),
    (
        "SoIntersectionVisitationCallback",
        ("SoPath",),
        "class SoIntersectionVisitationCallback(Protocol):\n"
        "    def __call__(self, data: object, path: SoPath, /) -> int: ...",
    ),
    (
        "SoLineSegmentCallback",
        ("SoCallbackAction", "SoPrimitiveVertex"),
        "class SoLineSegmentCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction,\n"
        "        first: SoPrimitiveVertex, second: SoPrimitiveVertex, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoPointCallback",
        ("SoCallbackAction", "SoPrimitiveVertex"),
        "class SoPointCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction,\n"
        "        vertex: SoPrimitiveVertex, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoRenderManagerCallback",
        ("SoRenderManager",),
        "class SoRenderManagerCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, manager: SoRenderManager, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoSceneManagerCallback",
        ("SoSceneManager",),
        "class SoSceneManagerCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, manager: SoSceneManager, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoSelectionClassCallback",
        ("SoSelection",),
        "_SelectionClassDataT = TypeVar(\"_SelectionClassDataT\", contravariant=True)\n"
        "\n"
        "class SoSelectionClassCallback(Protocol[_SelectionClassDataT]):\n"
        "    def __call__(\n"
        "        self, data: _SelectionClassDataT, selection: SoSelection, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoSelectionPathCallback",
        ("SoPath",),
        "_SelectionPathDataT = TypeVar(\"_SelectionPathDataT\", contravariant=True)\n"
        "\n"
        "class SoSelectionPathCallback(Protocol[_SelectionPathDataT]):\n"
        "    def __call__(self, data: _SelectionPathDataT, path: SoPath, /) -> None: ...",
    ),
    (
        "SoSelectionPickCallback",
        ("SoPath", "SoPickedPoint"),
        "_SelectionPickDataT = TypeVar(\"_SelectionPickDataT\", contravariant=True)\n"
        "\n"
        "class SoSelectionPickCallback(Protocol[_SelectionPickDataT]):\n"
        "    def __call__(\n"
        "        self, data: _SelectionPickDataT, point: SoPickedPoint, /\n"
        "    ) -> SoPath: ...",
    ),
    (
        "SoTriangleCallback",
        ("SoCallbackAction", "SoPrimitiveVertex"),
        "class SoTriangleCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction,\n"
        "        first: SoPrimitiveVertex, second: SoPrimitiveVertex,\n"
        "        third: SoPrimitiveVertex, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoExtSelectionLassoFilterCallback",
        ("SoPath",),
        "class SoExtSelectionLassoFilterCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, path: SoPath, /\n"
        "    ) -> SoPath | None: ...",
    ),
    (
        "SoExtSelectionTriangleFilterCallback",
        ("SoCallbackAction", "SoPrimitiveVertex"),
        "class SoExtSelectionTriangleFilterCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction,\n"
        "        first: SoPrimitiveVertex, second: SoPrimitiveVertex,\n"
        "        third: SoPrimitiveVertex, /\n"
        "    ) -> bool: ...",
    ),
    (
        "SoExtSelectionLineSegmentFilterCallback",
        ("SoCallbackAction", "SoPrimitiveVertex"),
        "class SoExtSelectionLineSegmentFilterCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction,\n"
        "        first: SoPrimitiveVertex, second: SoPrimitiveVertex, /\n"
        "    ) -> bool: ...",
    ),
    (
        "SoExtSelectionPointFilterCallback",
        ("SoCallbackAction", "SoPrimitiveVertex"),
        "class SoExtSelectionPointFilterCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, action: SoCallbackAction,\n"
        "        vertex: SoPrimitiveVertex, /\n"
        "    ) -> bool: ...",
    ),
    (
        "SoQtRenderAreaCallback",
        ("QEvent",),
        "class SoQtRenderAreaCallback(Protocol):\n"
        "    def __call__(self, data: object, event: QEvent, /) -> object: ...",
    ),
    (
        "SoQtFatalErrorCallback",
        ("SbString",),
        "class SoQtFatalErrorCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, message: SbString, line: int, data: object, /\n"
        "    ) -> None: ...",
    ),
    (
        "SoQtAutoClippingCallback",
        ("SbVec2f",),
        "class SoQtAutoClippingCallback(Protocol):\n"
        "    def __call__(\n"
        "        self, data: object, value: SbVec2f, /\n"
        "    ) -> SbVec2f: ...",
    ),
    (
        "SoQtMenuSelectionCallback",
        (),
        "class SoQtMenuSelectionCallback(Protocol):\n"
        "    def __call__(self, menu_id: int, data: object, /) -> None: ...",
    ),
)
# Protocols belong to the module that owns the binding surface, even when
# their arguments are classes imported from the sibling stub.
PYTHON_PROTOCOL_MODULES = {
    name: "pivy.gui.soqt" if name.startswith("SoQt") else "pivy.coin"
    for name, _, _ in PYTHON_PROTOCOL_DEFINITIONS
}
CALLBACK_TYPE_SIGNATURES = {
    "ScXMLStateChangeCB": "ScXMLStateChangeCallback",
    "ScXMLStateMachineDeleteCB": "ScXMLStateMachineDeleteCallback",
    "SoCallbackAction::SoCallbackActionCB": "SoCallbackActionNodeCallback",
    "SoCallbackCB": "SoActionCallback",
    "SoDraggerCB": "SoDraggerCallback",
    "SoEventCallbackCB": "SoEventCallbackHandler",
    "SoGLPreRenderCB": "SoGLPreRenderCallback",
    "SoGLRenderAction::SoGLRenderAbortCB": "SoGLRenderAbortCallback",
    "SoGLRenderPassCB": "SoGLRenderPassCallback",
    "SoIntersectionDetectionAction::SoIntersectionCB": "SoIntersectionCallback",
    "SoIntersectionDetectionAction::SoIntersectionFilterCB": "SoIntersectionFilterCallback",
    "SoIntersectionDetectionAction::SoIntersectionVisitationCB": "SoIntersectionVisitationCallback",
    "SoLineSegmentCB": "SoLineSegmentCallback",
    "SoPointCB": "SoPointCallback",
    "SoRenderManagerRenderCB": "SoRenderManagerCallback",
    "SoSceneManagerRenderCB": "SoSceneManagerCallback",
    "SoSelectionClassCB": "SoSelectionClassCallback[object]",
    "SoSelectionPathCB": "SoSelectionPathCallback[object]",
    "SoSelectionPickCB": "SoSelectionPickCallback[object]",
    "SoTriangleCB": (
        "SoTriangleCallback"
    ),
    "SoSensorManagerChangedCB": "SoSensorManagerChangedCallback",
    "SoDBHeaderCB": "SoDBHeaderCallback",
    "SoGLSortedObjectOrderCB": "SoGLSortedObjectOrderCallback",
    "SoGLImageEndFrameCB": "SoGLImageEndFrameCallback",
    "SoShaderEnableCB": "SoShaderEnableCallback",
    "SoProtoFetchExternProtoCB": "SoProtoFetchExternProtoCallback",
    "SbImageReadImageCB": "SbImageReadImageCallback",
    "SoSensorCB": "SoSensorCallback[SoSensor, object]",
    "SoErrorCB": "SoErrorCallback",
    "SoQtRenderAreaEventCB": "SoQtRenderAreaCallback",
    "SoQtFatalErrorCB": "SoQtFatalErrorCallback",
    "SoQtComponentCB": "SoQtComponentCallback",
    "SoQtViewerCB": "SoQtViewerCallback",
    "SoQtAutoClippingCB": "SoQtAutoClippingCallback",
    "SoQtMenuSelectionCallback": "SoQtMenuSelectionCallback",
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
    ("SoSensorManager", "setChangedCallback"): CallbackMethodPolicy(
        (
            ("pyfunc", "SoSensorManagerChangedCallback"),
            ("data", "object"),
        ),
        (
            "self, pyfunc: SoSensorManagerChangedCallback, data: object",
            "None",
        ),
    ),
    ("SoDB", "registerHeader"): CallbackMethodPolicy(
        (
            ("precallback", "SoDBHeaderCallback"),
            ("postcallback", "SoDBHeaderCallback"),
            ("userdata", "object | None"),
        ),
        (
            "headerstring: SbString, isbinary: bool, ivversion: float, "
            "precallback: SoDBHeaderCallback, "
            "postcallback: SoDBHeaderCallback, "
            "userdata: object | None = ...",
            "bool",
        ),
    ),
    ("SoQt", "setFatalErrorHandler"): CallbackMethodPolicy(
        (
            ("cb", "SoQtFatalErrorCallback"),
            ("userdata", "object"),
        ),
        (
            "cb: SoQtFatalErrorCallback, "
            "userdata: object",
            "SoQtFatalErrorCallback | None",
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
            ("cb", "SoQtAutoClippingCallback | None"),
            ("cbuserdata", "object | None"),
        ),
        (
            "self, strategy: SoQtNearPlaneMode, value: float = ..., "
            "cb: SoQtAutoClippingCallback | None = ..., "
            "cbuserdata: object | None = ...",
            "None",
        ),
    ),
    ("SoQtPopupMenu", "addMenuSelectionCallback"): CallbackMethodPolicy(
        (
            ("callback", "SoQtMenuSelectionCallback"),
            ("data", "object"),
        ),
        (
            "self, callback: SoQtMenuSelectionCallback, data: object",
            "None",
        ),
    ),
    ("SoQtPopupMenu", "removeMenuSelectionCallback"): CallbackMethodPolicy(
        (
            ("callback", "SoQtMenuSelectionCallback"),
            ("data", "object"),
        ),
        (
            "self, callback: SoQtMenuSelectionCallback, data: object",
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
            ("f", "SoCallbackListCallback[object]"),
            ("userData", "object | None"),
        ),
        (
            "self, f: SoCallbackListCallback[object], "
            "userData: object | None = ...",
            "None",
        ),
    ),
    ("SoCallbackList", "removeCallback"): CallbackMethodPolicy(
        (
            ("f", "SoCallbackListCallback[object]"),
            ("userdata", "object | None"),
        ),
        (
            "self, f: SoCallbackListCallback[object], "
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
            ("func", "SoContextDestructionCallback"),
            ("userdata", "object | None"),
        ),
        (
            "func: SoContextDestructionCallback, userdata: object | None = ...",
            "None",
        ),
    ),
    ("SoContextHandler", "removeContextDestructionCallback"): CallbackMethodPolicy(
        (
            ("func", "SoContextDestructionCallback"),
            ("userdata", "object | None"),
        ),
        (
            "func: SoContextDestructionCallback, userdata: object | None = ...",
            "None",
        ),
    ),
    ("SoGLRenderAction", "setSortedObjectOrderStrategy"): CallbackMethodPolicy(
        (
            ("cb", "SoGLSortedObjectOrderCallback | None"),
            ("closure", "object | None"),
        ),
        (
            "self, strategy: int, "
            "cb: SoGLSortedObjectOrderCallback | None = ..., "
            "closure: object | None = ...",
            "None",
        ),
        (
            ("strategy", "int"),
            ("cb", "SoGLSortedObjectOrderCallback | None"),
            ("closure", "object | None"),
        ),
    ),
    ("SoGLCacheContextElement", "scheduleDeleteCallback"): CallbackMethodPolicy(
        (
            ("cb", "SoContextDestructionCallback"),
            ("closure", "object | None"),
        ),
        (
            "contextid: int, "
            "cb: SoContextDestructionCallback, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SoGLImage", "setEndFrameCallback"): CallbackMethodPolicy(
        (
            ("cb", "SoGLImageEndFrameCallback | None"),
            ("closure", "object | None"),
        ),
        (
            "self, cb: SoGLImageEndFrameCallback | None, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SoShaderProgram", "setEnableCallback"): CallbackMethodPolicy(
        (
            ("cb", "SoShaderEnableCallback | None"),
            ("closure", "object | None"),
        ),
        (
            "self, cb: SoShaderEnableCallback | None, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SoProto", "setFetchExternProtoCallback"): CallbackMethodPolicy(
        (
            ("cb", "SoProtoFetchExternProtoCallback | None"),
            ("closure", "object | None"),
        ),
        (
            "cb: SoProtoFetchExternProtoCallback | None, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SbImage", "addReadImageCB"): CallbackMethodPolicy(
        (
            ("cb", "SbImageReadImageCallback"),
            ("closure", "object | None"),
        ),
        (
            "cb: SbImageReadImageCallback, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SbImage", "removeReadImageCB"): CallbackMethodPolicy(
        (
            ("cb", "SbImageReadImageCallback"),
            ("closure", "object | None"),
        ),
        (
            "cb: SbImageReadImageCallback, "
            "closure: object | None = ...",
            "None",
        ),
    ),
    ("SbImage", "scheduleReadFile"): CallbackMethodPolicy(
        (
            ("cb", "SbImageReadImageCallback"),
            ("closure", "object | None"),
        ),
        (
            "self, cb: SbImageReadImageCallback, "
            "closure: object | None, filename: SbString, "
            "searchdirectories: SbString | None = ..., "
            "numdirectories: int = ...",
            "bool",
        ),
        (
            ("cb", "SbImageReadImageCallback"),
            ("closure", "object | None"),
            ("filename", "SbString"),
            ("searchdirectories", "SbString | None"),
            ("numdirectories", "int"),
        ),
    ),
    ("SoDB", "addProgressCallback"): CallbackMethodPolicy(
        (
            ("func", "SoDBProgressCallback[_ProgressDataT]"),
            ("userdata", "_ProgressDataT | None"),
        ),
        (
            "func: SoDBProgressCallback[_ProgressDataT], "
            "userdata: _ProgressDataT | None",
            "None",
        ),
    ),
    ("SoDB", "removeProgressCallback"): CallbackMethodPolicy(
        (
            ("func", "SoDBProgressCallback[_ProgressDataT]"),
            ("userdata", "_ProgressDataT | None"),
        ),
        (
            "func: SoDBProgressCallback[_ProgressDataT], "
            "userdata: _ProgressDataT | None",
            "None",
        ),
    ),
    ("SoSensor", "setFunction"): CallbackMethodPolicy(
        (("callbackfunction", "SoSensorCallback[SoSensor, _SensorDataT]"),),
        (
            "self, callbackfunction: SoSensorCallback[SoSensor, _SensorDataT]",
            "None",
        ),
    ),
    ("SoDataSensor", "setDeleteCallback"): CallbackMethodPolicy(
        (
            ("function", "SoSensorCallback[SoSensor, _SensorDataT]"),
            ("data", "_SensorDataT | None"),
        ),
        (
            "self, function: SoSensorCallback[SoSensor, _SensorDataT], "
            "data: _SensorDataT | None = ...",
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
                ("pyfunc", "SoDraggerCallback[_DraggerDataT]"),
                ("data", "_DraggerDataT | None"),
            ),
            (
                "self, pyfunc: SoDraggerCallback[_DraggerDataT], "
                "data: _DraggerDataT | None = ...",
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
                ("pyfunc", "SoSelectionPathCallback[_SelectionPathDataT]"),
                ("userdata", "_SelectionPathDataT | None"),
            ),
            (
                "self, pyfunc: SoSelectionPathCallback[_SelectionPathDataT], "
                "userdata: _SelectionPathDataT | None = ...",
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
                ("pyfunc", "SoSelectionClassCallback[_SelectionClassDataT]"),
                ("userdata", "_SelectionClassDataT | None"),
            ),
            (
                "self, pyfunc: SoSelectionClassCallback[_SelectionClassDataT], "
                "userdata: _SelectionClassDataT | None = ...",
                "None",
            ),
        )
    )

CALLBACK_METHOD_POLICIES[("SoSelection", "setPickFilterCallback")] = (
    CallbackMethodPolicy(
        (
            ("pyfunc", "SoSelectionPickCallback[_SelectionPickDataT]"),
            ("userdata", "_SelectionPickDataT | None"),
        ),
        (
            "self, pyfunc: SoSelectionPickCallback[_SelectionPickDataT], "
            "userdata: _SelectionPickDataT | None = ..., "
            "callOnlyIfSelectable: int = ...",
            "None",
        ),
        (
            ("pyfunc", "SoSelectionPickCallback[_SelectionPickDataT]"),
            ("userdata", "_SelectionPickDataT | None"),
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
                    "SoExtSelectionLassoFilterCallback | None",
                ),
                ("userdata", "object | None"),
                ("callonlyifselectable", "bool"),
            ),
            (
                "self, f: SoExtSelectionLassoFilterCallback | None, "
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
                    "SoExtSelectionTriangleFilterCallback | None",
                ),
                ("userdata", "object | None"),
            ),
            (
                "self, func: SoExtSelectionTriangleFilterCallback | None, "
                "userdata: object | None = ...",
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
                    "SoExtSelectionLineSegmentFilterCallback | None",
                ),
                ("userdata", "object | None"),
            ),
            (
                "self, func: SoExtSelectionLineSegmentFilterCallback | None, "
                "userdata: object | None = ...",
                "None",
            ),
        ),
        ("SoExtSelection", "setPointFilterCallback"): CallbackMethodPolicy(
            (
                (
                    "func",
                    "SoExtSelectionPointFilterCallback | None",
                ),
                ("userdata", "object | None"),
            ),
            (
                "self, func: SoExtSelectionPointFilterCallback | None, "
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
PYTHON_SHADOW_METHOD_TYPES[("SoMFDouble", "getValues")] = (
    "self, start: int = ...",
    "list[float]",
)
PYTHON_SHADOW_METHOD_TYPES[("SoMFDouble", "getValuesSnapshot")] = (
    "self",
    "list[float]",
)
PYTHON_SHADOW_METHOD_TYPES[("SoMFDouble", "__setitem__")] = (
    "self, index: int, value: float",
    "None",
)
for _scxml_factory_class in (
    "ScXMLInExprDataObj",
    "ScXMLAppendOpExprDataObj",
    "ScXMLScriptElt",
):
    PYTHON_SHADOW_METHOD_TYPES[(_scxml_factory_class, "createInstance")] = (
        "",
        _scxml_factory_class,
    )
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
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "setDrawStyle")] = (
    "self, type: SoQtDrawType, style: SoQtViewStyle",
    "None",
)
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "getDrawStyle")] = (
    "self, type: SoQtDrawType",
    "SoQtViewStyle",
)
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "setBufferingType")] = (
    "self, type: SoQtBufferMode",
    "None",
)
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "getBufferingType")] = (
    "self",
    "SoQtBufferMode",
)
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "setStereoType")] = (
    "self, s: SoQtStereoType",
    "bool",
)
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "getStereoType")] = (
    "self",
    "SoQtStereoType",
)
PYTHON_SHADOW_METHOD_TYPES[("SoQtViewer", "setAutoClippingStrategy")] = (
    "self, strategy: SoQtNearPlaneMode, value: float = ..., "
    "cb: SoQtAutoClippingCallback | None = ..., "
    "cbuserdata: object | None = ...",
    "None",
)
for _soqt_constructor_class in (
    "SoQtPlaneViewer",
    "SoQtExaminerViewer",
    "SoQtFlyViewer",
):
    PYTHON_SHADOW_METHOD_TYPES[(_soqt_constructor_class, "__init__")] = (
        "self, parent: QWidget | None = ..., name: str | None = ..., "
        "embed: bool = ..., flag: SoQtBuildFlag = ..., "
        "type: SoQtViewerType = ...",
        "None",
    )
PYTHON_SHADOW_METHOD_TYPES[("SoSearchAction", "setFind")] = (
    "self, what: SoSearchFind",
    "None",
)
PYTHON_SHADOW_METHOD_TYPES[("SoSearchAction", "getFind")] = (
    "self",
    "SoSearchFind",
)
PYTHON_SHADOW_METHOD_TYPES[("SoSearchAction", "setInterest")] = (
    "self, interest: SoSearchInterest",
    "None",
)
PYTHON_SHADOW_METHOD_TYPES[("SoSearchAction", "getInterest")] = (
    "self",
    "SoSearchInterest",
)
for _callback_action_method, _callback_action_type in (
    ("getComplexityType", "SoComplexityValue"),
    ("getLightModel", "SoLightModelValue"),
    ("getVertexOrdering", "SoShapeHintsOrdering"),
    ("getShapeType", "SoShapeHintsShapeType"),
    ("getFaceType", "SoShapeHintsFaceType"),
    ("getUnits", "SoUnitsValue"),
    ("getPickStyle", "SoPickStyleValue"),
):
    PYTHON_SHADOW_METHOD_TYPES[("SoCallbackAction", _callback_action_method)] = (
        "self",
        _callback_action_type,
    )
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
FUNCTION_POINTER_TYPE_SIGNATURES = {"void(*)(void*)": "Callable[[object], None]"}
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
        "SoSensorCallback[%s, _SensorDataT]" % class_name,
        "_SensorDataT | None",
    )
    for class_name in SENSOR_CALLBACK_CLASSES
}
KNOWN_ITER_ELEMENT_TYPES = {
    "SbIntList": "int",
    "SbName": "str",
    # SbPList is intentionally heterogeneous.  ``object`` keeps callers
    # honest at this untyped legacy boundary; typed subclasses below provide
    # concrete element types where Coin guarantees them.
    "SbPList": "object",
    "SbString": "str",
    **vector_iter_element_types(),
    # The base multifield has no element type.  Concrete SoMF* classes are
    # normalized from MULTIFIELD_TYPE_POLICIES below.
    "SoMField": "object",
    "SoNodeKitPath": "SoNode",
    "SoPath": "SoNode",
}
RUNTIME_UNSUPPORTED_NOTE = (
    "NOTE: SWIG exposes raw C pointers here; keep Incomplete until a "
    "Python-level wrapper exists."
)
RUNTIME_UNSUPPORTED_METHOD_NOTES = {}
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

# Family-level follow-up guidance makes the opaque-parameter report an audit
# artifact rather than just a count.  The guidance is deliberately
# conservative: each family must earn a concrete annotation through a safe
# adapter or a runtime proof.
OPAQUE_PARAMETER_FAMILY_ACTIONS = {
    "geometry": "probe copy/sequence adapters; preserve cross-width overloads",
    "image/buffer": "keep native storage opaque; prefer snapshot adapters",
    "action": "model action handles only with ownership proof",
    "array/output": "use typed pointer helpers or tuple outputs",
    "callback/handle": "move userdata into a named callback contract",
    "other": "require symbol-level review before typing",
}


@dataclass(frozen=True)
class GeometryParameterAudit:
    """Review record for one opaque geometry parameter."""

    disposition: str
    rationale: str
    next_action: str


# These are the complete, currently observed geometry-family boundaries.
# They are kept explicit so a future sequence/copy adapter can reduce this
# list one proven symbol at a time without silently widening the API.
GEOMETRY_PARAMETER_AUDIT = {
    key: GeometryParameterAudit(
        disposition="intentional native boundary",
        rationale=(
            "The parameter is a legacy native pointer/reference or "
            "cross-width geometry value; the generated Python surface does "
            "not yet prove a safe copy or sequence conversion."
        ),
        next_action=(
            "Add a runtime-backed copy/sequence overload only after testing "
            "the exact native layout and ownership behavior."
        ),
    )
    for key in (
        ("parameter", "SbVec2s", "setValue", "v"),
        ("parameter", "SbVec2s", "__init__", "v"),
        ("parameter", "SbVec3s", "setValue", "v"),
        ("parameter", "SbVec3s", "__init__", "v"),
        ("parameter", "SbMatrix", "__init__", "matrix"),
        ("parameter", "SbMatrix", "setValue", "pMat"),
        ("parameter", "SbMatrix", "getValue", "m"),
        ("parameter", "SbMatrix", "LUDecomposition", "index"),
        ("parameter", "SbMatrix", "LUBackSubstitution", "index"),
        ("parameter", "SbPlane", "intersect", "SbPlane"),
        ("parameter", "SbVec2i32", "setValue", "v"),
        ("parameter", "SbVec2i32", "__init__", "v"),
        ("parameter", "SbVec3i32", "setValue", "v"),
        ("parameter", "SbVec3i32", "__init__", "v"),
        ("parameter", "SbVec2b", "setValue", "v"),
        ("parameter", "SbVec2b", "__init__", "v"),
        ("parameter", "SbVec3b", "setValue", "v"),
        ("parameter", "SbVec3b", "__init__", "v"),
    )
}


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
class RawPointerAudit:
    """Review record for one intentionally raw C-pointer boundary."""

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


# A small number of field attributes are not emitted by stubgen even though
# Coin exposes them through the runtime field registry.  Keep these binding
# names declarative so the generator and the coverage check share one list.
# The runtime checker is deliberately broader than this table: it will report
# newly exposed SoSF*/SoMF* fields instead of silently accepting drift.
FIELD_ATTRIBUTE_TYPE_POLICIES = {
    "SoNodeKitListPart": {
        "containerTypeName": "SoSFName",
        "childTypeNames": "SoMFName",
        "containerNode": "SoSFNode",
    },
    "SoVRMLAnchor": {
        "addChildren": "SoMFNode",
        "removeChildren": "SoMFNode",
    },
    "SoVRMLAudioClip": {
        "duration_changed": "SoSFTime",
        "isActive": "SoSFBool",
    },
    "SoVRMLBackground": {
        "set_bind": "SoSFBool",
        "isBound": "SoSFBool",
    },
    "SoVRMLBillboard": {
        "addChildren": "SoMFNode",
        "removeChildren": "SoMFNode",
    },
    "SoVRMLCollision": {
        "addChildren": "SoMFNode",
        "removeChildren": "SoMFNode",
    },
    "SoVRMLFog": {
        "set_bind": "SoSFBool",
        "isBound": "SoSFBool",
    },
    "SoVRMLGroup": {
        "addChildren": "SoMFNode",
        "removeChildren": "SoMFNode",
    },
    "SoVRMLNavigationInfo": {
        "set_bind": "SoSFBool",
        "isBound": "SoSFBool",
    },
    "SoVRMLTimeSensor": {
        "timeIn": "SoSFTime",
    },
    "SoVRMLTransform": {
        "addChildren": "SoMFNode",
        "removeChildren": "SoMFNode",
    },
    "SoVRMLViewpoint": {
        "set_bind": "SoSFBool",
        "bindTime": "SoSFTime",
        "isBound": "SoSFBool",
    },
}
RUNTIME_FIELD_ATTRIBUTE_TYPE_POLICIES = {
    class_name: dict(attributes)
    for class_name, attributes in FIELD_ATTRIBUTE_TYPE_POLICIES.items()
}

# These public attributes are emitted by stubgen or documented by the native
# runtime rather than added by the field-registry normalizer above.  Keep
# their expected Python types in the same policy registry so structural
# validation does not maintain a second attribute database.
FIELD_ATTRIBUTE_TYPE_POLICIES.update(
    {
        "SoBoolOperation": {
            "inverse": "SoEngineOutput",
            "output": "SoEngineOutput",
        },
        "SoComposeVec3f": {"vector": "SoEngineOutput"},
        "SoDecomposeVec3f": {
            "x": "SoEngineOutput",
            "vector": "SoMFVec3f",
        },
        "SoCube": {
            "width": "SoSFFloat",
            "height": "SoSFFloat",
            "depth": "SoSFFloat",
        },
        "SoMaterial": {
            "diffuseColor": "SoMFColor",
            "ambientColor": "SoMFColor",
            "emissiveColor": "SoMFColor",
            "specularColor": "SoMFColor",
            "shininess": "SoMFFloat",
            "transparency": "SoMFFloat",
        },
        "SoTransform": {
            "center": "SoSFVec3f",
            "scaleFactor": "SoSFVec3f",
            "translation": "SoSFVec3f",
            "rotation": "SoSFRotation",
            "scaleOrientation": "SoSFRotation",
        },
        "SoCamera": {
            "aspectRatio": "SoSFFloat",
            "farDistance": "SoSFFloat",
            "focalDistance": "SoSFFloat",
            "nearDistance": "SoSFFloat",
            "orientation": "SoSFRotation",
            "position": "SoSFVec3f",
            "viewportMapping": "SoSFEnum",
        },
        "SoLight": {
            "color": "SoSFColor",
            "intensity": "SoSFFloat",
            "on": "SoSFBool",
        },
        "SoSphere": {"radius": "SoSFFloat"},
        "SoCylinder": {"parts": "SoSFBitMask"},
        "SoCone": {"parts": "SoSFBitMask"},
        "SoDirectionalLight": {"direction": "SoSFVec3f"},
        "SoTexture2": {
            "blendColor": "SoSFColor",
            "enableCompressedTexture": "SoSFBool",
            "filename": "SoSFString",
            "image": "SoSFImage",
            "model": "SoSFEnum",
            "wrapS": "SoSFEnum",
            "wrapT": "SoSFEnum",
        },
        "SoCoordinate3": {"point": "SoMFVec3f"},
        "SoNormal": {"vector": "SoMFVec3f"},
        "SoTextureCoordinate2": {"point": "SoMFVec2f"},
        "SoVertexProperty": {
            "normal": "SoMFVec3f",
            "texCoord": "SoMFVec2f",
            "vertex": "SoMFVec3f",
            "textureUnit": "SoMFInt32",
        },
        "SoIndexedShape": {
            "coordIndex": "SoMFInt32",
            "materialIndex": "SoMFInt32",
            "normalIndex": "SoMFInt32",
            "textureCoordIndex": "SoMFInt32",
        },
        "SoShapeHints": {
            "creaseAngle": "SoSFFloat",
            "faceType": "SoSFEnum",
            "shapeType": "SoSFEnum",
            "useVBO": "SoSFBool",
            "vertexOrdering": "SoSFEnum",
            "windingType": "SoSFEnum",
        },
        "SbViewVolume": {
            "type": "int",
            "projPoint": "SbVec3f",
            "projDir": "SbVec3f",
            "nearDist": "float",
            "nearToFar": "float",
            "llf": "SbVec3f",
            "lrf": "SbVec3f",
            "ulf": "SbVec3f",
        },
        "SoIntersectingPrimitive": {
            "path": "SoPath | None",
            "type": "int",
            "vertex": "SbVec3f",
            "xf_vertex": "SbVec3f",
        },
        "SoNormalBundle": {"generator": "SoNormalGenerator | None"},
        "SoSearchAction": {"duringSearchAll": "bool"},
    }
)

# Python keywords cannot be used in dotted attribute access.  Coin retains
# these native field names in its registry, while the generated SWIG module
# exposes the established Python-safe aliases.
FIELD_ATTRIBUTE_NAME_ALIASES = {
    ("SoComposeRotationFromTo", "from"): "srcFrom",
    ("SoComposeRotationFromTo", "to"): "destTo",
}


@dataclass(frozen=True)
class MultifieldTypePolicy:
    """Python-level value policy for a multiple-value Coin field."""

    element_type: str
    set_values_types: tuple[str, ...] = ()
    get_values_type: str | None = None
    single_value_type: str | None = None
    indexed_access: bool = True
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
    "SoSFBool": FieldTypePolicy(
        value_type="bool",
        setter_argument_type="bool",
        setter_value_type="bool",
    ),
    "SoSFInt32": FieldTypePolicy(
        value_type="int",
        setter_argument_type="int",
        setter_value_type="int",
    ),
    "SoSFShort": FieldTypePolicy(
        value_type="int",
        setter_argument_type="int",
        setter_value_type="int",
    ),
    "SoSFUShort": FieldTypePolicy(
        value_type="int",
        setter_argument_type="int",
        setter_value_type="int",
    ),
    "SoSFUInt32": FieldTypePolicy(
        value_type="int",
        setter_argument_type="int",
        setter_value_type="int",
    ),
    "SoSFFloat": FieldTypePolicy(
        value_type="float",
        setter_argument_type="float",
        setter_value_type="float",
    ),
    "SoSFDouble": FieldTypePolicy(
        value_type="float",
        setter_argument_type="float",
        setter_value_type="float",
    ),
    "SoSFTime": FieldTypePolicy(
        value_type="SbTime",
        setter_argument_type="SbTime",
        setter_value_type="SbTime",
    ),
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
    "SoMFDouble": MultifieldTypePolicy(
        element_type="float",
        set_values_types=("float",),
        get_values_type="float",
    ),
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


def multifield_values_types():
    """Return Python types exposed by the convenience ``values`` property.

    ``values`` is intentionally different from ``getValuesSnapshot``.  The
    binding converts iterable vector/color values to nested Python sequences,
    and converts ``SbName``/``SbString`` values to ordinary strings.
    """

    values = {}
    for field_class, policy in MULTIFIELD_TYPE_POLICIES.items():
        if field_class in {"SoMFName", "SoMFString"}:
            values[field_class] = "str"
        elif field_class == "SoMFColor":
            values[field_class] = "Sequence[float]"
        elif policy.component_sequence_type:
            values[field_class] = policy.component_sequence_type
        else:
            values[field_class] = policy.element_type
    return values


def multifield_snapshot_types():
    """Return element types for owned Python multifield snapshots."""

    return {
        field_class: policy.element_type
        for field_class, policy in MULTIFIELD_TYPE_POLICIES.items()
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
        ('parameter', 'SoDB', 'doSelect', 'exceptfds'),
        ('parameter', 'SoDB', 'doSelect', 'readfds'),
        ('parameter', 'SoDB', 'doSelect', 'writefds'),
        ('parameter', 'SoDB', 'getHeaderData', 'userdata'),
        ('parameter', 'SoField', 'addAuditor', 'f'),
        ('parameter', 'SoField', 'removeAuditor', 'f'),
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


def _raw_pointer_audits(
    keys: tuple[tuple[str, str, str, str], ...],
    *,
    disposition: str,
    rationale: str,
    next_action: str,
) -> dict[tuple[str, str, str, str], RawPointerAudit]:
    return {
        key: RawPointerAudit(
            disposition=disposition,
            rationale=rationale,
            next_action=next_action,
        )
        for key in keys
    }


# Every current ``raw C pointers`` site has an explicit review record.  The
# keys are intentionally listed one by one: a broad classifier may recognize
# a new SWIG pointer-shaped signature, but it must not silently make that
# boundary part of the supported API.
RAW_POINTER_AUDIT = {
    **_raw_pointer_audits(
        (
            ("parameter", "SbBSPTree", "setUserData", "data"),
            ("parameter", "SbByteBuffer", "__init__", "buffer"),
            ("parameter", "SbHeap", "buildHeap", "data"),
            ("parameter", "SbImage", "__init__", "bytes"),
            ("parameter", "SbOctTree", "debugTree", "fp"),
            ("parameter", "SbTesselator", "__init__", "data"),
            ("parameter", "SbTesselator", "addVertex", "data"),
            ("parameter", "SoByteStream", "unconvert", "data"),
            ("parameter", "SoGLImage", "setData", "bytes"),
            ("parameter", "SoMarkerSet", "addMarker", "bytes"),
            ("parameter", "SoMarkerSet", "getMarker", "bytes"),
            ("parameter", "SoMultiTextureImageElement", "set", "bytes"),
            ("parameter", "SoMultiTextureImageElement", "setElt", "bytes"),
            ("parameter", "SoSFImage", "setSubValue", "pixels"),
            ("parameter", "SoSFImage", "setSubValues", "pixelblocks"),
            ("parameter", "SoTexture2", "readImage", "bytes"),
            ("parameter", "SoTextureCubeMap", "readImage", "bytes"),
            ("parameter", "SoVRMLAudioClip", "read", "buffer"),
        ),
        disposition="intentional native input boundary",
        rationale=(
            "SWIG accepts a borrowed native buffer or pointer whose Python "
            "ownership and lifetime are not represented by the binding."
        ),
        next_action=(
            "Add a copying or owning Python adapter after confirming the "
            "native buffer layout and lifetime."
        ),
    ),
    **_raw_pointer_audits(
        (
            ("parameter", "SbBox3d", "output", "file"),
            ("parameter", "SbBox3f", "output", "file"),
            ("parameter", "SbCylinder", "output", "file"),
            ("parameter", "SbDPLine", "output", "file"),
            ("parameter", "SbDPMatrix", "output", "fp"),
            ("parameter", "SbDPPlane", "output", "file"),
            ("parameter", "SbDPRotation", "output", "fp"),
            ("parameter", "SbDPViewVolume", "output", "fp"),
            ("parameter", "SbLine", "output", "file"),
            ("parameter", "SbMatrix", "output", "fp"),
            ("parameter", "SbPlane", "output", "file"),
            ("parameter", "SbRotation", "output", "fp"),
            ("parameter", "SbSphere", "output", "file"),
            ("parameter", "SbTime", "output", "fp"),
            ("parameter", "SbVec2d", "output", "fp"),
            ("parameter", "SbVec2f", "output", "fp"),
            ("parameter", "SbVec2i32", "output", "fp"),
            ("parameter", "SbVec2s", "output", "fp"),
            ("parameter", "SbVec3d", "output", "fp"),
            ("parameter", "SbVec3f", "output", "fp"),
            ("parameter", "SbVec3s", "output", "fp"),
            ("parameter", "SbVec4d", "output", "fp"),
            ("parameter", "SbVec4f", "output", "fp"),
            ("parameter", "SbViewVolume", "output", "fp"),
            ("parameter", "SbViewportRegion", "output", "file"),
            ("parameter", "SbXfBox3f", "output", "file"),
            ("parameter", "SoCoordinateElement", "output", "file"),
            ("parameter", "SoElement", "output", "file"),
            ("parameter", "SoEnvironmentElement", "output", "file"),
            ("parameter", "SoFloatElement", "output", "file"),
            ("parameter", "SoFontNameElement", "output", "file"),
            ("parameter", "SoInt32Element", "output", "file"),
            ("parameter", "SoLightAttenuationElement", "output", "file"),
            ("parameter", "SoListenerDopplerElement", "output", "file"),
            ("parameter", "SoListenerOrientationElement", "output", "file"),
            ("parameter", "SoListenerPositionElement", "output", "file"),
            ("parameter", "SoNotList", "output", "file"),
            ("parameter", "SoNotRec", "output", "file"),
            ("parameter", "SoOverrideElement", "output", "file"),
            ("parameter", "SoReplacedElement", "output", "file"),
            ("parameter", "SoShapeHintsElement", "output", "file"),
            ("parameter", "SoSoundElement", "output", "file"),
            ("parameter", "SoState", "output", "file"),
            ("parameter", "SoTextureOverrideElement", "output", "fp"),
            ("parameter", "SoViewportRegionElement", "output", "file"),
        ),
        disposition="intentional native output boundary",
        rationale=(
            "Coin writes to a native FILE-like sink or ABI-level pointer; "
            "the Python binding does not own or model that sink."
        ),
        next_action=(
            "Provide a Python file-like or serialized-value adapter only "
            "after confirming the native output contract."
        ),
    ),
    **_raw_pointer_audits(
        (
            ("parameter", "SoAction", "getPathCode", "indices"),
            ("parameter", "SoAction", "usePathCode", "indices"),
            ("parameter", "SoFieldData", "getEnumData", "values"),
            ("parameter", "SoInput", "readBinaryArray", "c"),
            ("parameter", "SoInput", "readBinaryArray", "d"),
            ("parameter", "SoInput", "readBinaryArray", "f"),
            ("parameter", "SoInput", "readBinaryArray", "l"),
            ("parameter", "SoInput", "resetFilePointer", "fptr"),
            ("parameter", "SoInput", "setBuffer", "bufpointer"),
            ("parameter", "SoInput", "setFilePointer", "newFP"),
            ("parameter", "SoInput", "setStringArray", "strings"),
            ("parameter", "SoOutput", "getBuffer", "bufPointer"),
            ("parameter", "SoOutput", "setBuffer", "bufPointer"),
            ("parameter", "SoOutput", "setFilePointer", "newFP"),
            ("parameter", "SoOutput", "writeBinaryArray", "c"),
            ("parameter", "SoOutput", "writeBinaryArray", "d"),
            ("parameter", "SoOutput", "writeBinaryArray", "f"),
            ("parameter", "SoOutput", "writeBinaryArray", "l"),
            ("parameter", "SoSensorManager", "doSelect", "userTimeOut"),
            ("parameter", "SoDB", "doSelect", "usertimeout"),
            ("parameter", "SoOffscreenRenderer", "writeToPostScript", "fp"),
            ("parameter", "SoOffscreenRenderer", "writeToRGB", "fp"),
        ),
        disposition="intentional ABI boundary",
        rationale=(
            "The parameter is a pointer-to-pointer, output array, file "
            "descriptor, or mutable native storage handle rather than a "
            "stable Python value."
        ),
        next_action=(
            "Add a typed output tuple, buffer protocol, or lifetime-bound "
            "view only after testing the native ownership semantics."
        ),
    ),
    **_raw_pointer_audits(
        (
            ("return", "SoDiffuseColorElement", "getPackedArrayPtr", "return"),
            ("return", "SoInput", "getCurFile", "return"),
            ("return", "SoLazyElement", "getColorIndexPointer", "return"),
            ("return", "SoLazyElement", "getPackedColors", "return"),
            ("return", "SoLazyElement", "getTransparencyPointer", "return"),
            ("return", "SoMultiTextureImageElement", "get", "return"),
            ("return", "SoMultiTextureImageElement", "getDefault", "return"),
            ("return", "SoMultiTextureImageElement", "getImage", "return"),
            ("return", "SoOutput", "getFilePointer", "return"),
            ("return", "SoSFImage", "getSubTexture", "return"),
            ("return", "SoVectorOutput", "getFilePointer", "return"),
        ),
        disposition="intentional borrowed native return",
        rationale=(
            "The wrapper returns borrowed native storage or a platform "
            "pointer without an independent Python owner."
        ),
        next_action=(
            "Add an owning copy or an explicit lifetime-bound view before "
            "exposing a concrete Python return type."
        ),
    ),
}


@dataclass(frozen=True)
class CoinTypingPolicy:
    """Single registry for the Python-facing Coin binding policy."""

    vectors: Mapping[str, VectorTypePolicy]
    fields: Mapping[str, FieldTypePolicy]
    multifields: Mapping[str, MultifieldTypePolicy]
    field_attributes: Mapping[str, Mapping[str, str]]
    field_aliases: Mapping[tuple[str, str], str]
    method_return_overrides: Mapping[tuple[str, str], object]
    callback_methods: Mapping[tuple[str, str], CallbackMethodPolicy]
    protocols: tuple[tuple[str, tuple[str, ...], str], ...]
    incomplete_rules: tuple[IncompleteRule, ...]


# Keep the individual names above as compatibility aliases for focused
# generator helpers, but expose one immutable registry for new consumers.
COIN_TYPING_POLICY = CoinTypingPolicy(
    vectors=MappingProxyType(dict(VECTOR_TYPE_POLICIES)),
    fields=MappingProxyType(dict(FIELD_TYPE_POLICIES)),
    multifields=MappingProxyType(dict(MULTIFIELD_TYPE_POLICIES)),
    field_attributes=MappingProxyType(
        {name: MappingProxyType(dict(attributes))
         for name, attributes in FIELD_ATTRIBUTE_TYPE_POLICIES.items()}
    ),
    field_aliases=MappingProxyType(dict(FIELD_ATTRIBUTE_NAME_ALIASES)),
    method_return_overrides=MappingProxyType(dict(METHOD_RETURN_TYPE_OVERRIDES)),
    callback_methods=MappingProxyType(dict(CALLBACK_METHOD_POLICIES)),
    protocols=tuple(PYTHON_PROTOCOL_DEFINITIONS),
    incomplete_rules=tuple(INCOMPLETE_RULES),
)

# These are intentionally opaque pointer-to-pointer or platform-structure
# surfaces. Keep them visible in the report without pretending that the raw
# SWIG representation is a useful Python type.
INCOMPLETE_CATEGORY_OVERRIDES = {
    ("parameter", "SoAction", "getPathCode", "indices"): "raw C pointers",
    ("parameter", "SoAction", "usePathCode", "indices"): "raw C pointers",
    ("parameter", "SoFieldData", "getEnumData", "values"): "raw C pointers",
    ("parameter", "SoSensorManager", "doSelect", "userTimeOut"): "raw C pointers",
    ("parameter", "SoDB", "doSelect", "usertimeout"): "raw C pointers",
    # SoQt exposes the native event-handler function pointer and closure
    # directly.  There is no Python adapter for these low-level device hooks.
    ("parameter", "SoQtDevice", "enable", "handler"): "function pointers",
    ("parameter", "SoQtDevice", "disable", "handler"): "function pointers",
    ("parameter", "SoQtDevice", "enable", "closure"): "raw C pointers",
    ("parameter", "SoQtDevice", "disable", "closure"): "raw C pointers",
    ("parameter", "SoQtKeyboard", "enable", "handler"): "function pointers",
    ("parameter", "SoQtKeyboard", "disable", "handler"): "function pointers",
    ("parameter", "SoQtKeyboard", "enable", "closure"): "raw C pointers",
    ("parameter", "SoQtKeyboard", "disable", "closure"): "raw C pointers",
    ("parameter", "SoQtMouse", "enable", "handler"): "function pointers",
    ("parameter", "SoQtMouse", "disable", "handler"): "function pointers",
    ("parameter", "SoQtMouse", "enable", "closure"): "raw C pointers",
    ("parameter", "SoQtMouse", "disable", "closure"): "raw C pointers",
    ("parameter", "SoQtViewer", "getAnaglyphStereoColorMasks", "left"):
        "unknown output parameters",
    ("parameter", "SoQtViewer", "getAnaglyphStereoColorMasks", "right"):
        "unknown output parameters",
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
