%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec2d, double, 2, 0)
PIVY_SB_VEC_OUTPUT2(double)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec2d {
  SbVec2d __add__(const SbVec2d &u) { return *self + u; }
  SbVec2d __sub__(const SbVec2d &u) { return *self - u; }
  SbVec2d __mul__(const float d) { return *self * d; }
  SbVec2d __rmul__(const float d) { return *self * d; }
  SbVec2d __div__(const float d) { return *self / d; }
  SbVec2d __truediv__(const float d) { return *self / d; }
  int __eq__(const SbVec2d &u ) { return *self == u; }
  int __nq__(const SbVec2d &u) { return *self != u; }
}
