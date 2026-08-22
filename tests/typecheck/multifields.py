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


def check_integer_multifield_family() -> None:
    int32 = coin.SoMFInt32()
    int32.setValues(0, 2, [1, 2])
    assert_type(int32[0], int)
    assert_type(int32.getValues(), list[int])
    assert_type(iter(int32), Iterator[int])
    int32.set1Value(0, 3)
    int32[0] = 4

    short = coin.SoMFShort()
    short.setValues(0, 2, [1, 2])
    assert_type(short[0], int)
    assert_type(short.getValues(), list[int])
    assert_type(iter(short), Iterator[int])
    short.set1Value(0, 3)
    short[0] = 4

    uint32 = coin.SoMFUInt32()
    uint32.setValues(0, 2, [1, 2])
    assert_type(uint32[0], int)
    assert_type(uint32.getValues(), list[int])
    assert_type(iter(uint32), Iterator[int])
    uint32.set1Value(0, 3)
    uint32[0] = 4

    ushort = coin.SoMFUShort()
    ushort.setValues(0, 2, [1, 2])
    assert_type(ushort[0], int)
    assert_type(ushort.getValues(), list[int])
    assert_type(iter(ushort), Iterator[int])
    ushort.set1Value(0, 3)
    ushort[0] = 4


def check_bitmask_multifield() -> None:
    values = coin.SoMFBitMask()

    values.setValues(0, 2, [1, 2])
    assert_type(values[0], int)
    assert_type(values.getValues(), list[int])
    assert_type(iter(values), Iterator[int])
    values[0] = 3


def check_boolean_enum_and_time_multifields() -> None:
    booleans = coin.SoMFBool()
    booleans.setValues(0, 2, [True, False])
    booleans.set1Value(0, True)
    booleans[1] = False
    assert_type(booleans[0], bool)
    assert_type(booleans.getValues(), list[bool])
    assert_type(iter(booleans), Iterator[bool])

    enums = coin.SoMFEnum()
    enums.setValues(0, 2, [1, 2])
    enums.set1Value(0, 3)
    enums[1] = 4
    assert_type(enums[0], int)
    assert_type(enums.getValues(), list[int])
    assert_type(iter(enums), Iterator[int])

    times = coin.SoMFTime()
    time_values: Sequence[coin.SbTime] = [coin.SbTime(0.5)]
    times.setValues(0, 1, time_values)
    times.set1Value(0, coin.SbTime(1.0))
    times[0] = coin.SbTime(2.0)
    assert_type(times[0], coin.SbTime)
    assert_type(times.getValues(), list[coin.SbTime])
    assert_type(iter(times), Iterator[coin.SbTime])


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


def check_color_rgba_multifield() -> None:
    values = coin.SoMFColorRGBA()
    colors: Sequence[coin.SbColor4f] = [coin.SbColor4f()]
    rgba: Sequence[Sequence[float]] = [(0.2, 0.4, 0.8, 1.0)]

    assert_type(iter(values), Iterator[coin.SbColor4f])
    assert_type(values[0], coin.SbColor4f)
    assert_type(values.getValues(), list[coin.SbColor4f])
    values.setValues(0, 1, colors)
    values.setValues(0, 1, rgba)
    values.set1Value(0, rgba[0])
    values[0] = coin.SbColor4f()
    values[0] = rgba[0]


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


def check_string_multifields() -> None:
    names = coin.SoMFName()
    names.setValues(0, 2, ["pivy", coin.SbName("coin")])
    names.set1Value(0, "updated")
    names[1] = "again"
    assert_type(names.find("again"), int)
    assert_type(names[0], coin.SbName)
    assert_type(iter(names), Iterator[coin.SbName])
    assert_type(names.getValues(), list[str])

    strings = coin.SoMFString()
    strings.setValues(0, 2, ["pivy", coin.SbString("coin")])
    strings.set1Value(0, "updated")
    strings[1] = "again"
    assert_type(strings.find("again"), int)
    assert_type(strings[0], coin.SbString)
    assert_type(iter(strings), Iterator[coin.SbString])
    assert_type(strings.getValues(), list[str])
