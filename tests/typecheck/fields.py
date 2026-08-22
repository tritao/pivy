# pyright: reportMissingModuleSource=false

from typing import Iterator
from typing_extensions import assert_type

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


def check_extended_single_value_fields() -> None:
    trigger = coin.SoSFTrigger()
    assert_type(trigger.getValue(), None)
    trigger.setValue()

    time = coin.SoSFTime()
    assert_type(time.getValue(), coin.SbTime)
    time.setValue(coin.SbTime(1.0))

    plane = coin.SoSFPlane()
    assert_type(plane.getValue(), coin.SbPlane)
    plane.setValue(coin.SbPlane())

    matrix = coin.SoSFMatrix()
    assert_type(matrix.getValue(), coin.SbMatrix)
    matrix.setValue(coin.SbMatrix())

    box2 = coin.SoSFBox2f()
    assert_type(box2.getValue(), coin.SbBox2f)
    box2.setValue(0.0, 0.0, 1.0, 1.0)

    box3 = coin.SoSFBox3s()
    assert_type(box3.getValue(), coin.SbBox3s)
    box3.setValue(0, 0, 0, 1, 1, 1)

    rgba = coin.SoSFColorRGBA()
    assert_type(rgba.getValue(), coin.SbColor4f)
    rgba.setValue([0.2, 0.4, 0.8, 1.0])


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


def check_string_name_and_multifield_contracts() -> None:
    string_field = coin.SoSFString()
    assert_type(string_field.getValue(), coin.SbString)
    string_field.setValue(coin.SbString("hello"))
    string_field.setValue("hello")

    name_field = coin.SoSFName()
    assert_type(name_field.getValue(), coin.SbName)
    name_field.setValue(coin.SbName("world"))
    name_field.setValue("world")

    names = coin.SoMFName()
    names.setValues(0, 2, [coin.SbName("one"), "two"])
    assert_type(names[0], coin.SbName)
    assert_type(names.getValues(), list[str])
    assert_type(iter(names), Iterator[coin.SbName])
    names[0] = "updated"

    strings = coin.SoMFString()
    strings.setValues(0, 2, [coin.SbString("one"), "two"])
    assert_type(strings[0], coin.SbString)
    assert_type(strings.getValues(), list[str])
    assert_type(iter(strings), Iterator[coin.SbString])
    strings[0] = coin.SbString("updated")

    nodes = coin.SoMFNode()
    nodes.setValues(0, 1, [coin.SoCone()])
    assert_type(nodes[0], coin.SoNode)
    assert_type(nodes.getValues(), list[coin.SoNode])
    assert_type(iter(nodes), Iterator[coin.SoNode])

    paths = coin.SoMFPath()
    paths.setValues(0, 1, [coin.SoPath()])
    assert_type(paths[0], coin.SoPath)
    assert_type(paths.getValues(), list[coin.SoPath])
    assert_type(iter(paths), Iterator[coin.SoPath])


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


def check_enum_declaration_sequences() -> None:
    field = coin.SoSFEnum()
    field.setEnums(2, [0, 1], ["ZERO", coin.SbName("ONE")])
