# pyright: reportMissingModuleSource=false

from typing import assert_type

from pivy import coin


def check_scalar_fields() -> None:
    cube = coin.SoCube()

    assert_type(cube.width, coin.SoSFFloat)
    assert_type(cube.height, coin.SoSFFloat)
    assert_type(cube.depth, coin.SoSFFloat)
    assert_type(cube.width.getValue(), float)
    cube.width.setValue(10.0)

    enabled = coin.SoSFBool()
    assert_type(enabled.getValue(), bool)
    enabled.setValue(True)


def check_value_fields() -> None:
    material = coin.SoMaterial()

    assert_type(material.diffuseColor, coin.SoMFColor)
    assert_type(material.transparency, coin.SoMFFloat)

    color = coin.SoSFColor()
    assert_type(color.getValue(), coin.SbColor)
    color.setValue(0.2, 0.4, 0.8)
    color.setValue([0.2, 0.4, 0.8])

    direction = coin.SoSFVec3f()
    assert_type(direction.getValue(), coin.SbVec3f)
    direction.setValue(1.0, 2.0, 3.0)
    direction.setValue([1.0, 2.0, 3.0])

    rotation = coin.SoSFRotation()
    assert_type(rotation.getValue(), coin.SbRotation)
    rotation.setValue([0.0, 0.0, 1.0, 1.5708])


def check_field_attribute_inventory() -> None:
    material = coin.SoMaterial()
    assert_type(material.ambientColor, coin.SoMFColor)
    assert_type(material.emissiveColor, coin.SoMFColor)
    assert_type(material.specularColor, coin.SoMFColor)
    assert_type(material.shininess, coin.SoMFFloat)

    transform = coin.SoTransform()
    assert_type(transform.center, coin.SoSFVec3f)
    assert_type(transform.scaleFactor, coin.SoSFVec3f)
    assert_type(transform.translation, coin.SoSFVec3f)
    assert_type(transform.rotation, coin.SoSFRotation)
    assert_type(transform.scaleOrientation, coin.SoSFRotation)

    camera = coin.SoCamera()
    assert_type(camera.aspectRatio, coin.SoSFFloat)
    assert_type(camera.farDistance, coin.SoSFFloat)
    assert_type(camera.focalDistance, coin.SoSFFloat)
    assert_type(camera.nearDistance, coin.SoSFFloat)
    assert_type(camera.orientation, coin.SoSFRotation)
    assert_type(camera.position, coin.SoSFVec3f)
    assert_type(camera.viewportMapping, coin.SoSFEnum)

    light = coin.SoLight()
    assert_type(light.color, coin.SoSFColor)
    assert_type(light.intensity, coin.SoSFFloat)
    assert_type(light.on, coin.SoSFBool)

    assert_type(coin.SoSphere().radius, coin.SoSFFloat)
    assert_type(coin.SoCylinder().parts, coin.SoSFBitMask)
    assert_type(coin.SoCone().parts, coin.SoSFBitMask)
    assert_type(coin.SoDirectionalLight().direction, coin.SoSFVec3f)

    texture = coin.SoTexture2()
    assert_type(texture.blendColor, coin.SoSFColor)
    assert_type(texture.enableCompressedTexture, coin.SoSFBool)
    assert_type(texture.filename, coin.SoSFString)
    assert_type(texture.image, coin.SoSFImage)
    assert_type(texture.model, coin.SoSFEnum)
    assert_type(texture.wrapS, coin.SoSFEnum)
    assert_type(texture.wrapT, coin.SoSFEnum)

    assert_type(coin.SoCoordinate3().point, coin.SoMFVec3f)
    assert_type(coin.SoNormal().vector, coin.SoMFVec3f)
    assert_type(coin.SoTextureCoordinate2().point, coin.SoMFVec2f)

    vertex = coin.SoVertexProperty()
    assert_type(vertex.normal, coin.SoMFVec3f)
    assert_type(vertex.texCoord, coin.SoMFVec2f)
    assert_type(vertex.vertex, coin.SoMFVec3f)
    assert_type(vertex.textureUnit, coin.SoMFInt32)

    indexed = coin.SoIndexedFaceSet()
    assert_type(indexed.coordIndex, coin.SoMFInt32)
    assert_type(indexed.materialIndex, coin.SoMFInt32)
    assert_type(indexed.normalIndex, coin.SoMFInt32)
    assert_type(indexed.textureCoordIndex, coin.SoMFInt32)

    hints = coin.SoShapeHints()
    assert_type(hints.creaseAngle, coin.SoSFFloat)
    assert_type(hints.faceType, coin.SoSFEnum)
    assert_type(hints.shapeType, coin.SoSFEnum)
    assert_type(hints.useVBO, coin.SoSFBool)
    assert_type(hints.vertexOrdering, coin.SoSFEnum)
    assert_type(hints.windingType, coin.SoSFEnum)


def check_nullable_fields() -> None:
    node = coin.SoSFNode()
    assert_type(node.getValue(), coin.SoNode | None)
    node.setValue(coin.SoCone())
    node.setValue(None)

    path = coin.SoSFPath()
    assert_type(path.getValue(), coin.SoPath | None)
    path.setValue(None)


def check_image_fields() -> None:
    image = coin.SoSFImage()
    image.setValue(coin.SbVec2s(2, 2), 1, "abcd")
    assert_type(image.getValue(), tuple[str, coin.SbVec2s, int])
    assert_type(image.startEditing(), tuple[str, coin.SbVec2s, int])
    image.finishEditing()

    image3 = coin.SoSFImage3()
    image3.setValue(coin.SbVec3s(2, 2, 2), 1, b"abcdefgh")
    assert_type(image3.getValue(), tuple[str, coin.SbVec3s, int])
    assert_type(image3.startEditing(), tuple[str, coin.SbVec3s, int])
    image3.finishEditing()


def check_field_factory_contract() -> None:
    assert_type(coin.SoSFFloat.createInstance(), coin.SoSFFloat)
    assert_type(coin.SoMFVec3f.createInstance(), coin.SoMFVec3f)
    assert_type(coin.SoSFBox3d.createInstance(), coin.SoSFBox3d)
