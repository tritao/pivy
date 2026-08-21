%include Inventor/SbVecCommon.i
PIVY_SB_VEC(SbVec4f, float, 4, 0)
PIVY_SB_VEC_OUTPUT4(float)

%ignore SbVec2d::__imul__;

/* add operator overloading methods instead of the global functions */
%extend SbVec4f {
  SbVec4f __add__(const SbVec4f &u) { return *self + u; }
  SbVec4f __sub__(const SbVec4f &u) { return *self - u; }
  SbVec4f __mul__(const float d) { return *self * d; }
  SbVec4f __mul__(const SbMatrix &m) { SbVec4f res; m.multVecMatrix(*self,res); return res; }
  SbVec4f __rmul__(const float d) { return *self * d; }
  SbVec4f __div__(const float d) { return *self / d; }
  SbVec4f __truediv__(const float d) { return *self / d; }
  int __eq__(const SbVec4f &u) { return *self == u; }
  int __nq__(const SbVec4f &u) { return *self != u; }
}
