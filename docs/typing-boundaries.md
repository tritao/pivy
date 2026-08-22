# Intentional `Incomplete` typing boundaries

`Incomplete` is a reviewed boundary, not a quality score by itself. The
category policy in `tools/pivy_stub_typing_policy.py` is the source of truth;
the quality report prints its disposition and current count. The report must
keep `uncategorized` at zero.

The exact dynamic/runtime inventory lives in `TRIAGED_INCOMPLETE_SITES`, while
special cases are recorded in `INCOMPLETE_CATEGORY_OVERRIDES`. New sites must
be covered by one of those explicit rules or by a safe Python-level adapter.

## Review dispositions

### raw C pointers

Disposition: intentional

SWIG exposes a borrowed pointer or ABI-level pointer without a stable Python
owner.

Keep these sites `Incomplete` until the binding can copy the data or expose an
owning Python object with a documented lifetime. `SbImage.getValue` and
`SoOffscreenRenderer.getBuffer` demonstrate the preferred direction: add a
runtime adapter that snapshots the buffer, then type the Python value.

### callbacks

Disposition: intentional

The native callback boundary still needs an explicit Python lifecycle and
ownership contract.

Use a `Protocol` when the callback signature is known. Keep the boundary
`Incomplete` when native registration, retention, or teardown semantics are
not yet safely represented.

### unknown output parameters

Disposition: zero budget

Output parameters must be represented by a typed return tuple or helper before
they are accepted.

This category is a regression guard: a new output-parameter site needs a
binding adapter or a policy entry before it can merge.

### function pointers

Disposition: intentional

A native C function-pointer ABI is not directly callable as a safe Python
value.

Expose a typed `Callable` only when the binding adapts invocation and lifetime;
otherwise document the native-only boundary explicitly.

### dynamic/runtime API

Disposition: intentional

Dynamic factories, opaque objects, and runtime field storage cannot be
recovered from a static declaration alone.

The report separates runtime factory returns, opaque pointer/object returns,
opaque parameter boundaries, and opaque field storage so each group has a
concrete follow-up. Promote a site when runtime behavior becomes stable enough
to model.

### uncategorized

Disposition: zero budget

Every remaining Incomplete site must have a reviewed category.

An uncategorized site is a typing hole, not an intentional boundary. The
report and policy tests fail until it is adapted, added to an explicit rule, or
otherwise resolved.

## Checking the boundary policy

```bash
pixi run typecheck_report
pixi run test_typing_policy
```

Use `--show-category` on `tools.report_pivy_typing` to inspect the individual
sites behind a category.
