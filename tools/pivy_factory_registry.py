"""Canonical registries for class-specific Pivy factory policies."""

from __future__ import annotations


# Keep the order stable: runtime tests use this tuple to exercise every
# factory, while the set is used by the stub-generation policy.
ENGINE_FACTORY_CLASS_NAMES = (
    "SoBoolOperation",
    "SoCalculator",
    "SoComposeVec2f",
    "SoComposeVec3f",
    "SoComposeVec4f",
    "SoDecomposeVec2f",
    "SoDecomposeVec3f",
    "SoDecomposeVec4f",
    "SoComposeRotation",
    "SoDecomposeRotation",
    "SoComposeMatrix",
    "SoDecomposeMatrix",
    "SoComposeRotationFromTo",
    "SoComputeBoundingBox",
    "SoConcatenate",
    "SoCounter",
    "SoElapsedTime",
    "SoGate",
    "SoInterpolateFloat",
    "SoInterpolateVec2f",
    "SoInterpolateVec3f",
    "SoInterpolateVec4f",
    "SoInterpolateRotation",
    "SoOnOff",
    "SoOneShot",
    "SoSelectOne",
    "SoTimeCounter",
    "SoTransformVec3f",
    "SoTriggerAny",
    "SoHeightMapToNormalMap",
    "SoVRMLColorInterpolator",
    "SoVRMLCoordinateInterpolator",
    "SoVRMLNormalInterpolator",
    "SoVRMLOrientationInterpolator",
    "SoVRMLPositionInterpolator",
    "SoVRMLScalarInterpolator",
    "SoVRMLTimeSensor",
)

ENGINE_FACTORY_CLASSES = frozenset(ENGINE_FACTORY_CLASS_NAMES)
