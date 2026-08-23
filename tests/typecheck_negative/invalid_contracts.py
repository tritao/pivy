# pyright: reportMissingModuleSource=false

from pivy import coin
from pivy.gui import soqt


def invalid_vector_input() -> None:
    field = coin.SoSFVec3f()
    field.setValue("not a vector")


def invalid_enum_input() -> None:
    field = coin.SoSFEnum()
    field.setValue("not an enum value")


def invalid_multifield_item() -> None:
    field = coin.SoMFVec3f()
    field[0] = "not a vector"


def invalid_multifield_slice() -> None:
    # Coin's SWIG sequence helpers accept integer indexing only; a Python
    # slice reaches the native int overload and raises TypeError at runtime.
    field = coin.SoMFFloat()
    field[0:1]


def invalid_double_multifield_element() -> None:
    field = coin.SoMFDouble()
    field.setValues([object()])


def invalid_callback_arity() -> None:
    callback_list = coin.SoCallbackList()

    def callback(data: object) -> None:
        pass

    callback_list.addCallback(callback, None)


def invalid_stable_enum_value() -> None:
    style: coin.SoDrawStyleValue = 4
    lasso_type: coin.SoExtSelectionLassoType = 3
    depth_function: coin.SoDepthBufferFunction = 8
    selection_policy: coin.SoSelectionPolicy = 4
    rotation_axis: coin.SoRotationXYZAxis = 3
    viewer = soqt.SoQtViewer()
    viewer.setDrawStyle(0, 99)
    del style, lasso_type, depth_function, selection_policy, rotation_axis, viewer


def invalid_nodekit_lookup() -> None:
    kit = coin.SoShapeKit()
    kit.getPart(123, True)


def invalid_soqt_build_flag() -> None:
    soqt.SoQtExaminerViewer(flag=4)
