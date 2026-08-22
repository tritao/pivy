# pyright: reportMissingModuleSource=false

from typing_extensions import assert_type

from pivy import coin


def check_input_lookup_and_buffer_contract() -> None:
    reader = coin.SoInput()

    assert_type(reader.findProto(coin.SbName("missing")), coin.SoProto | None)
    assert_type(reader.getCurrentProto(), coin.SoProto | None)
    assert_type(
        reader.findReference(coin.SbName("missing")), coin.SoBase | None
    )
    assert_type(reader.getCurFileName(), str | None)
    assert_type(reader.isValidFile(), bool)
    assert_type(reader.isValidBuffer(), bool)
    assert_type(reader.getNumBytesRead(), int)
    assert_type(reader.getHeader(), coin.SbString)
    assert_type(reader.getIVVersion(), float)
    assert_type(reader.isBinary(), bool)
    assert_type(reader.eof(), bool)

    reader.setBuffer("Separator {}")


def check_output_contract() -> None:
    output = coin.SoOutput()

    assert_type(output.getCurrentProto(), coin.SoProto | None)
    assert_type(output.getBufferSize(), int)
    assert_type(output.isBinary(), bool)
    assert_type(output.isCompact(), bool)
    assert_type(output.getAnnotation(), int)
    assert_type(output.getStage(), int)
    assert_type(output.getDefaultASCIIHeader(), coin.SbString)
    assert_type(output.getDefaultBinaryHeader(), coin.SbString)
    assert_type(output.lookupDEFNode(coin.SbName("missing")), bool)
    assert_type(output.findReference(coin.SoCube()), int)


def check_write_action_output() -> None:
    output = coin.SoOutput()
    action = coin.SoWriteAction(output)
    assert_type(action.getOutput(), coin.SoOutput)


def check_offscreen_buffer_contract() -> None:
    renderer = coin.SoOffscreenRenderer(coin.SbViewportRegion(32, 32))
    assert_type(renderer.getBuffer(), bytes)


def check_color_packer_buffer_contract() -> None:
    packer = coin.SoColorPacker()
    assert_type(packer.getPackedColors(), bytes)
    assert_type(packer.getSize(), int)
