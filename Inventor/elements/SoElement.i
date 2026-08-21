/* Expose Coin's macro-generated element factories as owned, typed objects.
   Coin declares these factories as void * for its C API compatibility. */

%{
#include <Inventor/elements/SoElement.h>

/* autocast an element factory result and transfer ownership to Python */
SWIGEXPORT PyObject *
autocast_element(SoElement * element)
{
  PyObject * result = NULL;

  if (element) {
    PyObject * obj = NULL;
    SoType type = element->getTypeId();

    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)element, SWIGTYPE_p_SoElement, 0);
      result = cast_internal(NULL, obj, type.getName().getString(),
                             type.getName().getLength(), 1);
      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }

    if (!result) {
      result = SWIG_NewPointerObj((void*)element, SWIGTYPE_p_SoElement,
                                  SWIG_POINTER_OWN);
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}
%}

%define PIVY_ELEMENT_FACTORY_OUT(_class_)
%typemap(out) void * _class_::createInstance {
  $result = autocast_element((SoElement *)$1);
}
%enddef

PIVY_ELEMENT_FACTORY_OUT(SoDecimationTypeElement)
PIVY_ELEMENT_FACTORY_OUT(SoComplexityTypeElement)
PIVY_ELEMENT_FACTORY_OUT(SoDrawStyleElement)
PIVY_ELEMENT_FACTORY_OUT(SoLazyElement)
PIVY_ELEMENT_FACTORY_OUT(SoMaterialBindingElement)
PIVY_ELEMENT_FACTORY_OUT(SoNormalBindingElement)
PIVY_ELEMENT_FACTORY_OUT(SoPickStyleElement)
PIVY_ELEMENT_FACTORY_OUT(SoShapeHintsElement)
PIVY_ELEMENT_FACTORY_OUT(SoMultiTextureImageElement)
PIVY_ELEMENT_FACTORY_OUT(SoTextureCoordinateBindingElement)
PIVY_ELEMENT_FACTORY_OUT(SoMultiTextureCoordinateElement)
PIVY_ELEMENT_FACTORY_OUT(SoNormalElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLNormalElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLMultiTextureCoordinateElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLLazyElement)
PIVY_ELEMENT_FACTORY_OUT(SoAmbientColorElement)
PIVY_ELEMENT_FACTORY_OUT(SoAnnoText3CharOrientElement)
PIVY_ELEMENT_FACTORY_OUT(SoAnnoText3FontSizeHintElement)
PIVY_ELEMENT_FACTORY_OUT(SoAnnoText3RenderPrintElement)
PIVY_ELEMENT_FACTORY_OUT(SoModelMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoBBoxModelMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoBumpMapCoordinateElement)
PIVY_ELEMENT_FACTORY_OUT(SoBumpMapElement)
PIVY_ELEMENT_FACTORY_OUT(SoBumpMapMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoCacheElement)
PIVY_ELEMENT_FACTORY_OUT(SoClipPlaneElement)
PIVY_ELEMENT_FACTORY_OUT(SoComplexityElement)
PIVY_ELEMENT_FACTORY_OUT(SoCoordinateElement)
PIVY_ELEMENT_FACTORY_OUT(SoCreaseAngleElement)
PIVY_ELEMENT_FACTORY_OUT(SoCullElement)
PIVY_ELEMENT_FACTORY_OUT(SoDecimationPercentageElement)
PIVY_ELEMENT_FACTORY_OUT(SoDiffuseColorElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLClipPlaneElement)
PIVY_ELEMENT_FACTORY_OUT(SoLightElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLModelMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoProfileElement)
PIVY_ELEMENT_FACTORY_OUT(SoMultiTextureMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLMultiTextureMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLDrawStyleElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLLightIdElement)
PIVY_ELEMENT_FACTORY_OUT(SoMultiTextureEnabledElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLMultiTextureEnabledElement)
PIVY_ELEMENT_FACTORY_OUT(SoLinePatternElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLLinePatternElement)
PIVY_ELEMENT_FACTORY_OUT(SoSwitchElement)
PIVY_ELEMENT_FACTORY_OUT(SoTextOutlineEnabledElement)
PIVY_ELEMENT_FACTORY_OUT(SoUnitsElement)
PIVY_ELEMENT_FACTORY_OUT(SoFocalDistanceElement)
PIVY_ELEMENT_FACTORY_OUT(SoFontSizeElement)
PIVY_ELEMENT_FACTORY_OUT(SoLineWidthElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLLineWidthElement)
PIVY_ELEMENT_FACTORY_OUT(SoPointSizeElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLPointSizeElement)
PIVY_ELEMENT_FACTORY_OUT(SoTextureQualityElement)
PIVY_ELEMENT_FACTORY_OUT(SoTextureOverrideElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLRenderPassElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLUpdateAreaElement)
PIVY_ELEMENT_FACTORY_OUT(SoLocalBBoxMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoOverrideElement)
PIVY_ELEMENT_FACTORY_OUT(SoPickRayElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLCoordinateElement)
PIVY_ELEMENT_FACTORY_OUT(SoEnvironmentElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLEnvironmentElement)
PIVY_ELEMENT_FACTORY_OUT(SoFontNameElement)
PIVY_ELEMENT_FACTORY_OUT(SoLightAttenuationElement)
PIVY_ELEMENT_FACTORY_OUT(SoPolygonOffsetElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLPolygonOffsetElement)
PIVY_ELEMENT_FACTORY_OUT(SoProjectionMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLProjectionMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoProfileCoordinateElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLMultiTextureImageElement)
PIVY_ELEMENT_FACTORY_OUT(SoViewingMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLViewingMatrixElement)
PIVY_ELEMENT_FACTORY_OUT(SoViewVolumeElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLShapeHintsElement)
PIVY_ELEMENT_FACTORY_OUT(SoShapeStyleElement)
PIVY_ELEMENT_FACTORY_OUT(SoViewportRegionElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLViewportRegionElement)
PIVY_ELEMENT_FACTORY_OUT(SoWindowElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLCacheContextElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLColorIndexElement)
PIVY_ELEMENT_FACTORY_OUT(SoListenerPositionElement)
PIVY_ELEMENT_FACTORY_OUT(SoListenerOrientationElement)
PIVY_ELEMENT_FACTORY_OUT(SoListenerDopplerElement)
PIVY_ELEMENT_FACTORY_OUT(SoListenerGainElement)
PIVY_ELEMENT_FACTORY_OUT(SoSoundElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLVBOElement)
PIVY_ELEMENT_FACTORY_OUT(SoDepthBufferElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLDepthBufferElement)
PIVY_ELEMENT_FACTORY_OUT(SoVertexAttributeElement)
PIVY_ELEMENT_FACTORY_OUT(SoGLVertexAttributeElement)
PIVY_ELEMENT_FACTORY_OUT(SoVertexAttributeBindingElement)
PIVY_ELEMENT_FACTORY_OUT(SoSpecularColorElement)
PIVY_ELEMENT_FACTORY_OUT(SoEmissiveColorElement)
PIVY_ELEMENT_FACTORY_OUT(SoShininessElement)
PIVY_ELEMENT_FACTORY_OUT(SoTransparencyElement)
PIVY_ELEMENT_FACTORY_OUT(SoLightModelElement)
PIVY_ELEMENT_FACTORY_OUT(SoTextureCombineElement)
PIVY_ELEMENT_FACTORY_OUT(SoTextureUnitElement)
PIVY_ELEMENT_FACTORY_OUT(SoCacheHintElement)
