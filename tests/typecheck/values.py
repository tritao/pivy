# pyright: reportMissingModuleSource=false

from typing import Iterator, Sequence
from typing_extensions import assert_type

from pivy import coin


def check_vectors() -> None:
    vector = coin.SbVec3f([1.0, 2.0, 3.0])
    other = coin.SbVec3f(4.0, 5.0, 6.0)

    assert_type(vector.getValue(), Sequence[float])
    assert_type(vector[0], float)
    assert_type(iter(vector), Iterator[float])
    assert_type(len(vector), int)
    assert_type(vector.normalize(), float)
    assert_type(vector.cross(other), coin.SbVec3f)
    assert_type(vector.dot(other), float)
    assert_type(vector + other, coin.SbVec3f)
    assert_type(vector * 2.0, coin.SbVec3f)

    vector[0] = 7.0
    vector.setValue([7.0, 8.0, 9.0])


def check_byte_buffer_snapshot() -> None:
    buffer = coin.SbByteBuffer(4, "a\x00cd")
    assert_type(buffer.data(), bytes)


def check_sb_image_snapshot() -> None:
    image = coin.SbImage()
    pixels, size, components = image.getValue()

    assert_type(pixels, bytes | None)
    assert_type(size, coin.SbVec2s | coin.SbVec3s)
    assert_type(components, int)


def check_glyph_bitmap_snapshot() -> None:
    glyph = coin.SoGlyph.getGlyph("A", coin.SbName("Helvetica"))
    assert_type(
        glyph.getBitmapValue(True),
        tuple[bytes | None, coin.SbVec2s, coin.SbVec2s],
    )


def check_fixed_width_integer_vectors() -> None:
    vector = coin.SbVec4ui32([1, 2, 3, 4])

    assert_type(vector.getValue(), Sequence[int])
    assert_type(vector[0], int)
    assert_type(iter(vector), Iterator[int])
    assert_type(len(vector), int)

    vector[0] = 5
    vector.setValue([5, 6, 7, 8])


def check_element_factory_contract() -> None:
    element = coin.SoShapeHintsElement.createInstance()
    assert_type(element, coin.SoShapeHintsElement)

    model_matrix = coin.SoModelMatrixElement.createInstance()
    assert_type(model_matrix, coin.SoModelMatrixElement)


def check_colors() -> None:
    color = coin.SbColor([0.2, 0.4, 0.8])

    assert_type(color.getValue(), Sequence[float])
    assert_type(color.getHSVValue(), Sequence[float])
    assert_type(color.getPackedValue(), int)
    assert_type(color.setHSVValue(0.5, 0.5, 0.5), coin.SbColor)
    assert_type(color * 0.5, coin.SbColor)


def check_rotations() -> None:
    rotation = coin.SbRotation(coin.SbVec3f(0.0, 1.0, 0.0), 0.5)
    vector = coin.SbVec3f(1.0, 2.0, 3.0)

    axis, angle = rotation.getAxisAngle()
    assert_type(axis, coin.SbVec3f)
    assert_type(angle, float)
    assert_type(rotation.getMatrix(), coin.SbMatrix)
    assert_type(rotation.multVec(vector), coin.SbVec3f)
    assert_type(rotation * vector, coin.SbVec3f)
    assert_type(rotation * 2.0, coin.SbRotation)
    assert_type(rotation.inverse(), coin.SbRotation)


def check_matrices() -> None:
    matrix = coin.SbMatrix.identity()
    vector = coin.SbVec3f(1.0, 2.0, 3.0)
    vector4 = coin.SbVec4f(1.0, 2.0, 3.0, 1.0)

    assert_type(matrix.getValue(), Sequence[Sequence[float]])
    assert_type(matrix[0], Sequence[float])
    assert_type(matrix.multMatrixVec(vector), coin.SbVec3f)
    assert_type(matrix.multDirMatrix(vector), coin.SbVec3f)
    assert_type(matrix.multVecMatrix(vector), coin.SbVec3f)
    assert_type(matrix.multVecMatrix(vector4), coin.SbVec4f)
    assert_type(matrix * vector, coin.SbVec3f)

    translation, rotation, scale, scale_orientation = matrix.getTransform()
    assert_type(translation, coin.SbVec3f)
    assert_type(rotation, coin.SbRotation)
    assert_type(scale, coin.SbVec3f)
    assert_type(scale_orientation, coin.SbRotation)


def check_double_precision_values() -> None:
    rotation = coin.SbDPRotation(coin.SbVec3d(0.0, 1.0, 0.0), 0.5)
    axis, angle = rotation.getAxisAngle()

    assert_type(axis, coin.SbVec3d)
    assert_type(angle, float)


def check_int32_scalar_output_helpers() -> None:
    scalar = coin.intp()

    vector2 = coin.SbVec2i32(1, 2)
    assert_type(vector2.getValue(scalar, scalar), None)

    vector3 = coin.SbVec3i32(1, 2, 3)
    assert_type(vector3.getValue(scalar, scalar, scalar), None)

    vector4 = coin.SbVec4i32(1, 2, 3, 4)
    assert_type(vector4.getValue(scalar, scalar, scalar, scalar), None)

    box2 = coin.SbBox2i32(1, 2, 3, 4)
    assert_type(box2.getBounds(), tuple[int, int, int, int])
    assert_type(box2.getOrigin(), tuple[int, int])
    assert_type(box2.getSize(), coin.SbVec2i32)

    box3 = coin.SbBox3i32(1, 2, 3, 4, 5, 6)
    assert_type(box3.getBounds(), tuple[int, int, int, int, int, int])
    assert_type(box3.getOrigin(), tuple[int, int, int])
    assert_type(box3.getSize(), coin.SbVec3i32)
