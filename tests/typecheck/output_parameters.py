# pyright: reportMissingModuleSource=false

from typing import assert_type

from pivy import coin


def check_scalar_output_helpers() -> None:
    count = coin.uintp()
    assert_type(coin.SoOutput.getAvailableCompressionMethods(count), coin.SbName)
    assert_type(count.value(), int)

    state = coin.SoState(coin.SoCallbackAction(), coin.SoTypeList())
    test = coin.intp()
    write = coin.intp()
    function = coin.intp()
    assert_type(
        coin.SoDepthBufferElement.get(
            state, test, write, function, coin.SbVec2f()
        ),
        None,
    )


def check_numeric_sequence_inputs() -> None:
    state = coin.SoState(coin.SoCallbackAction(), coin.SoTypeList())
    node = coin.SoCube()

    assert_type(
        coin.SoLazyElement.setColorIndices(state, node, 3, [0, 1, 2]),
        None,
    )
    lazy = coin.SoGLLazyElement.createInstance()
    assert_type(lazy.setColorIndexElt(node, 3, [0, 1, 2]), None)
    assert_type(
        coin.SoGLColorIndexElement.set(state, node, 3, [0, 1, 2]),
        None,
    )
    assert_type(
        coin.SoShininessElement.set(state, node, 1, [0.5]),
        None,
    )
    assert_type(
        coin.SoTransparencyElement.set(state, node, 1, [0.5]),
        None,
    )

    field = coin.SoMFEnum()
    assert_type(field.setEnums(1, [0], coin.SbName("ZERO")), None)
