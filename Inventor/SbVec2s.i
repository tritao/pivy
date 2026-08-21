%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec2s, short, 2, 1)
PIVY_SB_VEC_OUTPUT2(short)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec2s {
  SbVec2s __add__(const SbVec2s &u) { return *self + u; }
  SbVec2s __sub__(const SbVec2s &u) { return *self - u; }
  SbVec2s __mul__(const double d) { return *self * d; }
  SbVec2s __rmul__(const double d) { return *self * d; }
  SbVec2s __div__(const double d) { return *self / d; }
  SbVec2s __truediv__(const double d) { return *self / d; }
  int __eq__(const SbVec2s &u) { return *self == u; }
  int __nq__(const SbVec2s &u ) { return *self != u; }
}
