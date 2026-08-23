# Pivy typing architecture plan

## Direction

Do not design around SWIG 4.5 yet. Evolve the current typing branch until
SWIG 4.5 is another producer that can be compared with Pivy's canonical API
model, rather than a dependency that forces an architectural rewrite.

The target architecture is:

```text
stubgen output ──> semantic API model ──> Pivy typing policy
                                             │
                                             ▼
                                      resolved typed model
                                       /       |        \
                                      ▼        ▼         ▼
                                  .pyi     validator   report
                                renderer
```

Later, an experimental SWIG 4.5 output should enter through a separate parser
and be compared semantically with the resolved Pivy model:

```text
SWIG 4.5 output ──> semantic comparison <── current Pivy model
```

## Non-negotiable invariants

1. The current Python API semantics remain the reference.
2. Architecture-only refactors must produce byte-for-byte identical public
   stubs.
3. A PR that intentionally changes typing semantics must say so explicitly
   and update the relevant runtime, static, compatibility, and quality tests.
4. The current generator remains the source of behavior until an equivalent
   semantic-model pipeline is proven.
5. Do not replace SWIG, migrate packaging, redesign CMake, or solve SoQt as
   part of this architecture work.
6. Keep policy metadata in Python; do not invent a YAML or custom `.i` DSL.

## Migration phases

### Phase 0 — Freeze today's semantics

Document the current API invariants and make the existing gates the baseline:

- Coin and SoQt runtime tests
- stub validation
- Pyright and Pyrefly checks
- strict and negative typing tests
- compatibility snapshot
- stubtest
- stub drift and determinism checks
- field-coverage checks
- typing-quality and verifytypes reports

Architecture-only PRs must prove that generated public stubs are unchanged.

### Phase 1 — Introduce a semantic API model

Add a small, deliberately boring model under `tools/pivy_typing/`:

```text
tools/pivy_typing/
    model.py
```

Start with dataclasses for:

- `Module`
- `Class`
- `Method`
- `Overload`
- `Parameter`
- `Attribute`
- `TypeExpr`

`TypeExpr` can initially hold normalized text. The first implementation must
parse the existing stubgen result into the model and render output that is
byte-for-byte identical to today's stubs.

### Phase 2 — Split the generator into pipeline stages

Refactor `tools/generate_pivy_stubs.py` into explicit stages:

```text
tools/pivy_typing/
    model.py
    parse_stubgen.py
    normalize.py
    policy.py
    render_pyi.py
```

The top-level generator should become orchestration:

```python
raw = parse_stubgen(...)
model = normalize(raw)
model = apply_pivy_policy(model)
render_pyi(model)
```

Parsing, policy, and rendering must be replaceable independently. No typing
semantic changes belong in this refactor.

### Phase 3 — Structure policy rules

Keep the existing Python policy system, but gradually replace opaque tuples
with structured rules. For example:

```python
ParameterRule(
    target=Symbol(
        class_name="SoDepthBufferElement",
        method="get",
        parameter="function_out",
    ),
    python_type="intp",
    reason="SbBool& output uses a scalar pointer helper",
    source="Inventor/elements/SoDepthBufferElement.i",
)
```

Rules should carry, where applicable:

- target symbol
- resolved Python type
- reason
- binding source
- ownership or lifetime implications
- proposed remediation

The existing canonical registries, such as `pivy_factory_registry.py`, are
the model for this direction.

### Phase 4 — Organize policy by ownership

Separate generic semantic knowledge from Pivy binding-specific behavior:

```text
tools/pivy_typing/policy/
    primitives.py
    vectors.py
    matrices.py
    fields.py
    multifields.py
    callbacks.py
    factories.py
    boundaries.py
    overrides/
        actions.py
        sensors.py
        selection.py
        images.py
        soqt.py
```

Generic rules such as `int32_t -> int` belong centrally. Rules describing
Python retention, callback userdata, ownership, or a Pivy-specific adapter
belong with the relevant binding domain and should record their `.i` source.

Do not create a new metadata language before upstream SWIG mechanisms are
understood.

### Phase 5 — Remove duplicated structural validation

Use the resolved semantic model to derive structural expectations such as:

- parameter and return annotations
- overloads
- iterator element types
- field attribute types
- factory return types

Remove duplicate expected-signature databases from
`pivy_stub_validation_data.py` where the expectation is already represented by
the policy/model.

Keep handwritten runtime tests for independent behavioral evidence:

- callbacks can be registered and removed
- userdata is retained and returned correctly
- callback lifetime is safe
- factories return concrete subclasses with correct ownership
- sequence overloads accept the promised Python values

### Phase 6 — Make `Incomplete` semantic

Represent intentional boundaries in the resolved model instead of discovering
them from rendered `.pyi` text:

```python
IncompleteType(
    category=BoundaryCategory.RAW_POINTER,
    reason="borrowed native pointer without a stable Python lifetime",
    source="Inventor/.../SomeBinding.i",
)
```

The renderer emits `Incomplete`; reports and validators consume the model's
category and rationale directly. The `UNKNOWN`/uncategorized budget remains
zero, while intentional raw, callback, function-pointer, and dynamic
boundaries may remain until a safe adapter exists.

### Phase 7 — Model callback contracts

Give callbacks a first-class contract containing the information needed to
decide whether a Python annotation is truthful:

```python
CallbackContract(
    protocol="SoSensorCallback",
    parameters=(...),
    return_type="None",
    userdata=True,
    retention=Retention.PROXY_LIFETIME,
    removal=Removal.IDENTITY,
    nullable=False,
)
```

Not every field must affect `.pyi`, but the contract should distinguish a
Python-safe callback adapter from a native function-pointer boundary.

### Phase 8 — Emit a canonical typing manifest

Add a task such as:

```bash
pixi run typecheck_manifest
```

which writes a machine-readable manifest, for example:

```text
build/typing/pivy-api.json
```

The manifest should record symbols, parameters, overloads, returns,
attributes, boundary categories, provenance, and reasons. It is the
backend-neutral API snapshot used for semantic comparison; formatting and
stub import order must not matter.

### Phase 9 — Make the current renderer disposable

The final architecture should be:

```text
raw producer output
        │
        ▼
      parser
        │
        ▼
 semantic model
        │
        ▼
   Pivy policy
        │
        ▼
 resolved API model
    /       |        \
   ▼        ▼         ▼
.pyi    manifest    reports
```

The `.pyi` renderer should contain syntax-generation logic only. It must not
own the semantic rules that define Pivy's Python API.

## SWIG 4.5 experiment

Only after the backend-neutral baseline is stable:

1. Generate an experimental stub with SWIG 4.5.
2. Parse it into the same semantic model.
3. Normalize equivalent type spellings.
4. Compare it with the canonical Pivy manifest.
5. Classify differences as equivalent, generic typemap work,
   binding-specific metadata, intentional boundaries, or SWIG mismatches.
6. Decide from measured differences whether any current backend should be
   replaced.

The experiment must not change the current production generator or public
typing contract by itself.

## Mergeable PR sequence

1. Refactor generator into parse → model → policy → render with byte-identical
   stubs.
2. Introduce structured policy rule classes without semantic changes.
3. Split generic policy from binding-specific overrides and add provenance.
4. Model `Incomplete` boundaries explicitly and simplify the quality report.
5. Derive structural validator expectations from the resolved model.
6. Model callbacks and factories as semantic contracts, retaining independent
   runtime tests.
7. Add the canonical JSON manifest and semantic-diff tooling.
8. Shrink compatibility and generator-specific legacy layers.
9. Declare the result the backend-neutral typing baseline.
10. Begin the SWIG 4.5 comparison experiment.

## Current branch status

Already established before this plan:

- measurable typing-quality and verifytypes reports
- canonical policy and factory registries
- compatibility, drift, determinism, and field-coverage gates
- safe Coin field and callback adapters validated at runtime
- typed `SoMFDouble` sequence semantics
- typed remaining Coin ScXML factories
- cleanup of leaked module-local names

Phase 1 is now implemented on this branch:

- `tools/pivy_typing/model.py` records classes, methods, overloads, parameters,
  annotations, defaults, decorators and annotated attributes.
- The production generator parses every postprocessed stub through that model.
- The compatibility renderer returns the retained source unchanged, so the
  generated Coin and SoQt stubs remain byte-for-byte identical.
- `tests/test_pivy_typing_model.py` covers full-stub round trips and signature
  details, and CMake tracks the model as a stub-generation dependency.

Phase 2 is also now in place as a mechanical pipeline boundary:

- raw stubgen reads are represented by `StubgenOutput`;
- named normalization and policy stages run through a shared pipeline;
- the compatibility `.pyi` renderer is a distinct final stage;
- stage-order tests, stub drift, determinism and lint all pass with no public
  stub changes.

The next implementation slice is Phase 3: replace the remaining unstructured
policy tuples with typed rule objects carrying target and provenance metadata.

Phase 3 has started with the highest-impact exceptional signature maps:

- method-return overrides and Python parameter overrides now have structured
  `PolicyTarget`/`OverrideRule` entries;
- legacy dictionaries remain derived compatibility views for existing
  generator consumers;
- tests assert the structured rules and compatibility views cannot drift.

The scalar-pointer, scalar-reference, sequence, fixed-width boolean-array and
matrix parameter maps now use the same rule representation as well. The
remaining Phase 3 work is to migrate the other exceptional factory/callback
maps where doing so clarifies ownership rather than just wrapping generic
type tables.

Phase 4 has begun by attaching an explicit `PolicyOwner` to structured rules.
The current classification distinguishes Coin and SoQt domains without moving
files or changing generated output; that gives the next refactor a safe seam
for splitting policy by binding ownership instead of by generator operation.
