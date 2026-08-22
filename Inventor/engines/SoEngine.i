/* add generic interface to access outputs as attributes */
%extend SoEngine {
%pythoncode %{
    def __getattr__(self, name):
        try:
            return SoFieldContainer.__getattr__(self, name)
        except AttributeError as e:
            ##############################################################
            if name == "this":
                raise AttributeError
            ##############################################################
            out = self.getOutput(SbName(name))
            if out is None:
                raise e
            return out
    
    def __setattr__(self,name,value):
        if name == 'this':
            return SoFieldContainer.__setattr__(self, name, value)
        out = self.getOutput(SbName(name))
        if out is None:
            return SoFieldContainer.__setattr__(self, name, value)
        raise AttributeError('Cannot set output %s on engine %s' %(name,self.__class__.__name__))
        
%}
}

/* Coin's engine macros expose these factories as void *.  The factory always
   creates a new engine, so autocast it to the concrete Python class and
   transfer ownership to the returned wrapper. */
%define PIVY_ENGINE_FACTORY_OUT(_class_)
%typemap(out) void * _class_::createInstance {
  $result = autocast_base((SoBase *)$1, 1);
}
%enddef

PIVY_ENGINE_FACTORY_OUT(SoBoolOperation)
PIVY_ENGINE_FACTORY_OUT(SoCalculator)
PIVY_ENGINE_FACTORY_OUT(SoComposeVec2f)
PIVY_ENGINE_FACTORY_OUT(SoComposeVec3f)
PIVY_ENGINE_FACTORY_OUT(SoComposeVec4f)
PIVY_ENGINE_FACTORY_OUT(SoDecomposeVec2f)
PIVY_ENGINE_FACTORY_OUT(SoDecomposeVec3f)
PIVY_ENGINE_FACTORY_OUT(SoDecomposeVec4f)
PIVY_ENGINE_FACTORY_OUT(SoComposeRotation)
PIVY_ENGINE_FACTORY_OUT(SoDecomposeRotation)
PIVY_ENGINE_FACTORY_OUT(SoComposeMatrix)
PIVY_ENGINE_FACTORY_OUT(SoDecomposeMatrix)
PIVY_ENGINE_FACTORY_OUT(SoComposeRotationFromTo)
PIVY_ENGINE_FACTORY_OUT(SoComputeBoundingBox)
PIVY_ENGINE_FACTORY_OUT(SoConcatenate)
PIVY_ENGINE_FACTORY_OUT(SoCounter)
PIVY_ENGINE_FACTORY_OUT(SoElapsedTime)
PIVY_ENGINE_FACTORY_OUT(SoGate)
PIVY_ENGINE_FACTORY_OUT(SoInterpolateFloat)
PIVY_ENGINE_FACTORY_OUT(SoInterpolateVec2f)
PIVY_ENGINE_FACTORY_OUT(SoInterpolateVec3f)
PIVY_ENGINE_FACTORY_OUT(SoInterpolateVec4f)
PIVY_ENGINE_FACTORY_OUT(SoInterpolateRotation)
PIVY_ENGINE_FACTORY_OUT(SoOnOff)
PIVY_ENGINE_FACTORY_OUT(SoOneShot)
PIVY_ENGINE_FACTORY_OUT(SoSelectOne)
PIVY_ENGINE_FACTORY_OUT(SoTimeCounter)
PIVY_ENGINE_FACTORY_OUT(SoTransformVec3f)
PIVY_ENGINE_FACTORY_OUT(SoTriggerAny)
PIVY_ENGINE_FACTORY_OUT(SoHeightMapToNormalMap)
PIVY_ENGINE_FACTORY_OUT(SoVRMLColorInterpolator)
PIVY_ENGINE_FACTORY_OUT(SoVRMLCoordinateInterpolator)
PIVY_ENGINE_FACTORY_OUT(SoVRMLNormalInterpolator)
PIVY_ENGINE_FACTORY_OUT(SoVRMLOrientationInterpolator)
PIVY_ENGINE_FACTORY_OUT(SoVRMLPositionInterpolator)
PIVY_ENGINE_FACTORY_OUT(SoVRMLScalarInterpolator)
PIVY_ENGINE_FACTORY_OUT(SoVRMLTimeSensor)
