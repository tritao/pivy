"""Reviewed Coin/Pivy ownership decisions for the highest-impact boundaries.

The records in this module are deliberately small and source-backed.  They
are not a second type policy: they answer a different question, namely which
layer owns the next improvement for an already identified boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

from tools.pivy_typing.remediation import RemediationClass


ROADMAP_SOURCE = "tools/pivy_typing/coin_api_roadmap.py"


@dataclass(frozen=True)
class CoinApiCandidateReview:
    """Evidence and next-step decision for one ranked Coin method."""

    class_name: str
    method_name: str
    classification: RemediationClass
    native_signatures: tuple[str, ...]
    source_headers: tuple[str, ...]
    evidence: str
    coin4_action: str
    coin5_direction: str
    status: str = "open"

    @property
    def key(self) -> tuple[str, str]:
        return self.class_name, self.method_name

    @property
    def source(self) -> str:
        return ROADMAP_SOURCE


def _review(
    class_name: str,
    method_name: str,
    classification: RemediationClass,
    signature: str,
    header: str,
    evidence: str,
    coin4_action: str,
    coin5_direction: str,
    *,
    status: str = "open",
) -> CoinApiCandidateReview:
    return CoinApiCandidateReview(
        class_name=class_name,
        method_name=method_name,
        classification=classification,
        native_signatures=(signature,),
        source_headers=(header,),
        evidence=evidence,
        coin4_action=coin4_action,
        coin5_direction=coin5_direction,
        status=status,
    )


# These are the reviewed entries from the ranked queue produced by
# report_pivy_binding_friendliness.py.  The review is method-level: all
# incomplete boundaries on an open method inherit the same owner unless a
# future boundary-specific exception is added explicitly.  Resolved entries
# remain here as an auditable record of the binding work that closed them.
COIN_API_CANDIDATE_REVIEWS: tuple[CoinApiCandidateReview, ...] = (
    _review(
        "SoMultiTextureImageElement",
        "get",
        RemediationClass.COIN_API,
        "static const unsigned char *get(SoState *, int, SbVec2s|SbVec3s &, int &, Wrap &, Wrap &, Wrap &, Model &, SbColor &)",
        "Inventor/elements/SoMultiTextureImageElement.h",
        "The result is borrowed pixel storage and the metadata is returned through mutable output references; the native lifetime and extent are not represented by the return value.",
        "Add an additive owning image-snapshot query that returns bytes plus size, component count, wrapping, model and blend color. Keep get() for native callers.",
        "Make the snapshot/value result the preferred API and deprecate the borrowed pointer overloads after downstream users migrate.",
    ),
    _review(
        "SbOctTree",
        "findItems",
        RemediationClass.INTENTIONALLY_NATIVE,
        "void findItems(const SbVec3f|SbBox3f|SbSphere &, SbList<void *> &, SbBool) const",
        "Inventor/SbOctTree.h",
        "The tree stores caller-owned void* items and writes an untyped SbList<void *> supplied by the caller. There is no general Python object ownership or type contract to recover.",
        "Keep this low-level C++ utility native; do not spend typing effort on a generic void* adapter.",
        "If a high-level query is needed, add a separate typed/container API rather than changing the void* ABI.",
    ),
    _review(
        "SoConvexDataCache",
        "generate",
        RemediationClass.PIVY_BINDING,
        "void generate(const SoCoordinateElement *, const SbMatrix &, const int32_t * indices, int, const int32_t * matindices, const int32_t * normindices, const int32_t * texindices, Binding, Binding, Binding)",
        "Inventor/caches/SoConvexDataCache.h",
        "All input arrays carry an explicit count and are consumed by the call. A Pivy wrapper can marshal integer sequences into temporary contiguous buffers without changing Coin ownership semantics.",
        "Add a typed Pivy overload accepting Sequence[int] for each optional index array, with count validation and runtime coverage.",
        "If other bindings need the same conversion, standardize a span/vector overload in Coin while retaining the pointer ABI.",
        status="resolved",
    ),
    _review(
        "SoDB",
        "doSelect",
        RemediationClass.INTENTIONALLY_NATIVE,
        "static int doSelect(int, void * readfds, void * writefds, void * exceptfds, struct timeval *)",
        "Inventor/SoDB.h",
        "This is a select(2)-style platform ABI using fd_set-compatible void pointers and a timeval pointer; it is not a portable Coin value type or a Python event-loop contract.",
        "Keep the ABI boundary native and document a higher-level event-loop integration point instead of typing fd_set pointers.",
        "If modernized, introduce a platform-neutral event polling abstraction as a new API; do not reinterpret the existing doSelect signature.",
    ),
    _review(
        "SoSensorManager",
        "doSelect",
        RemediationClass.INTENTIONALLY_NATIVE,
        "int doSelect(int, void * readfds, void * writefds, void * exceptfds, struct timeval *)",
        "Inventor/sensors/SoSensorManager.h",
        "The method mirrors SoDB.doSelect and exposes the same fd_set/timeval ABI. The native event-loop integration is intentionally platform-specific.",
        "Keep native; expose sensor queue processing through existing typed methods rather than fd-set pointers.",
        "Consider a separate platform-neutral poller only if Coin itself gains one; preserve this compatibility ABI.",
    ),
    _review(
        "SoShapeHintsElement",
        "get",
        RemediationClass.PIVY_BINDING,
        "static void get(SoState *, VertexOrdering &, ShapeType &, FaceType &)",
        "Inventor/elements/SoShapeHintsElement.h",
        "The outputs are three closed enum values and the class already exposes separate typed scalar getters. Pivy can safely provide a tuple or use the scalar getters; no Coin ownership change is required.",
        "Add a Pivy tuple-returning helper and type the three enum outputs from the existing enum policy.",
        "A future Coin convenience overload may return a small value struct, but it is not required for a safe binding.",
        status="resolved",
    ),
    _review(
        "SoWindowElement",
        "get",
        RemediationClass.INTENTIONALLY_NATIVE,
        "static void get(SoState *, void *& window, void *& context, void *& display, SoGLRenderAction *&)",
        "Inventor/elements/SoWindowElement.h",
        "The outputs are platform window-system handles (Window, GLXContext and Display*) represented as void*. Their validity depends on the active rendering backend and context lifetime.",
        "Keep this low-level rendering ABI native; do not expose guessed Python integer or object types.",
        "If a portable rendering handle API is ever added, make it a separate backend-neutral abstraction.",
    ),
    _review(
        "SoWindowElement",
        "set",
        RemediationClass.INTENTIONALLY_NATIVE,
        "static void set(SoState *, void * window, void * context, void * display, SoGLRenderAction *)",
        "Inventor/elements/SoWindowElement.h",
        "The inputs are the same backend-specific window-system handles as get(); Pivy cannot make their ABI portable by changing annotations.",
        "Keep native and require a rendering-backend adapter above this element API.",
        "Prefer a typed rendering-context object in any future Coin API while retaining this ABI for compatibility.",
    ),
    _review(
        "SbFifo",
        "peek",
        RemediationClass.INTENTIONALLY_NATIVE,
        "SbBool peek(void *& item, uint32_t & type) const",
        "Inventor/threads/SbFifo.h",
        "The queue is a thread primitive carrying untyped void* payloads and a caller-defined numeric type tag. A generic Python wrapper cannot establish object lifetime or tag meaning.",
        "Keep native; avoid a misleading Any/object annotation for this ABI primitive.",
        "A future typed queue would need an explicit ownership and payload model, not a signature-only change.",
    ),
    _review(
        "SbFifo",
        "retrieve",
        RemediationClass.INTENTIONALLY_NATIVE,
        "void retrieve(void *& ptr, uint32_t & type)",
        "Inventor/threads/SbFifo.h",
        "The retrieved payload is an untyped void* plus an out type tag, with ownership governed by the caller and queue users.",
        "Keep native and leave this outside the supported typed Python API.",
        "Only replace it with a new typed queue API that defines payload ownership and synchronization semantics.",
    ),
    _review(
        "SbFifo",
        "tryRetrieve",
        RemediationClass.INTENTIONALLY_NATIVE,
        "SbBool tryRetrieve(void *& ptr, uint32_t & type)",
        "Inventor/threads/SbFifo.h",
        "This is the non-blocking form of the same untyped void* queue ABI; the success flag does not solve payload ownership or type interpretation.",
        "Keep native; do not add a weak Python object contract.",
        "A new typed, ownership-aware queue could be introduced independently if a supported use case appears.",
    ),
    _review(
        "SbHeap",
        "traverseHeap",
        RemediationClass.INTENTIONALLY_NATIVE,
        "SbBool traverseHeap(SbBool (*func)(void *, void *), void * userdata) const",
        "Inventor/SbHeap.h",
        "The traversal callback is a C function pointer over untyped heap objects and userdata. It is an ABI callback, not a Python callback contract.",
        "Keep native; do not confuse it with the separately modelled safe Pivy callback adapters.",
        "If needed, add a typed iterator or visitor API with explicit object ownership rather than adapting the function pointer.",
    ),
    _review(
        "SbStorage",
        "__init__",
        RemediationClass.INTENTIONALLY_NATIVE,
        "SbStorage(unsigned int size, cc_storage_f * constr, cc_storage_f * destr)",
        "Inventor/threads/SbStorage.h",
        "The optional constructor/destructor callbacks operate on thread-local native storage and use a C function-pointer ABI.",
        "Keep the callback-taking constructor native; the size-only constructor is already straightforward to type.",
        "A future managed-storage API would need a distinct lifetime model and should not retrofit Python callbacks into this ABI.",
    ),
    _review(
        "SbThread",
        "create",
        RemediationClass.INTENTIONALLY_NATIVE,
        "static SbThread * create(void *(*func)(void *), void * closure)",
        "Inventor/threads/SbThread.h",
        "Thread entry and closure are raw C function pointers and void* data crossing a native thread boundary; Python interpreter lifetime and GIL rules are not represented.",
        "Keep native; use a Python threading/executor layer for Python work.",
        "If Coin offers managed task execution later, make it a new API with explicit interpreter/runtime integration.",
    ),
    _review(
        "SbThread",
        "join",
        RemediationClass.INTENTIONALLY_NATIVE,
        "SbBool join(SbThread *, void ** retval = 0L)",
        "Inventor/threads/SbThread.h",
        "The optional result is a void** from a native thread entry point and has no portable Python value or ownership contract.",
        "Keep native and avoid exposing the result as an untyped Python object.",
        "A managed task API could return a typed future/result, while this ABI remains unchanged.",
    ),
    _review(
        "SbTime",
        "getValue",
        RemediationClass.PIVY_BINDING,
        "void getValue(time_t & sec, long & usec) const; void getValue(struct timeval * tv) const",
        "Inventor/SbTime.h",
        "The scalar result is a pair of ordinary time values and the timeval overload is a platform struct. Pivy can expose a typed (seconds, microseconds) result without changing Coin.",
        "Add a Pivy helper returning tuple[int, int] and keep the timeval overload explicitly native.",
        "If Coin adds a value-returning duration/timestamp type, prefer it for new code while retaining the ABI overloads.",
        status="partial",
    ),
    _review(
        "SoFieldContainer",
        "getFieldsMemorySize",
        RemediationClass.PIVY_BINDING,
        "virtual void getFieldsMemorySize(size_t & managed, size_t & unmanaged) const",
        "Inventor/fields/SoFieldContainer.h",
        "Both outputs are scalar sizes with no borrowed storage or ownership issue. The missing Python shape is a binding output-tuple adapter.",
        "Expose a typed Pivy helper returning tuple[int, int] and retain the native output-reference method for compatibility.",
        "A Coin value struct would be a convenience only; it is not necessary to make this API bindable.",
        status="resolved",
    ),
    _review(
        "SoGLMultiTextureImageElement",
        "get",
        RemediationClass.INTENTIONALLY_NATIVE,
        "static SoGLImage * get(SoState *, int, Model &, SbColor &)",
        "Inventor/elements/SoGLMultiTextureImageElement.h",
        "The return is a borrowed backend-specific SoGLImage pointer and the query requires an active OpenGL state/context.",
        "Keep native; do not promise a Python-owned GL image from this element query.",
        "If a portable GPU-resource API is needed, introduce an owning/render-backend abstraction separately from this element ABI.",
    ),
    _review(
        "SoInput",
        "read",
        RemediationClass.PIVY_BINDING,
        "virtual SbBool read(int & i); virtual SbBool read(SbString & s)",
        "Inventor/SoInput.h",
        "The selected overloads write scalar or SbString values and return success. Pivy can wrap them as typed value-returning operations; no native pointer lifetime is involved.",
        "Add typed Pivy read helpers or overload policies returning (ok, value), while leaving binary-array and char-pointer APIs native.",
        "A Coin value-returning parser API would improve all bindings, but is an additive convenience rather than a prerequisite.",
        status="resolved",
    ),
    _review(
        "SoLinearProfile",
        "getTrimCurve",
        RemediationClass.COIN_API,
        "virtual void getTrimCurve(SoState *, int32_t & numpoints, float *& points, int & floatspervec, int32_t & numknots, float *& knotvector)",
        "Inventor/nodes/SoLinearProfile.h",
        "The method returns two variable-length borrowed float arrays through pointer-to-pointer outputs. Counts and vector shape are separate, and ownership/lifetime are not expressed by the result.",
        "Add an additive owning trim-curve result containing points, floats-per-vector and knot vector; keep the pointer ABI for native callers.",
        "Make the owning result the preferred API and retire the pointer-output form only in a future breaking release.",
    ),
)


REVIEWS_BY_KEY = {review.key: review for review in COIN_API_CANDIDATE_REVIEWS}


def coin_api_candidate_review(
    class_name: str, method_name: str | None
) -> CoinApiCandidateReview | None:
    """Return the reviewed candidate for a class/method boundary, if any."""

    if method_name is None:
        return None
    return REVIEWS_BY_KEY.get((class_name, method_name))


__all__ = [
    "COIN_API_CANDIDATE_REVIEWS",
    "CoinApiCandidateReview",
    "REVIEWS_BY_KEY",
    "ROADMAP_SOURCE",
    "coin_api_candidate_review",
]
