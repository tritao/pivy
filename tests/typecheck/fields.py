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


def check_multifield_snapshots() -> None:
    vectors = coin.SoMFVec3f()
    vectors.setValues([[1.0, 2.0, 3.0]])
    assert_type(vectors.getValuesSnapshot(), list[coin.SbVec3f])

    scalars = coin.SoMFFloat()
    scalars.setValues([1.0, 2.0])
    assert_type(scalars.getValuesSnapshot(), list[float])

    names = coin.SoMFName()
    names.setValues(["snapshot"])
    assert_type(names.getValuesSnapshot(), list[coin.SbName])


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

    draw_style = coin.SoDrawStyle()
    assert_type(draw_style.linePattern, coin.SoSFUShort)
    assert_type(draw_style.linePatternScaleFactor, coin.SoSFInt32)
    assert_type(draw_style.lineWidth, coin.SoSFFloat)
    assert_type(draw_style.pointSize, coin.SoSFFloat)
    assert_type(draw_style.style, coin.SoSFEnum)

    environment = coin.SoEnvironment()
    assert_type(environment.ambientColor, coin.SoSFColor)
    assert_type(environment.ambientIntensity, coin.SoSFFloat)
    assert_type(environment.attenuation, coin.SoSFVec3f)
    assert_type(environment.fogColor, coin.SoSFColor)
    assert_type(environment.fogType, coin.SoSFEnum)
    assert_type(environment.fogVisibility, coin.SoSFFloat)

    texture = coin.SoTexture3()
    assert_type(texture.blendColor, coin.SoSFColor)
    assert_type(texture.enableCompressedTexture, coin.SoSFBool)
    assert_type(texture.filenames, coin.SoMFString)
    assert_type(texture.images, coin.SoSFImage3)
    assert_type(texture.wrapR, coin.SoSFEnum)

    assert_type(coin.SoTexture2Transform().center, coin.SoSFVec2f)
    assert_type(coin.SoTexture2Transform().rotation, coin.SoSFFloat)
    assert_type(coin.SoTexture2Transform().scaleFactor, coin.SoSFVec2f)
    assert_type(coin.SoTexture3Transform().scaleOrientation, coin.SoSFRotation)

    assert_type(coin.SoFont().name, coin.SoSFName)
    assert_type(coin.SoFont().size, coin.SoSFFloat)
    assert_type(coin.SoFontStyle().family, coin.SoSFEnum)
    assert_type(coin.SoFontStyle().style, coin.SoSFBitMask)
    assert_type(coin.SoText3().string, coin.SoMFString)
    assert_type(coin.SoText3().parts, coin.SoSFBitMask)

    assert_type(coin.SoClipPlane().on, coin.SoSFBool)
    assert_type(coin.SoClipPlane().plane, coin.SoSFPlane)
    assert_type(coin.SoPolygonOffset().factor, coin.SoSFFloat)
    assert_type(coin.SoPolygonOffset().styles, coin.SoSFBitMask)
    assert_type(coin.SoUnits().units, coin.SoSFEnum)
    assert_type(coin.SoBaseColor().rgb, coin.SoMFColor)

    assert_type(coin.SoProfileCoordinate2().point, coin.SoMFVec2f)
    assert_type(coin.SoProfileCoordinate3().point, coin.SoMFVec3f)
    assert_type(coin.SoCoordinate4().point, coin.SoMFVec4f)
    assert_type(coin.SoIndexedShape().coordIndex, coin.SoMFInt32)
    assert_type(coin.SoVertexProperty().orderedRGBA, coin.SoMFUInt32)
    assert_type(coin.SoVertexProperty().texCoord3, coin.SoMFVec3f)


def check_extended_node_field_inventory() -> None:
    switch = coin.SoSwitch()
    assert_type(switch.whichChild, coin.SoSFInt32)

    lod = coin.SoLOD()
    assert_type(lod.center, coin.SoSFVec3f)
    assert_type(lod.range, coin.SoMFFloat)

    assert_type(coin.SoFaceSet().numVertices, coin.SoMFInt32)
    assert_type(coin.SoLineSet().numVertices, coin.SoMFInt32)
    assert_type(coin.SoPointSet().numPoints, coin.SoSFInt32)

    text2 = coin.SoText2()
    assert_type(text2.justification, coin.SoSFEnum)
    assert_type(text2.spacing, coin.SoSFFloat)
    assert_type(text2.string, coin.SoMFString)

    text3 = coin.SoText3()
    assert_type(text3.justification, coin.SoSFEnum)
    assert_type(text3.parts, coin.SoSFBitMask)
    assert_type(text3.spacing, coin.SoSFFloat)
    assert_type(text3.string, coin.SoMFString)

    shape = coin.SoVRMLShape()
    assert_type(shape.appearance, coin.SoSFNode)
    assert_type(shape.boundingBoxCaching, coin.SoSFEnum)
    assert_type(shape.geometry, coin.SoSFNode)
    assert_type(shape.renderCaching, coin.SoSFEnum)

    assert_type(coin.SoMaterialBinding().value, coin.SoSFEnum)
    assert_type(coin.SoNormalBinding().value, coin.SoSFEnum)


def check_runtime_registry_field_contracts() -> None:
    part = coin.SoNodeKitListPart()
    assert_type(part.containerTypeName, coin.SoSFName)
    assert_type(part.childTypeNames, coin.SoMFName)
    assert_type(part.containerNode, coin.SoSFNode)

    anchor = coin.SoVRMLAnchor()
    assert_type(anchor.addChildren, coin.SoMFNode)
    assert_type(anchor.removeChildren, coin.SoMFNode)

    audio = coin.SoVRMLAudioClip()
    assert_type(audio.duration_changed, coin.SoSFTime)
    assert_type(audio.isActive, coin.SoSFBool)

    background = coin.SoVRMLBackground()
    assert_type(background.set_bind, coin.SoSFBool)
    assert_type(background.isBound, coin.SoSFBool)

    billboard = coin.SoVRMLBillboard()
    assert_type(billboard.addChildren, coin.SoMFNode)
    assert_type(billboard.removeChildren, coin.SoMFNode)

    collision = coin.SoVRMLCollision()
    assert_type(collision.addChildren, coin.SoMFNode)
    assert_type(collision.removeChildren, coin.SoMFNode)

    fog = coin.SoVRMLFog()
    assert_type(fog.set_bind, coin.SoSFBool)
    assert_type(fog.isBound, coin.SoSFBool)

    group = coin.SoVRMLGroup()
    assert_type(group.addChildren, coin.SoMFNode)
    assert_type(group.removeChildren, coin.SoMFNode)

    navigation = coin.SoVRMLNavigationInfo()
    assert_type(navigation.set_bind, coin.SoSFBool)
    assert_type(navigation.isBound, coin.SoSFBool)

    timer = coin.SoVRMLTimeSensor()
    assert_type(timer.timeIn, coin.SoSFTime)

    transform = coin.SoVRMLTransform()
    assert_type(transform.addChildren, coin.SoMFNode)
    assert_type(transform.removeChildren, coin.SoMFNode)

    viewpoint = coin.SoVRMLViewpoint()
    assert_type(viewpoint.set_bind, coin.SoSFBool)
    assert_type(viewpoint.bindTime, coin.SoSFTime)
    assert_type(viewpoint.isBound, coin.SoSFBool)


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


def check_numeric_multifield_contracts() -> None:
    booleans = coin.SoMFBool()
    booleans.setValues(0, 2, [True, False])
    assert_type(len(booleans), int)
    assert_type(booleans[0], bool)
    booleans[0] = True
    assert_type(booleans.getValues(), list[bool])
    assert_type(iter(booleans), Iterator[bool])

    integers = coin.SoMFInt32()
    integers.setValues(0, 2, [1, 2])
    assert_type(integers[0], int)
    integers[0] = 3
    assert_type(integers.getValues(), list[int])
    assert_type(iter(integers), Iterator[int])

    floats = coin.SoMFFloat()
    floats.setValues(0, 2, [1.0, 2.0])
    assert_type(floats[0], float)
    floats[0] = 3.0
    assert_type(floats.getValues(), list[float])
    assert_type(iter(floats), Iterator[float])

    colors = coin.SoMFColor()
    colors.setValues(0, 1, [[0.1, 0.2, 0.3]])
    assert_type(colors[0], coin.SbColor)
    colors[0] = coin.SbColor()
    assert_type(colors.getValues(), list[coin.SbColor])
    assert_type(iter(colors), Iterator[coin.SbColor])

    vectors = coin.SoMFVec3f()
    vectors.setValues(0, 1, [[1.0, 2.0, 3.0]])
    assert_type(vectors[0], coin.SbVec3f)
    vectors[0] = coin.SbVec3f()
    assert_type(vectors.getValues(), list[coin.SbVec3f])
    assert_type(iter(vectors), Iterator[coin.SbVec3f])

    rotations = coin.SoMFRotation()
    rotations.setValues(0, 1, [[0.0, 0.0, 1.0, 0.0]])
    assert_type(rotations[0], coin.SbRotation)
    assert_type(rotations.getValues(), list[coin.SbRotation])
    assert_type(iter(rotations), Iterator[coin.SbRotation])


def check_image_fields() -> None:
    image = coin.SoSFImage()
    image.setValue(coin.SbVec2s(2, 2), 1, b"abcd")
    assert_type(image.getValue(), tuple[bytes, coin.SbVec2s, int])
    assert_type(image.startEditing(), tuple[bytes, coin.SbVec2s, int])
    assert_type(
        image.getSubTextureValue(0),
        tuple[bytes | None, coin.SbVec2s, coin.SbVec2s, int],
    )
    image.finishEditing()

    image3 = coin.SoSFImage3()
    image3.setValue(coin.SbVec3s(2, 2, 2), 1, b"abcdefgh")
    assert_type(image3.getValue(), tuple[bytes, coin.SbVec3s, int])
    assert_type(image3.startEditing(), tuple[bytes, coin.SbVec3s, int])
    image3.finishEditing()


def check_field_factory_contract() -> None:
    assert_type(coin.SoSFFloat.createInstance(), coin.SoSFFloat)
    assert_type(coin.SoMFVec3f.createInstance(), coin.SoMFVec3f)
    assert_type(coin.SoSFBox3d.createInstance(), coin.SoSFBox3d)


def check_enum_declaration_sequences() -> None:
    field = coin.SoSFEnum()
    field.setEnums(2, [0, 1], ["ZERO", coin.SbName("ONE")])
