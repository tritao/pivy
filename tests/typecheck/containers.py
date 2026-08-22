# pyright: reportMissingModuleSource=false

from typing import Any, Iterator, Sequence
from typing_extensions import assert_type

from pivy import coin


def check_untyped_and_scalar_lists() -> None:
    pointers = coin.SbPList()
    pointers.append(object())
    pointers.set(0, "value")
    assert_type(pointers.get(0), Any)
    assert_type(pointers[0], Any)
    assert_type(iter(pointers), Iterator[Any])

    integers = coin.SbIntList()
    integers.append(1)
    integers.set(0, 2)
    assert_type(integers.get(0), int)
    assert_type(integers[0], int)
    assert_type(iter(integers), Iterator[int])

    name = coin.SbName("pivy")
    string = coin.SbString("pivy")
    assert_type(iter(name), Iterator[str])
    assert_type(iter(string), Iterator[str])


def check_typed_object_lists() -> None:
    base_list = coin.SoBaseList()
    assert_type(base_list.get(0), coin.SoBase)
    assert_type(base_list[0], coin.SoBase)
    assert_type(iter(base_list), Iterator[coin.SoBase])
    base_list.append(coin.SoCube())
    base_list.set(0, coin.SoSphere())
    base_list[0] = coin.SoCone()

    node_list = coin.SoNodeList()
    assert_type(node_list.get(0), coin.SoNode)
    assert_type(node_list[0], coin.SoNode)
    assert_type(iter(node_list), Iterator[coin.SoNode])
    node_list.append(coin.SoCube())
    node_list[0] = coin.SoSphere()

    field_list = coin.SoFieldList()
    assert_type(field_list.get(0), coin.SoField)
    assert_type(field_list[0], coin.SoField)
    assert_type(iter(field_list), Iterator[coin.SoField])
    field_list.append(coin.SoSFFloat())
    field_list[0] = coin.SoSFFloat()

    path_list = coin.SoPathList()
    assert_type(path_list.get(0), coin.SoPath)
    assert_type(path_list[0], coin.SoPath)
    assert_type(iter(path_list), Iterator[coin.SoPath])
    path_list.append(coin.SoPath())
    path_list[0] = coin.SoPath()


def check_scenegraph_collections() -> None:
    root = coin.SoGroup()
    cube = coin.SoCube()
    sphere = coin.SoSphere()
    root.addChild(cube)
    root += [sphere]

    assert_type(root.getChild(0), coin.SoNode)
    assert_type(root.getNumChildren(), int)
    assert_type(root.getChildren(), coin.SoChildList)
    assert_type(root[0], coin.SoNode)
    assert_type(iter(root), Iterator[coin.SoNode])
    assert_type(len(root), int)
    assert_type(cube in root, bool)
    assert_type(root.findChild(cube), int)
    assert_type(root.getByName("child"), coin.SoNode | None)

    children = root.getChildren()
    assert_type(children[0], coin.SoNode)
    assert_type(iter(children), Iterator[coin.SoNode])
    children.append(coin.SoCone())
    children.set(0, coin.SoCylinder())

    root -= sphere
    root -= (cube,)


def check_paths() -> None:
    root = coin.SoSeparator()
    child = coin.SoGroup()
    root.addChild(child)

    path = coin.SoPath()
    path.append(root)
    path.append(0)

    assert_type(path.getHead(), coin.SoNode | None)
    assert_type(path.getTail(), coin.SoNode | None)
    assert_type(path.getNode(0), coin.SoNode)
    assert_type(path.getNodeFromTail(0), coin.SoNode)
    assert_type(path.getIndex(0), int)
    assert_type(path.getIndexFromTail(0), int)
    assert_type(path.getLength(), int)
    assert_type(path.findNode(child), int)
    assert_type(path.containsNode(child), bool)
    assert_type(path.containsPath(path), bool)
    assert_type(iter(path), Iterator[coin.SoNode])
    assert_type(path.index(), Iterator[int])

    nodes: Sequence[coin.SoNode] = [root, child]
    for node in nodes:
        path.append(node)
