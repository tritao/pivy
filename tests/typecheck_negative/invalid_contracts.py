# pyright: reportMissingModuleSource=false

from pivy import coin


def invalid_vector_input() -> None:
    field = coin.SoSFVec3f()
    field.setValue("not a vector")


def invalid_multifield_item() -> None:
    field = coin.SoMFVec3f()
    field[0] = "not a vector"


def invalid_double_multifield_element() -> None:
    field = coin.SoMFDouble()
    field.setValues([object()])


def invalid_callback_arity() -> None:
    callback_list = coin.SoCallbackList()

    def callback(data: object) -> None:
        pass

    callback_list.addCallback(callback, None)
