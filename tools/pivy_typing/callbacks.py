"""First-class contracts for Python-facing Pivy callbacks.

The generated annotations describe callable shapes.  These contracts record
the additional binding facts needed to decide whether those annotations are
safe: what is retained, how removal works, and whether ``None`` clears the
callback.  They are deliberately data-only so validators, manifests and
future producer adapters can consume the same information.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping

try:
    from tools.pivy_stub_typing_policy import (
        CALLBACK_DATA_PARAMETER_NAMES,
        CALLBACK_METHOD_POLICIES,
        CALLBACK_PARAMETER_NAMES,
    )
except ImportError:
    from pivy_stub_typing_policy import (
        CALLBACK_DATA_PARAMETER_NAMES,
        CALLBACK_METHOD_POLICIES,
        CALLBACK_PARAMETER_NAMES,
    )


class CallbackRetention(str, Enum):
    """How long a Python callback adapter keeps its closure alive."""

    PROXY_LIFETIME = "proxy-lifetime"
    GLOBAL_REGISTRATION = "global-registration"
    SENSOR_LIFETIME = "sensor-lifetime"
    UNTIL_DISPATCH = "until-dispatch"


class CallbackRemoval(str, Enum):
    """What operation releases a registered callback."""

    IDENTITY = "callback-and-userdata-identity"
    REPLACE_OR_CLEAR = "replace-or-clear"
    DISPATCH = "after-dispatch"
    CLEAR = "clear-all"
    NONE = "not-applicable"


@dataclass(frozen=True)
class CallbackContract:
    """The semantic contract for one callback-bearing method."""

    class_name: str
    method_name: str
    parameter_types: tuple[tuple[str, str], ...]
    callback_parameters: tuple[tuple[str, str], ...]
    userdata_parameters: tuple[str, ...]
    return_type: str
    retention: CallbackRetention
    removal: CallbackRemoval
    nullable: bool
    python_safe: bool
    source: str
    reason: str

    @property
    def key(self) -> tuple[str, str]:
        return self.class_name, self.method_name

    @property
    def has_userdata(self) -> bool:
        return bool(self.userdata_parameters)

    @property
    def callback_type(self) -> str | None:
        return self.callback_parameters[0][1] if self.callback_parameters else None


_CALLBACK_PARAMETER_NAMES = {
    name.lower() for name in CALLBACK_PARAMETER_NAMES
} | {
    "precallback",
    "postcallback",
    "function",
    "f",
    "func",
}
_CALLBACK_DATA_PARAMETER_NAMES = {
    name.lower() for name in CALLBACK_DATA_PARAMETER_NAMES
} | {"userdata", "userdata", "userData".lower()}


def _is_callback_parameter(name: str, annotation: str) -> bool:
    normalized = name.lower()
    return (
        normalized in _CALLBACK_PARAMETER_NAMES
        or "Callable[" in annotation
        or annotation.endswith("Callback")
        or "Callback[" in annotation
    )


def _is_userdata_parameter(name: str) -> bool:
    return name.lower() in _CALLBACK_DATA_PARAMETER_NAMES


def _lifecycle(
    class_name: str,
    method_name: str,
) -> tuple[CallbackRetention, CallbackRemoval]:
    """Return reviewed lifecycle semantics for adapted callback families."""

    key = class_name, method_name
    if key in {
        ("SbImage", "scheduleReadFile"),
        ("SoGLCacheContextElement", "scheduleDeleteCallback"),
    }:
        return CallbackRetention.UNTIL_DISPATCH, CallbackRemoval.DISPATCH

    if class_name in {
        "SoError",
        "SoDebugError",
        "SoMemoryError",
        "SoReadError",
        "SoDB",
        "SoQt",
    }:
        retention = CallbackRetention.GLOBAL_REGISTRATION
    elif class_name in {"SoSensor", "SoDataSensor"}:
        retention = CallbackRetention.SENSOR_LIFETIME
    elif class_name == "SoContextHandler":
        retention = CallbackRetention.GLOBAL_REGISTRATION
    else:
        retention = CallbackRetention.PROXY_LIFETIME

    if method_name == "clearCallbacks":
        return retention, CallbackRemoval.CLEAR
    if method_name == "invokeCallbacks":
        return retention, CallbackRemoval.NONE
    if method_name.startswith("remove"):
        return retention, CallbackRemoval.IDENTITY
    if method_name.startswith("add"):
        return retention, CallbackRemoval.IDENTITY
    if method_name.startswith(("set", "register")):
        return retention, CallbackRemoval.REPLACE_OR_CLEAR
    return retention, CallbackRemoval.REPLACE_OR_CLEAR


def _contract_from_policy(
    class_name: str,
    method_name: str,
    method_policy,
) -> CallbackContract:
    parameters = tuple(method_policy.parameters().items())
    callback_parameters = tuple(
        (name, annotation)
        for name, annotation in method_policy.parameter_types
        if _is_callback_parameter(name, annotation)
    )
    userdata_parameters = tuple(
        name for name, _ in method_policy.parameter_types
        if _is_userdata_parameter(name)
    )
    if not callback_parameters and method_policy.parameter_types:
        # A tuple returned by a callback adapter is still a callback handle,
        # even though its name is not one of the normal callback spellings.
        callback_parameters = tuple(
            (name, annotation)
            for name, annotation in method_policy.parameter_types
            if name == "tuple"
        )
    retention, removal = _lifecycle(class_name, method_name)
    return CallbackContract(
        class_name=class_name,
        method_name=method_name,
        parameter_types=parameters,
        callback_parameters=callback_parameters,
        userdata_parameters=userdata_parameters,
        return_type=(
            method_policy.shadow_signature[1]
            if method_policy.shadow_signature is not None
            else "None"
        ),
        retention=retention,
        removal=removal,
        nullable=any("| None" in annotation for _, annotation in callback_parameters),
        python_safe=True,
        source="tools/pivy_stub_typing_policy.py",
        reason=(
            "SWIG/Pivy adapter exposes a Python callback and records its "
            "closure lifecycle explicitly."
        ),
    )


def _manual_contract(
    class_name: str,
    method_name: str,
    parameter_types: Mapping[str, str],
    return_type: str,
) -> CallbackContract:
    parameters = tuple(parameter_types.items())
    callback_parameters = tuple(
        (name, annotation)
        for name, annotation in parameters
        if _is_callback_parameter(name, annotation) or name == "tuple"
    )
    userdata_parameters = tuple(
        name for name, _ in parameters if _is_userdata_parameter(name)
    )
    retention, removal = _lifecycle(class_name, method_name)
    return CallbackContract(
        class_name=class_name,
        method_name=method_name,
        parameter_types=parameters,
        callback_parameters=callback_parameters,
        userdata_parameters=userdata_parameters,
        return_type=return_type,
        retention=retention,
        removal=removal,
        nullable=any("| None" in annotation for _, annotation in callback_parameters),
        python_safe=True,
        source="tools/pivy_typing/callbacks.py",
        reason=(
            "Existing runtime and static validation establish a Python-safe "
            "callback adapter and its closure lifecycle."
        ),
    )


# These were previously maintained only as validator tuples.  Keeping them
# here makes the contract registry the source for both validation and the
# manifest while preserving the exact existing expected signatures.
_MANUAL_CALLBACK_CONTRACTS = (
    ("SoEventCallback", "addEventCallback", {"pyfunc": "SoEventCallbackHandler", "userdata": "object | None"}, "tuple[SoEventCallbackHandler, object]"),
    ("SoEventCallback", "removeEventCallback", {"tuple": "tuple[SoEventCallbackHandler, object]"}, "None"),
    ("SoSceneManager", "setRenderCallback", {"pyfunc": "SoSceneManagerCallback", "userData": "object | None"}, "None"),
    ("SoRenderManager", "setRenderCallback", {"pyfunc": "SoRenderManagerCallback", "userData": "object | None"}, "None"),
    ("SoRenderManager", "addPreRenderCallback", {"pyfunc": "SoRenderManagerCallback", "data": "object"}, "None"),
    ("SoRenderManager", "removePreRenderCallback", {"pyfunc": "SoRenderManagerCallback", "data": "object"}, "None"),
    ("SoRenderManager", "addPostRenderCallback", {"pyfunc": "SoRenderManagerCallback", "data": "object"}, "None"),
    ("SoRenderManager", "removePostRenderCallback", {"pyfunc": "SoRenderManagerCallback", "data": "object"}, "None"),
    ("ScXMLStateMachine", "addDeleteCallback", {"pyfunc": "ScXMLStateMachineDeleteCallback", "userdata": "object"}, "None"),
    ("ScXMLStateMachine", "removeDeleteCallback", {"pyfunc": "ScXMLStateMachineDeleteCallback", "userdata": "object"}, "None"),
    ("ScXMLStateMachine", "addStateChangeCallback", {"pyfunc": "ScXMLStateChangeCallback", "userdata": "object"}, "None"),
    ("ScXMLStateMachine", "removeStateChangeCallback", {"pyfunc": "ScXMLStateChangeCallback", "userdata": "object"}, "None"),
)


def _build_contracts() -> dict[tuple[str, str], CallbackContract]:
    contracts = {
        key: _contract_from_policy(class_name, method_name, method_policy)
        for key, method_policy in CALLBACK_METHOD_POLICIES.items()
        for class_name, method_name in (key,)
    }
    for class_name, method_name, parameters, return_type in _MANUAL_CALLBACK_CONTRACTS:
        contracts[(class_name, method_name)] = _manual_contract(
            class_name, method_name, parameters, return_type
        )
    return contracts


CALLBACK_CONTRACTS: Mapping[tuple[str, str], CallbackContract] = MappingProxyType(
    _build_contracts()
)


def _is_soqt_class(class_name: str) -> bool:
    return class_name.startswith("SoQt")


def callback_contracts_for_module(module: str) -> tuple[CallbackContract, ...]:
    """Return contracts belonging to ``pivy.coin`` or ``pivy.gui.soqt``."""

    soqt = "soqt" in module.lower()
    return tuple(
        contract
        for contract in CALLBACK_CONTRACTS.values()
        if _is_soqt_class(contract.class_name) == soqt
    )


def callback_method_checks(
    *,
    module: str | None = None,
    excluded_classes: set[str] | frozenset[str] = frozenset(),
) -> tuple[tuple[str, str, dict[str, str], str], ...]:
    """Render contract records in the validator's existing check format."""

    contracts = (
        callback_contracts_for_module(module)
        if module is not None
        else CALLBACK_CONTRACTS.values()
    )
    return tuple(
        (
            contract.class_name,
            contract.method_name,
            dict(contract.parameter_types),
            contract.return_type,
        )
        for contract in contracts
        if contract.class_name not in excluded_classes
    )


__all__ = [
    "CallbackContract",
    "CallbackRemoval",
    "CallbackRetention",
    "CALLBACK_CONTRACTS",
    "callback_contracts_for_module",
    "callback_method_checks",
]
