%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec4d, double, 4, 0)
PIVY_SB_VEC_OUTPUT4(double)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec4d {
  SbVec4d __add__(const SbVec4d &u) { return *self + u; }
  SbVec4d __sub__(const SbVec4d &u) { return *self - u; }
  SbVec4d __mul__(const double d) { return *self * d; }
  SbVec4d __mul__(const SbDPMatrix &m) { SbVec4d res; m.multVecMatrix(*self,res); return res; }
  SbVec4d __rmul__(const double d) { return *self * d; }
  SbVec4d __div__(const double d) { return *self / d; }
  SbVec4d __truediv__(const double d) { return *self / d; }
  int __eq__(const SbVec4d &u ) { return *self == u; }
  int __nq__(const SbVec4d &u) { return *self != u; }
}
