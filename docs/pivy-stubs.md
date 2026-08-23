# Pivy Stubs

## Editor and Checker Smoke Test

The generated `pivy.coin` and `pivy.gui.soqt` `.pyi` files are committed next
to the package so editors can use them directly from a checkout. After pixi has
created the environment, VS Code can use the checked-in `.vscode` workspace
settings directly. Open the repository root, install the recommended Python and
Pylance extensions when prompted, and use
`Terminal > Run Task... > Pivy: typecheck stubs`.

The workspace points the Python extension at the pixi environment:

- POSIX: `.pixi/envs/default/bin/python`
- Windows: `.pixi\envs\default\python.exe`

Pyright/Pylance should then resolve `from pivy import coin` and
`from pivy.gui import soqt` from the committed stubs. The same smoke check can
be run without an editor:

```sh
pixi run typecheck_stubs
```

That task runs both:

```sh
pixi run typecheck_stubs_pyright
pixi run typecheck_stubs_pyrefly
```

`pixi run test_stubs` still validates the generated build stubs, runs the mypy
import check, and compares the generated files against the committed source
stubs to catch drift.

## Stub TODOs

## Runtime-Unsupported SWIG Surfaces

The generated `.pyi` files intentionally leave some APIs as `Incomplete` when
the current SWIG wrapper exposes a raw C pointer surface instead of a normal
Python value. These should not be typed as `Callable`, `Sequence`, or `Any`
until the binding grows a Python-level wrapper or typemap.

Known callback-pointer surfaces:

- `SoDB.getHeaderData`
- `SoGLImage.setEndFrameCallback`

The four error-handler setters use a SWIG-side adapter and accept a Python
callable with `(userdata, SoError)` arguments. The getter methods return the
retained Python callable and data when the handler was installed through Pivy,
and `None` for native handlers that Pivy cannot represent as Python objects.

Sensor constructors and the `SoSensor.setFunction`/`SoSensor.setData`/
`SoDataSensor.setDeleteCallback` setters use the existing SWIG-side sensor
adapter. They retain the Python callback and userdata together, so the getter
surface remains consistent when applications update either value separately.

`SoDB.registerHeader` and the progress callback registration methods use SWIG
adapters and accept Python callables with `(userdata, SoInput)` and
`(userdata, SbName, fraction, interruptible)` arguments respectively. Header
output callback pointers remain intentionally incomplete.

The public SoQt callback surface is typed where the SWIG wrapper accepts a
Python callable: fatal-error handlers, component window-close callbacks,
viewer start/finish and auto-clipping callbacks, and popup-menu callbacks.
The viewer/component callbacks use reusable protocols tied to their SoQt
receiver type; the remaining callback signatures use `Callable` annotations.

`SoSFImage` and `SoSFImage3` expose their pixel data through Python tuples of
`(str, size, component_count)` for `getValue()` and `startEditing()`. Their
pixel setters accept the strings or bytes used by the existing SWIG typemaps.

`SoCallbackList` uses Python shadow methods for callback registration and
accepts `(userdata, callbackdata)` callables. Callback data is passed as the
same Python object supplied to `invokeCallbacks`.

`SoContextHandler` uses SWIG adapters for context destruction callbacks and
accepts `(userdata, contextid)` callables. The callback registration and
removal methods match callbacks by Python object identity.

`SoGLRenderAction.setSortedObjectOrderStrategy` accepts an optional
`(userdata, SoGLRenderAction) -> float` callback. The callback closure is kept
alive by the action and is cleared when a non-callback strategy is selected.

`SoGLCacheContextElement.scheduleDeleteCallback` accepts a
`(userdata, contextid) -> None` callback. Its Python closure is retained until
Coin dispatches the scheduled deletion callback, then released.

`SoGLImage.setEndFrameCallback` accepts `(userdata) -> None`, while
`SoShaderProgram.setEnableCallback` accepts
`(userdata, SoState, enabled) -> None`. Both retain their callback closures on
the Python proxy and accept `None` to clear the native callback.

`SoProto.setFetchExternProtoCallback` accepts
`(userdata, SoInput, urls, numurls) -> SoProto | None`. The URL array is
presented as a Python list of borrowed `SbString` proxies, and the static
callback closure is retained until replaced or cleared.

`SbImage.addReadImageCB` and `removeReadImageCB` accept
`(userdata, filename, image) -> bool` callbacks. Registration and removal use
Python callback and userdata identity, and the retained closure is released on
removal.

`SbImage.scheduleReadFile` uses the same callback contract and releases the
retained closure after the scheduled read callback runs or the schedule fails.

`SoDragger` callback registration and removal methods use the same
`(userdata, SoDragger)` contract. Their Python closures are retained on the
dragger proxy, and removal matches the callback and userdata by identity.

`SoSelection` path and selection callbacks use `(userdata, SoPath)` or
`(userdata, SoSelection)` contracts. Their registration/removal closures are
retained on the selection proxy and matched by callback and userdata identity;
the pick-filter closure is retained while it is installed.

`SoExtSelection` filter setters expose typed lasso, triangle, line-segment, and
point callbacks. Their closures are retained while installed, and passing
`None` clears each native filter callback.

Known pointer-buffer surfaces:

- `SoMFDouble.getValues` remains a raw native pointer API. `getValuesSnapshot()`
  and sequence-based `setValues(...)` calls are bounded Python adapters;
  `_pivy_setValuesRaw` preserves the escape hatch for native pointer callers.

Resolved binding-backed surfaces:

- Class-specific static `createInstance()` methods for Coin elements and
  fields now return owned, concrete wrappers through SWIG typemaps.

High-volume `Incomplete` clusters that still need SWIG-side work:

- Raw callback registration tables and function-pointer fields, including
  `addMethod` action dispatch hooks, `SoActionMethodList`, `SbHeapFuncs`, and
  `SbOctTreeFuncs`.
- Raw `FILE *`, buffer, and select-loop entry points such as `output`,
  `SoInput.setFilePointer`, `SoOutput.setFilePointer`, binary array readers,
  and binary array writers.
- Image and texture byte-buffer APIs such as `SbImage`, `SoSFImage`,
  `SoSFImage3`, and `SoMultiTextureImageElement`.

Representative surfaces now validator-guarded to stay `Incomplete`:

- Callback and function-table surfaces:
  `SoActionMethodList.{addMethod,__setitem__,__getitem__,get}`,
  `SbHeapFuncs.*`, and `SbOctTreeFuncs.*`.
- Raw file and buffer surfaces:
  `SoInput.{setFilePointer,getCurFile,setBuffer,readBinaryArray}`,
  `SoOutput.{setFilePointer,getFilePointer,setBuffer,getBuffer}`.
- Raw image and texture byte buffers:
  `SbImage.{__init__,addReadImageCB,scheduleReadFile,getValue}`,
  `SoSFImage.{startEditing,setValue}`,
  `SoSFImage3.{getValue,startEditing,setValue}`,
  `SoMultiTextureImageElement.{getDefault,set,get}`.
- Abstract storage surfaces:
  `SoMField.values`, `SbHeap.{add,extractMin,buildHeap}`,
  and `SbOctTree.{addItem,findItems}`.

## Remaining By-Reference Gaps

Some non-const reference parameters are now split into two buckets:

- Helper-backed refs that the current wrapper already accepts through pointer
  proxy classes. These are typed in `.pyi` today, for example `charp`,
  `intp`, `floatp`, `doublep`, `longp`, and `SbBool &` via `intp`.
- Reference params that still have no honest Python helper surface. These now
  stay `Incomplete` instead of pretending to be plain `int` or `bool`.

Representative unsupported scalar-ref surfaces:

- `SbTime.getValue(time_t & sec, long & usec)`
- `SoInput.readHex(uint32_t & l)`
- `SoInput.read(unsigned int & i)`
- `SoInput.read(short & s)`
- `SoInput.read(unsigned short & s)`
- short/unsigned-short box and vector out-params such as
  `SbBox2s.getBounds(...)` and `SbVec4us.getValue(...)`

Representative unsupported enum-ref surfaces:

- `SoPolygonOffsetElement.{get,getDefault}` with `Style &`
- `SoShapeHintsElement.get(...)` with shape-hint enum refs
- `SoMultiTextureImageElement.get(...)` with `Wrap &` and `Model &`

The current binding now exposes `SoOutput.getAvailableCompressionMethods()`
through the `uintp` helper and adapts `SoDepthBufferElement.get()` to use
`intp` for its enum output. The remaining pointer-to-pointer surfaces are
still deliberately deferred:

- `SoAction.{getPathCode,usePathCode}` and `SoFieldData.getEnumData()` expose
  raw `const int *` output pointers.
- `SoSensorManager.doSelect()` and `SoDB.doSelect()` expose platform
  `timeval *` pointers.

TODO: add SWIG typemaps or Python wrapper helpers for these families before
tightening the stubs. Until then, `Incomplete` is the least misleading type.

Known fixed-width integer array surfaces:

- `SbVec2b`, `SbVec2i32`, `SbVec3b`, `SbVec3i32`, `SbVec4b`, `SbVec4ub`,
  `SbVec4s`, `SbVec4us`, `SbVec4i32`, and `SbVec4ui32` sequence constructors
  and `setValue` overloads
- `SbMatrix.LUDecomposition`
- `SbDPMatrix.LUDecomposition`
- `SoSFVec2s.setValue`
- `SoSFVec3s.setValue`
- `SoMFVec2s.set1Value`
- `SoMFVec2s.setValue`
- `SoMFVec3s.set1Value`
- `SoMFVec3s.setValue`

TODO: Add SWIG-side support before tightening these stubs. For callbacks, add
explicit Python-callable overloads or typemaps that retain the callback and
userdata safely. For fixed-width integer arrays, add
typemaps that accept Python integer sequences for the wrapped C array overloads.
