%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec2f, float, 2, 0)
PIVY_SB_VEC_OUTPUT2(float)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec2f {
  SbVec2f __add__(const SbVec2f &u) { return *self + u; }
  SbVec2f __sub__(const SbVec2f &u) { return *self - u; }
  SbVec2f __mul__(const float d) { return *self * d; }
  SbVec2f __rmul__(const float d) { return *self * d; }
  SbVec2f __div__(const float d) { return *self / d; }
  SbVec2f __truediv__(const float d) { return *self / d; }
  int __eq__(const SbVec2f &u ) { return *self == u; }
  int __nq__(const SbVec2f &u) { return *self != u; }
}
