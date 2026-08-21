# pyright: reportMissingModuleSource=false

from typing import Iterator, Sequence, assert_type

from pivy import coin


def check_scalar_multifield() -> None:
    values = coin.SoMFFloat()

    assert_type(len(values), int)
    assert_type(iter(values), Iterator[float])
    assert_type(values.getValues(), list[float])
    assert_type(values.getValues(0), list[float])

    values.setValues(0, 2, [1.0, 2.0])
    values.set1Value(0, 3.0)
    values[0] = 4.0
    assert_type(values[0], float)


def check_bitmask_multifield() -> None:
    values = coin.SoMFBitMask()

    values.setValues(0, 2, [1, 2])
    assert_type(values[0], int)
    assert_type(values.getValues(), list[int])
    assert_type(iter(values), Iterator[int])
    values[0] = 3


def check_vector_multifield() -> None:
    values = coin.SoMFVec3f()
    vectors: Sequence[coin.SbVec3f] = [coin.SbVec3f()]
    coordinates: Sequence[Sequence[float]] = [(1.0, 2.0, 3.0)]

    assert_type(iter(values), Iterator[coin.SbVec3f])
    assert_type(values[0], coin.SbVec3f)
    assert_type(values.getValues(), list[coin.SbVec3f])
    values.setValues(0, 1, vectors)
    values.setValues(0, 1, coordinates)
    values.set1Value(0, coordinates[0])
    values[0] = coin.SbVec3f()


def check_color_multifield() -> None:
    values = coin.SoMFColor()
    rgb: Sequence[float] = (0.2, 0.4, 0.8)

    assert_type(iter(values), Iterator[coin.SbColor])
    assert_type(values[0], coin.SbColor)
    assert_type(values.getValues(), list[coin.SbColor])
    values.setValues(0, 1, [coin.SbColor()])
    values.setValues(0, 1, [rgb])
    values.set1Value(0, rgb)
    values[0] = rgb


def check_object_multifields() -> None:
    nodes = coin.SoMFNode()
    node_values: Sequence[coin.SoNode] = [coin.SoCube()]
    assert_type(nodes[0], coin.SoNode)
    nodes.setValues(0, 1, node_values)
    nodes[0] = coin.SoSphere()
    assert_type(iter(nodes), Iterator[coin.SoNode])

    strings = coin.SoMFString()
    string_values: Sequence[coin.SbString | str] = ["pivy", coin.SbString()]
    strings.setValues(0, 2, string_values)
    assert_type(iter(strings), Iterator[coin.SbString])
    assert_type(strings[0], coin.SbString)
    assert_type(strings.getValues(), list[str])
