# pyright: reportMissingModuleSource=false

from typing_extensions import assert_type

from pivy import coin


def check_closed_coin_enum_domains() -> None:
    assert_type(coin.SoDepthBuffer.NEVER, coin.SoDepthBufferFunction)
    assert_type(coin.SoDepthBufferElement.LEQUAL, coin.SoDepthBufferFunction)
    assert_type(coin.SoSelection.SINGLE, coin.SoSelectionPolicy)
    assert_type(coin.SoRotationXYZ.Z, coin.SoRotationXYZAxis)
    assert_type(coin.SoSeparator.AUTO, coin.SoSeparatorCacheEnabled)
    assert_type(
        coin.SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND,
        coin.SoTransparencyTypeValue,
    )

