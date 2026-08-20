"""Shared, declarative policy for the generated Pivy typing surface."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from tools.pivy_stub_generation_data import CALLBACK_PARAMETER_NAMES
except ImportError:
    from pivy_stub_generation_data import CALLBACK_PARAMETER_NAMES


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
    return "uncategorized"
