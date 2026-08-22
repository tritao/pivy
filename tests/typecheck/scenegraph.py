# pyright: reportMissingModuleSource=false

from typing import Iterator
from typing_extensions import assert_type

from pivy import coin


def check_group_and_node_contract() -> None:
    root = coin.SoSeparator()
    cube = coin.SoCube()
    root.addChild(cube)

    assert_type(root.getChild(0), coin.SoNode)
    assert_type(root.getChildren(), coin.SoChildList)
    assert_type(root.getByName("missing"), coin.SoNode | None)
    assert_type(iter(root), Iterator[coin.SoNode])
    assert_type(cube.getChildren(), coin.SoChildList | None)
    assert_type(coin.SoNode.getByName("missing"), coin.SoNode | None)
    assert_type(
        coin.SoNode.getByName("missing", coin.SoNodeList()), int
    )


def check_path_contract() -> None:
    empty = coin.SoPath()
    assert_type(empty.getHead(), coin.SoNode | None)
    assert_type(empty.getTail(), coin.SoNode | None)
    assert_type(coin.SoPath.getByName("missing"), coin.SoPath | None)

    root = coin.SoSeparator()
    root.addChild(coin.SoCube())
    path = coin.SoPath(root)
    path.append(0)
    assert_type(path.getHead(), coin.SoNode | None)
    assert_type(path.getTail(), coin.SoNode | None)
    assert_type(path.getNode(0), coin.SoNode)
    assert_type(path.getNodeFromTail(0), coin.SoNode)
    assert_type(iter(path), Iterator[coin.SoNode])
    assert_type(path.index(), Iterator[int])


def check_field_and_name_lookups() -> None:
    cube = coin.SoCube()
    assert_type(cube.width, coin.SoSFFloat)
    assert_type(cube.__getattr__("width"), coin.SoField)
    assert_type(cube.__dir__(), list[str])
    assert_type(cube.getField("missing"), coin.SoField | None)
    assert_type(cube.getEventIn("missing"), coin.SoField | None)
    assert_type(cube.getEventOut("missing"), coin.SoField | None)
    assert_type(cube.getFieldName(cube.width), str | None)
    assert_type(cube.getAllFields(coin.SoFieldList()), int)
    assert_type(
        coin.SoBase.getNamedBase("missing", coin.SoType.badType()),
        coin.SoBase | None,
    )


def check_nodekit_lookup() -> None:
    kit = coin.SoShapeKit()
    assert_type(kit.shape, coin.SoNode | coin.SoField)
    assert_type(kit.appearance, coin.SoNode | coin.SoField)


def check_reflection_contract() -> None:
    cube_type = coin.SoType.fromName("SoCube")
    assert_type(cube_type, coin.SoType)
    assert_type(cube_type.isBad(), bool)
    assert_type(cube_type.isDerivedFrom(coin.SoType.fromName("SoNode")), bool)
    assert_type(cube_type.createInstance(), coin.SoBase | coin.SoField | coin.SoPath | None)
