%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec3d, double, 3, 0)
PIVY_SB_VEC_OUTPUT3(double)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec3d {
  SbVec3d __add__(const SbVec3d &u) { return *self + u; }
  SbVec3d __sub__(const SbVec3d &u) { return *self - u; }
  SbVec3d __mul__(const double d) { return *self * d; }
  SbVec3d __mul__(const SbDPMatrix &m) { SbVec3d res; m.multVecMatrix(*self,res); return res; }
  SbVec3d __rmul__(const double d) { return *self * d; }
  SbVec3d __div__(const double d) { return *self / d; }
  SbVec3d __truediv__(const double d) { return *self / d; }
  int __eq__(const SbVec3d &u) { return *self == u; }
  int __nq__(const SbVec3d &u) { return *self != u; }
}
