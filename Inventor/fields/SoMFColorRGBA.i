%include Inventor/fields/SoMFVecCommon.i

PIVY_SOMFVEC(
  SoMFColorRGBA,
  SbColor4f,
  float,
  rgba,
  4,
  SoMFColorRGBA_setValues
)

%extend SoMFColorRGBA {
  void __setitem__(int i, const float rgba[4]) {
    self->set1Value(i, rgba);
  }
}
