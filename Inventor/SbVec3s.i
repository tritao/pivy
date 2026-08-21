%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec3s, short, 3, 1)
PIVY_SB_VEC_OUTPUT3(short)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec3s {
  SbVec3s __add__(const SbVec3s &u) { return *self + u; }
  SbVec3s __sub__(const SbVec3s &u) { return *self - u; }
  SbVec3s __mul__(const double d) { return *self * d; }
  SbVec3s __rmul__(const double d) { return *self * d; }
  SbVec3s __div__(const double d) { return *self / d; }
  SbVec3s __truediv__(const double d) { return *self / d; }
  int __eq__(const SbVec3s &u) { return *self == u; }
  int __nq__(const SbVec3s &u) { return *self != u; }
}
