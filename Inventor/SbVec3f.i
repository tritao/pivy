%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec3f, float, 3, 0)
PIVY_SB_VEC_OUTPUT3(float)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec3f {
  SbVec3f __add__(const SbVec3f &u) { return *self + u; }
  SbVec3f __sub__(const SbVec3f &u) { return *self - u; }
  SbVec3f __mul__(const float d) { return *self * d; }
  SbVec3f __mul__(const SbMatrix &m) { SbVec3f res; m.multVecMatrix(*self,res); return res; }
  SbVec3f __rmul__(const float d) { return *self * d; }
  SbVec3f __div__( const float d) { return *self / d; }
  SbVec3f __truediv__( const float d) { return *self / d; }
  int __eq__(const SbVec3f &u ) { return *self == u; }
  int __nq__(const SbVec3f &u) { return *self != u; }
}
