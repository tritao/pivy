# pyright: reportMissingModuleSource=false

from typing import assert_type

from pivy import coin


def check_scalar_fields() -> None:
    cube = coin.SoCube()

    assert_type(cube.width, coin.SoSFFloat)
    assert_type(cube.height, coin.SoSFFloat)
    assert_type(cube.depth, coin.SoSFFloat)
    assert_type(cube.width.getValue(), float)
    cube.width.setValue(10.0)

    enabled = coin.SoSFBool()
    assert_type(enabled.getValue(), bool)
    enabled.setValue(True)


def check_value_fields() -> None:
    material = coin.SoMaterial()

    assert_type(material.diffuseColor, coin.SoMFColor)
    assert_type(material.transparency, coin.SoMFFloat)

    color = coin.SoSFColor()
    assert_type(color.getValue(), coin.SbColor)
    color.setValue(0.2, 0.4, 0.8)
    color.setValue([0.2, 0.4, 0.8])

    direction = coin.SoSFVec3f()
    assert_type(direction.getValue(), coin.SbVec3f)
    direction.setValue(1.0, 2.0, 3.0)
    direction.setValue([1.0, 2.0, 3.0])

    rotation = coin.SoSFRotation()
    assert_type(rotation.getValue(), coin.SbRotation)
    rotation.setValue([0.0, 0.0, 1.0, 1.5708])


def check_nullable_fields() -> None:
    node = coin.SoSFNode()
    assert_type(node.getValue(), coin.SoNode | None)
    node.setValue(coin.SoCone())
    node.setValue(None)

    path = coin.SoSFPath()
    assert_type(path.getValue(), coin.SoPath | None)
    path.setValue(None)


def check_field_factory_contract() -> None:
    assert_type(coin.SoSFFloat.createInstance(), coin.SoSFFloat)
    assert_type(coin.SoMFVec3f.createInstance(), coin.SoMFVec3f)
    assert_type(coin.SoSFBox3d.createInstance(), coin.SoSFBox3d)
