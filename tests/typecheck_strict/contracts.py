# pyright: strict
# pyright: reportMissingModuleSource=false

from typing import Iterator
from typing_extensions import assert_type

from pivy import coin


def scenegraph_contract() -> None:
    root = coin.SoSeparator()
    root.addChild(coin.SoCone())
    child = root.getChild(0)
    assert_type(child, coin.SoNode)


def field_contract() -> None:
    field = coin.SoMFVec3f()
    field.setValues([[1.0, 2.0, 3.0]])
    snapshot = field.getValuesSnapshot()
    assert_type(snapshot, list[coin.SbVec3f])
    values: Iterator[coin.SbVec3f] = iter(field)
    assert_type(values, Iterator[coin.SbVec3f])


def callback_contract() -> None:
    callback_list = coin.SoCallbackList()

    def callback(data: object, callbackdata: object) -> None:
        pass

    callback_list.addCallback(callback, None)
    callback_list.removeCallback(callback, None)
