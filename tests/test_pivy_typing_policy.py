import re
import json
import unittest
from dataclasses import replace
from pathlib import Path

import tools.pivy_stub_generation_data as compatibility_policy
from tools.pivy_factory_registry import (
    ENGINE_FACTORY_CLASS_NAMES,
    SCXML_FACTORY_CLASSES,
    SCXML_FACTORY_CLASS_NAMES,
    SCXML_UNSUPPORTED_FACTORY_CLASS_NAMES,
)
import tools.pivy_stub_typing_policy as policy
from tools.check_pivy_typing_matrix import SUPPORTED_PYTHON_VERSIONS
from tools.report_pivy_typing import (
    TYPING_QUALITY_BASELINE,
    collect_report,
    opaque_return_audit_issues,
    opaque_return_audit_summary,
    quality_regressions,
    report_to_dict,
)
from tools.check_pivy_policy_coverage import policy_coverage_errors
from tools.pivy_stub_typing_policy import (
    FACTORY_CLASSES,
    ENGINE_FACTORY_CLASSES,
    FIELD_TYPE_POLICIES,
    INCOMPLETE_CATEGORIES,
    INCOMPLETE_CATEGORY_ACTIONS,
    INCOMPLETE_CATEGORY_POLICIES,
    factory_method_return_type,
    MULTIFIELD_TYPE_POLICIES,
    classify_incomplete,
    field_method_type_overrides,
    multifield_component_sequence_types,
    multifield_getvalues_types,
    multifield_iter_element_types,
    multifield_single_value_types,
    multifield_setvalues_types,
    vector_iter_element_types,
    vector_output_parameter_types,
    vector_multifield_type_policies,
    vector_sequence_array_parameters,
    vector_value_return_types,
)


class FieldTypePolicyTests(unittest.TestCase):
    def test_engine_factory_policy(self):
        self.assertEqual(len(ENGINE_FACTORY_CLASSES), 37)
        self.assertEqual(set(ENGINE_FACTORY_CLASS_NAMES), ENGINE_FACTORY_CLASSES)
        self.assertTrue(
            {
                "SoBoolOperation",
                "SoComposeVec3f",
                "SoVRMLTimeSensor",
            }.issubset(ENGINE_FACTORY_CLASSES)
        )
        self.assertTrue(ENGINE_FACTORY_CLASSES.issubset(FACTORY_CLASSES))

    def test_image_field_python_surfaces(self):
        self.assertEqual(
            policy.METHOD_RETURN_TYPE_OVERRIDES[("SoSFImage", "getValue")],
            "tuple[str, SbVec2s, int]",
        )
        self.assertEqual(
            policy.METHOD_RETURN_TYPE_OVERRIDES[("SoSFImage3", "startEditing")],
            "tuple[str, SbVec3s, int]",
        )
        self.assertEqual(
            policy.PYTHON_PARAMETER_TYPE_OVERRIDES[
                ("SoSFImage3", "setValue", "bytes")
            ],
            "str | bytes",
        )

    def test_enum_name_sequence_policy(self):
        self.assertEqual(
            policy.SEQUENCE_POINTER_PARAMETERS[
                ("SoMFEnum", "setEnums", "names")
            ],
            "SbName | Sequence[SbName | str]",
        )

    def test_rgba_multifield_policy(self):
        rgba = policy.MULTIFIELD_TYPE_POLICIES["SoMFColorRGBA"]
        self.assertEqual(rgba.element_type, "SbColor4f")
        self.assertEqual(rgba.set_values_types, ("SbColor4f", "Sequence[float]"))
        self.assertEqual(rgba.get_values_type, "SbColor4f")
        self.assertEqual(rgba.component_sequence_type, "Sequence[float]")
        self.assertEqual(rgba.component_width, 4)
        self.assertEqual(rgba.component_parameter_name, "rgba")

    def test_scalar_multifield_family_policy(self):
        expected = {
            "SoMFBool": ("bool", "bool", "bool"),
            "SoMFEnum": ("int", "int", "int"),
            "SoMFTime": ("SbTime", "SbTime", "SbTime"),
        }
        for class_name, policy_values in expected.items():
            multifield = policy.MULTIFIELD_TYPE_POLICIES[class_name]
            self.assertEqual(
                (
                    multifield.element_type,
                    multifield.set_values_types[0],
                    multifield.get_values_type,
                ),
                policy_values,
            )

    def test_string_multifield_single_value_policy(self):
        single_value_types = multifield_single_value_types()

        self.assertEqual(single_value_types["SoMFName"], "SbName | str")
        self.assertEqual(single_value_types["SoMFString"], "SbString | str")

    def test_nullable_node_policy(self):
        policy = FIELD_TYPE_POLICIES["SoSFNode"]

        self.assertEqual(policy.value_type, "SoNode | None")
        self.assertEqual(policy.setter_value_type, "SoNode | None")

    def test_string_and_name_field_policies(self):
        self.assertEqual(
            policy.FIELD_TYPE_POLICIES["SoSFString"].value_type,
            "SbString",
        )
        self.assertEqual(
            policy.FIELD_TYPE_POLICIES["SoSFString"].setter_value_type,
            "SbString | str",
        )
        self.assertEqual(
            policy.FIELD_TYPE_POLICIES["SoSFName"].value_type,
            "SbName",
        )
        self.assertEqual(
            policy.FIELD_TYPE_POLICIES["SoSFName"].setter_value_type,
            "SbName | str",
        )

    def test_field_methods_are_derived_from_policy(self):
        overrides = field_method_type_overrides()

        self.assertEqual(
            overrides[("SoSFPath", "getValue", "self")],
            ("self", "SoPath | None"),
        )
        self.assertEqual(
            overrides[("SoSFPath", "setValue", "self, newvalue: SoPath")],
            ("self, newvalue: SoPath | None", "None"),
        )

    def test_reflection_helpers_are_derived_from_policy(self):
        self.assertEqual(
            policy.PYTHON_HELPER_METHOD_TYPES[("SoFieldContainer", "__getattr__")],
            ("self, name: str", "SoField"),
        )
        self.assertEqual(
            policy.PYTHON_HELPER_METHOD_TYPES[("SoType", "fromName")],
            ("name: SbName | str", "SoType"),
        )
        self.assertEqual(
            policy.PYTHON_HELPER_METHOD_TYPES[("SoBaseKit", "__getattr__")],
            ("self, name: str", "SoNode | SoField"),
        )
        self.assertEqual(
            policy.PYTHON_HELPER_METHOD_TYPES[("SoEngine", "__getattr__")],
            ("self, name: str", "SoField | SoEngineOutput"),
        )

    def test_sensor_shadow_methods_have_python_signatures(self):
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SoSensor", "setFunction")],
            (
                "self, callbackfunction: SoSensorCallback[SoSensor]",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SoDataSensor", "setDeleteCallback")],
            (
                "self, function: SoSensorCallback[SoSensor], "
                "data: object | None = ...",
                "None",
            ),
        )

    def test_sensor_constructor_callback_types(self):
        self.assertEqual(
            policy.SENSOR_CALLBACK_CONSTRUCTOR_TYPES["SoTimerSensor"],
            (
                "SoSensorCallback[SoTimerSensor]",
                "object | None",
            ),
        )

    def test_soqt_event_callback_type(self):
        self.assertEqual(
            policy.CALLBACK_TYPE_SIGNATURES["SoQtRenderAreaEventCB"],
            "Callable[[object, QEvent], object]",
        )
        self.assertEqual(
            policy.PYTHON_PARAMETER_TYPE_OVERRIDES[
                ("SoQtRenderArea", "setEventCallback", "user")
            ],
            "object",
        )

    def test_single_enum_sequence_policy(self):
        self.assertEqual(
            policy.PYTHON_PARAMETER_TYPE_OVERRIDES[
                ("SoSFEnum", "setEnums", "vals")
            ],
            "Sequence[int]",
        )
        self.assertEqual(
            policy.PYTHON_PARAMETER_TYPE_OVERRIDES[
                ("SoSFEnum", "setEnums", "names")
            ],
            "SbName | Sequence[SbName | str]",
        )

    def test_database_shadow_methods_have_python_signatures(self):
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SoDB", "registerHeader")],
            (
                "headerstring: SbString, isbinary: bool, ivversion: float, "
                "precallback: Callable[[object, SoInput], None], "
                "postcallback: Callable[[object, SoInput], None], "
                "userdata: object | None = ...",
                "bool",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SoDB", "addProgressCallback")],
            (
                "func: Callable[[object, SbName, float, bool], bool], "
                "userdata: object | None",
                "None",
            ),
        )

    def test_callback_list_shadow_methods_have_python_signatures(self):
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SoCallbackList", "addCallback")],
            (
                "self, f: Callable[[object, object], None], "
                "userData: object | None = ...",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SoCallbackList", "invokeCallbacks")],
            ("self, callbackdata: object", "None"),
        )

    def test_context_handler_callback_methods_have_python_signatures(self):
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[
                ("SoContextHandler", "addContextDestructionCallback")
            ],
            (
                "func: Callable[[object, int], None], "
                "userdata: object | None = ...",
                "None",
            ),
        )

    def test_sorted_object_callback_has_python_signature(self):
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[
                ("SoGLRenderAction", "setSortedObjectOrderStrategy")
            ],
            (
                "self, strategy: int, "
                "cb: Callable[[object, SoGLRenderAction], float] | None = ..., "
                "closure: object | None = ...",
                "None",
            ),
        )

    def test_graphics_callback_setters_have_python_signatures(self):
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[
                ("SoGLImage", "setEndFrameCallback")
            ],
            (
                "self, cb: Callable[[object], None] | None, "
                "closure: object | None = ...",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[
                ("SoShaderProgram", "setEnableCallback")
            ],
            (
                "self, cb: Callable[[object, SoState, bool], None] | None, "
                "closure: object | None = ...",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[
                ("SoProto", "setFetchExternProtoCallback")
            ],
            (
                "cb: Callable[[object, SoInput, list[SbString], int], "
                "SoProto | None] | None, closure: object | None = ...",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SbImage", "addReadImageCB")],
            (
                "cb: Callable[[object, SbString, SbImage], bool], "
                "closure: object | None = ...",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SbImage", "removeReadImageCB")],
            (
                "cb: Callable[[object, SbString, SbImage], bool], "
                "closure: object | None = ...",
                "None",
            ),
        )
        self.assertEqual(
            policy.PYTHON_SHADOW_METHOD_TYPES[("SbImage", "scheduleReadFile")],
            (
                "self, cb: Callable[[object, SbString, SbImage], bool], "
                "closure: object | None, filename: SbString, "
                "searchdirectories: SbString | None = ..., "
                "numdirectories: int = ...",
                "bool",
            ),
        )

    def test_int32_references_use_the_existing_integer_pointer_helper(self):
        self.assertEqual(policy.SCALAR_REFERENCE_HELPER_TYPES["int32_t"], "intp")


class MultifieldTypePolicyTests(unittest.TestCase):
    def test_fixed_width_multifields_are_derived_from_vector_policy(self):
        derived = vector_multifield_type_policies()
        self.assertEqual(
            set(derived),
            {
                "SoMFVec2b",
                "SoMFVec2s",
                "SoMFVec2i32",
                "SoMFVec2f",
                "SoMFVec2d",
                "SoMFVec3b",
                "SoMFVec3s",
                "SoMFVec3i32",
                "SoMFVec3f",
                "SoMFVec3d",
                "SoMFVec4b",
                "SoMFVec4ub",
                "SoMFVec4s",
                "SoMFVec4us",
                "SoMFVec4i32",
                "SoMFVec4ui32",
                "SoMFVec4f",
                "SoMFVec4d",
            },
        )
        for vector_name, vector_policy in policy.VECTOR_TYPE_POLICIES.items():
            multifield = derived["SoMF%s" % vector_name[2:]]
            with self.subTest(vector_name=vector_name):
                self.assertEqual(multifield.element_type, vector_name)
                self.assertEqual(multifield.component_width, vector_policy.width)

    def test_multifield_element_types_cover_sequence_fields(self):
        element_types = multifield_iter_element_types()

        self.assertEqual(element_types["SoMFFloat"], "float")
        self.assertEqual(element_types["SoMFVec3f"], "SbVec3f")
        self.assertEqual(element_types["SoMFNode"], "SoNode")
        self.assertEqual(
            element_types,
            {
                name: policy.element_type
                for name, policy in MULTIFIELD_TYPE_POLICIES.items()
            },
        )

    def test_multifield_setvalues_types_are_derived_from_policy(self):
        setvalues_types = multifield_setvalues_types()

        self.assertEqual(
            setvalues_types["SoMFColor"],
            ("SbColor", "SbVec3f", "Sequence[float]"),
        )
        self.assertNotIn("SoMFDouble", setvalues_types)

    def test_multifield_getvalues_types_are_derived_from_policy(self):
        getvalues_types = multifield_getvalues_types()

        self.assertEqual(getvalues_types["SoMFFloat"], "float")
        self.assertEqual(getvalues_types["SoMFVec3f"], "SbVec3f")
        self.assertEqual(getvalues_types["SoMFName"], "str")
        self.assertNotIn("SoMFDouble", getvalues_types)

    def test_vector_component_sequence_types_are_derived_from_policy(self):
        component_types = multifield_component_sequence_types()

        self.assertEqual(component_types["SoMFVec2s"], ("Sequence[int]", 2))
        self.assertEqual(component_types["SoMFVec3d"], ("Sequence[float]", 3))
        self.assertEqual(component_types["SoMFVec4ui32"], ("Sequence[int]", 4))


class VectorTypePolicyTests(unittest.TestCase):
    def test_vector_array_inputs_are_derived_from_one_policy(self):
        array_types = vector_sequence_array_parameters()

        self.assertEqual(
            array_types[("SbVec2b", "__init__", "v")],
            ("Sequence[int]", "2"),
        )
        self.assertEqual(
            array_types[("SbVec3d", "setValue", "v")],
            ("Sequence[float]", "3"),
        )
        self.assertEqual(
            array_types[("SbVec4ui32", "setValue", "v")],
            ("Sequence[int]", "4"),
        )

    def test_vector_outputs_and_iterators_are_derived_from_policy(self):
        self.assertEqual(vector_value_return_types()["SbVec4ub"], "Sequence[int]")
        self.assertEqual(vector_iter_element_types()["SbVec3f"], "float")
        self.assertEqual(
            vector_output_parameter_types()["SbVec3i32"],
            ("x: intp", "y: intp", "z: intp"),
        )
        self.assertEqual(
            vector_output_parameter_types()["SbVec4d"],
            ("x: doublep", "y: doublep", "z: doublep", "w: doublep"),
        )


class IncompletePolicyTests(unittest.TestCase):
    def classify(self, **kwargs):
        return classify_incomplete(
            has_raw_pointer_note=False,
            **kwargs,
        )

    def test_explicit_categories(self):
        self.assertEqual(
            self.classify(
                kind="return",
                class_name="SoType",
                method_name="createInstance",
                parameter_name="return",
            ),
            "dynamic/runtime API",
        )
        self.assertEqual(
            self.classify(
                kind="parameter",
                class_name="SoSelection",
                method_name="addSelectionCallback",
                parameter_name="callback",
            ),
            "callbacks",
        )
        self.assertEqual(
            self.classify(
                kind="parameter",
                class_name="SoOutput",
                method_name="setBuffer",
                parameter_name="buffer",
            ),
            "raw C pointers",
        )

    def test_output_parameter_requires_an_output_method(self):
        self.assertEqual(
            self.classify(
                kind="parameter",
                class_name="SbVec3f",
                method_name="assign",
                parameter_name="values",
            ),
            "uncategorized",
        )
        self.assertEqual(
            self.classify(
                kind="parameter",
                class_name="SbVec3f",
                method_name="getValue",
                parameter_name="values",
            ),
            "unknown output parameters",
        )

    def test_raw_pointer_note_is_explicit(self):
        self.assertEqual(
            classify_incomplete(
                kind="return",
                class_name="SbVec3f",
                method_name="asPointer",
                parameter_name="return",
                has_raw_pointer_note=True,
            ),
            "raw C pointers",
        )

    def test_sb_image_snapshot_is_a_safe_python_value(self):
        self.assertEqual(
            policy.METHOD_RETURN_TYPE_OVERRIDES[("SbImage", "getValue")],
            "tuple[bytes | None, SbVec2s | SbVec3s, int]",
        )

    def test_offscreen_buffer_snapshot_is_a_safe_python_value(self):
        self.assertEqual(
            policy.METHOD_RETURN_TYPE_OVERRIDES[
                ("SoOffscreenRenderer", "getBuffer")
            ],
            "bytes",
        )
        self.assertEqual(
            policy.EXTEND_HELPER_METHOD_TYPES[
            ("SoOffscreenRenderer", "getBuffer", "self")
        ],
        ("self", "bytes"),
        )

    def test_color_packer_snapshot_is_a_safe_python_value(self):
        self.assertEqual(
            policy.METHOD_RETURN_TYPE_OVERRIDES[
                ("SoColorPacker", "getPackedColors")
            ],
            "bytes",
        )
        self.assertEqual(
            policy.EXTEND_HELPER_METHOD_TYPES[
                ("SoColorPacker", "getPackedColors", "self")
            ],
            ("self", "bytes"),
        )

    def test_byte_stream_snapshot_is_a_safe_python_value(self):
        self.assertEqual(
            policy.METHOD_RETURN_TYPE_OVERRIDES[("SoByteStream", "getData")],
            "bytes",
        )

    def test_known_reference_helpers_are_site_specific(self):
        self.assertEqual(
            policy.SCALAR_REFERENCE_HELPER_PARAMETERS[
                ("SoOutput", "getAvailableCompressionMethods", "num")
            ],
            "uintp",
        )
        self.assertEqual(
            policy.SCALAR_REFERENCE_HELPER_PARAMETERS[
                ("SoDepthBufferElement", "get", "function_out")
            ],
            "intp",
        )

    def test_deferred_pointer_outputs_are_classified_explicitly(self):
        for class_name, method_name, parameter_name in (
            ("SoAction", "getPathCode", "indices"),
            ("SoAction", "usePathCode", "indices"),
            ("SoFieldData", "getEnumData", "values"),
            ("SoSensorManager", "doSelect", "userTimeOut"),
            ("SoDB", "doSelect", "usertimeout"),
        ):
            with self.subTest(class_name=class_name, method_name=method_name):
                self.assertEqual(
                    self.classify(
                        kind="parameter",
                        class_name=class_name,
                        method_name=method_name,
                        parameter_name=parameter_name,
                    ),
                    "raw C pointers",
                )


class CallbackTypePolicyTests(unittest.TestCase):
    def test_native_callback_boundaries_cover_remaining_sites(self):
        report = collect_report(Path("pivy/coin.pyi"))
        remaining = {
            "callbacks",
            "function pointers",
        }
        sites = [
            site
            for site, category in report.incomplete_sites
            if category in remaining
        ]
        self.assertEqual(len(sites), 66)
        for site in sites:
            with self.subTest(
                kind=site.kind,
                class_name=site.class_name,
                method_name=site.method_name,
                name=site.name,
            ):
                self.assertIsNotNone(
                    policy.native_callback_boundary(
                        kind=site.kind,
                        class_name=site.class_name,
                        method_name=site.method_name,
                    )
                )

    def test_callback_policy_generates_generator_views(self):
        for (class_name, method_name), method_policy in (
            policy.CALLBACK_METHOD_POLICIES.items()
        ):
            with self.subTest(class_name=class_name, method_name=method_name):
                if method_policy.shadow_signature is not None:
                    self.assertEqual(
                        policy.PYTHON_SHADOW_METHOD_TYPES[
                            (class_name, method_name)
                        ],
                        method_policy.shadow_signature,
                    )
                for parameter_name, annotation in method_policy.parameter_types:
                    self.assertEqual(
                        policy.CALLBACK_PARAMETER_TYPE_OVERRIDES[
                            (class_name, method_name, parameter_name)
                        ],
                        annotation,
                    )

    def test_error_callbacks_use_python_callable_overrides(self):
        expected = "SoErrorCallback"

        for class_name in (
            "SoError",
            "SoDebugError",
            "SoMemoryError",
            "SoReadError",
        ):
            self.assertEqual(
                policy.CALLBACK_PARAMETER_TYPE_OVERRIDES[
                    (class_name, "setHandlerCallback", "pyfunc")
                ],
                expected,
            )
            self.assertEqual(
                policy.CALLBACK_PARAMETER_TYPE_OVERRIDES[
                    (class_name, "setHandlerCallback", "data")
                ],
                "object",
            )

    def test_sensor_callbacks_use_python_callable_overrides(self):
        self.assertEqual(
            policy.CALLBACK_PARAMETER_TYPE_OVERRIDES[
                ("SoSensor", "setFunction", "callbackfunction")
            ],
            "SoSensorCallback[SoSensor]",
        )
        self.assertEqual(
            policy.CALLBACK_PARAMETER_TYPE_OVERRIDES[
                ("SoDataSensor", "setDeleteCallback", "function")
            ],
            "SoSensorCallback[SoSensor]",
        )
        self.assertEqual(
            policy.CALLBACK_PARAMETER_TYPE_OVERRIDES[
                ("SoDataSensor", "setDeleteCallback", "data")
            ],
            "object | None",
        )

    def test_adapted_callback_protocols_have_required_bindings(self):
        definitions = {
            name: required_classes
            for name, required_classes, _ in policy.CALLBACK_PROTOCOL_DEFINITIONS
        }
        self.assertEqual(
            definitions["SoSensorCallback"],
            ("SoSensor",),
        )
        self.assertEqual(
            definitions["SoErrorCallback"],
            ("SoError",),
        )
        self.assertEqual(
            policy.CALLBACK_TYPE_SIGNATURES["ScXMLStateMachineDeleteCB"],
            "ScXMLStateMachineDeleteCallback",
        )
        self.assertEqual(
            policy.CALLBACK_TYPE_SIGNATURES["ScXMLStateChangeCB"],
            "ScXMLStateChangeCallback",
        )

    def test_adapted_callback_protocols_are_emitted_in_public_stubs(self):
        coin_stub = Path("pivy/coin.pyi").read_text()
        coin_protocols = {
            "SoSensorCallback",
            "SoErrorCallback",
            "ScXMLStateMachineDeleteCallback",
            "ScXMLStateChangeCallback",
        }
        for name in coin_protocols:
            with self.subTest(name=name):
                self.assertIn("class %s(Protocol" % name, coin_stub)

        soqt_stub = Path("pivy/gui/soqt.pyi").read_text()
        self.assertNotIn("class SoErrorCallback(Protocol):", soqt_stub)
        self.assertNotIn("class SoEvent:", soqt_stub)
        self.assertNotIn("class SbVec2s:", soqt_stub)
        self.assertIn("class SoQtComponentCallback(Protocol):", soqt_stub)
        self.assertIn("class SoQtViewerCallback(Protocol):", soqt_stub)
        self.assertIn("SoEvent", soqt_stub.splitlines()[7])
        self.assertIn("SbVec2s", soqt_stub.splitlines()[7])


class PolicyBoundaryTests(unittest.TestCase):
    def test_factory_policy_matches_swig_inventory(self):
        interface_classes = set()
        for path, macro in (
            ("Inventor/elements/SoElement.i", "PIVY_ELEMENT_FACTORY_OUT"),
            ("Inventor/engines/SoEngine.i", "PIVY_ENGINE_FACTORY_OUT"),
            ("Inventor/fields/SoField.i", "PIVY_FIELD_FACTORY_OUT"),
            ("Inventor/scxml/ScXMLObject.i", "PIVY_SCXML_FACTORY_OUT"),
        ):
            text = Path(path).read_text()
            interface_classes.update(
                class_name
                for class_name in re.findall(rf"{macro}\(([^)]+)\)", text)
                if class_name != "_class_"
            )

        self.assertEqual(interface_classes, FACTORY_CLASSES)
        self.assertEqual(set(SCXML_FACTORY_CLASS_NAMES), SCXML_FACTORY_CLASSES)
        self.assertTrue(
            set(SCXML_UNSUPPORTED_FACTORY_CLASS_NAMES).isdisjoint(interface_classes)
        )
        for class_name in interface_classes:
            self.assertEqual(
                factory_method_return_type(class_name, "createInstance"),
                class_name,
            )

    def test_generation_data_is_a_compatibility_reexport(self):
        self.assertIs(
            compatibility_policy.METHOD_RETURN_TYPE_OVERRIDES,
            policy.METHOD_RETURN_TYPE_OVERRIDES,
        )
        self.assertIs(
            compatibility_policy.CALLBACK_TYPE_SIGNATURES,
            policy.CALLBACK_TYPE_SIGNATURES,
        )
        self.assertIs(
            compatibility_policy.KNOWN_ITER_ELEMENT_TYPES,
            policy.KNOWN_ITER_ELEMENT_TYPES,
        )

    def test_checked_stub_meets_reviewed_quality_baseline(self):
        report = collect_report(Path("pivy/coin.pyi"))
        self.assertEqual(quality_regressions(report), ())

    def test_quality_report_has_a_stable_json_shape(self):
        stub_path = Path("pivy/coin.pyi")
        report = collect_report(stub_path)
        payload = report_to_dict(report, stub_path)

        json.dumps(payload)
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["annotation_sites"], report.annotation_sites)
        self.assertEqual(
            payload["incomplete_categories"]["uncategorized"]["count"],
            0,
        )
        self.assertEqual(
            payload["dynamic_runtime_subcategories"],
            dict(report.dynamic_runtime_subcategories),
        )
        self.assertEqual(
            payload["opaque_return_audit"], opaque_return_audit_summary(report)
        )

    def test_opaque_pointer_return_audit_is_complete(self):
        report = collect_report(Path("pivy/coin.pyi"))
        self.assertEqual(opaque_return_audit_issues(report), ())
        self.assertEqual(len(policy.OPAQUE_RETURN_AUDIT), 40)
        for key in policy.OPAQUE_RETURN_AUDIT:
            with self.subTest(key=key):
                self.assertIn(key, policy.TRIAGED_INCOMPLETE_SITES)

    def test_policy_managed_fields_are_covered(self):
        self.assertEqual(policy_coverage_errors(Path("pivy/coin.pyi")), ())

    def test_typing_matrix_covers_supported_python_targets(self):
        self.assertEqual(
            SUPPORTED_PYTHON_VERSIONS,
            ("3.10", "3.11", "3.12", "3.13", "3.14"),
        )

    def test_quality_baseline_covers_every_incomplete_category(self):
        budget_categories = {
            category for category, _ in TYPING_QUALITY_BASELINE.max_incomplete_by_category
        }
        self.assertEqual(budget_categories, set(INCOMPLETE_CATEGORIES))

    def test_incomplete_categories_have_reviewed_actions(self):
        self.assertEqual(set(INCOMPLETE_CATEGORY_ACTIONS), set(INCOMPLETE_CATEGORIES))
        self.assertIn("adapter", INCOMPLETE_CATEGORY_ACTIONS["raw C pointers"])
        self.assertIn("triage", INCOMPLETE_CATEGORY_ACTIONS["uncategorized"])

    def test_incomplete_categories_have_documented_dispositions(self):
        self.assertEqual(
            set(INCOMPLETE_CATEGORY_POLICIES),
            set(INCOMPLETE_CATEGORIES),
        )
        documentation = " ".join(Path("docs/typing-boundaries.md").read_text().split())
        for category, category_policy in INCOMPLETE_CATEGORY_POLICIES.items():
            self.assertIn("### %s" % category, documentation)
            self.assertIn(category_policy.disposition, documentation)
            self.assertIn(" ".join(category_policy.rationale.split()), documentation)

    def test_quality_regressions_enforces_category_budget(self):
        report = collect_report(Path("pivy/coin.pyi"))
        baseline = replace(
            TYPING_QUALITY_BASELINE,
            max_incomplete_by_category=(
                ("dynamic/runtime API", 291),
            ),
        )
        violations = quality_regressions(report, baseline)
        self.assertTrue(any("dynamic/runtime API" in violation for violation in violations))

    def test_dynamic_runtime_inventory_is_complete(self):
        report = collect_report(Path("pivy/coin.pyi"))
        self.assertEqual(
            set(report.dynamic_runtime_subcategories),
            set(policy.DYNAMIC_RUNTIME_SUBCATEGORIES),
        )
        self.assertEqual(
            sum(report.dynamic_runtime_subcategories.values()),
            report.incomplete_categories["dynamic/runtime API"],
        )
        self.assertEqual(
            dict(report.dynamic_runtime_subcategories),
            {
                "runtime factory returns": 4,
                "opaque pointer/object returns": 40,
                "opaque parameter boundaries": 247,
                "opaque field storage": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
