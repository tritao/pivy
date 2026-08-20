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
