import re
import unittest
from pathlib import Path

import tools.pivy_stub_generation_data as compatibility_policy
import tools.pivy_stub_typing_policy as policy
from tools.report_pivy_typing import collect_report, quality_regressions
from tools.pivy_stub_typing_policy import (
    FACTORY_CLASSES,
    FIELD_TYPE_POLICIES,
    factory_method_return_type,
    MULTIFIELD_TYPE_POLICIES,
    classify_incomplete,
    field_method_type_overrides,
    multifield_component_sequence_types,
    multifield_getvalues_types,
    multifield_iter_element_types,
    multifield_setvalues_types,
    vector_iter_element_types,
    vector_output_parameter_types,
    vector_sequence_array_parameters,
    vector_value_return_types,
)


class FieldTypePolicyTests(unittest.TestCase):
    def test_nullable_node_policy(self):
        policy = FIELD_TYPE_POLICIES["SoSFNode"]

        self.assertEqual(policy.value_type, "SoNode | None")
        self.assertEqual(policy.setter_value_type, "SoNode | None")

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

    def test_int32_references_use_the_existing_integer_pointer_helper(self):
        self.assertEqual(policy.SCALAR_REFERENCE_HELPER_TYPES["int32_t"], "intp")


class MultifieldTypePolicyTests(unittest.TestCase):
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


class PolicyBoundaryTests(unittest.TestCase):
    def test_factory_policy_matches_swig_inventory(self):
        interface_classes = set()
        for path, macro in (
            ("Inventor/elements/SoElement.i", "PIVY_ELEMENT_FACTORY_OUT"),
            ("Inventor/fields/SoField.i", "PIVY_FIELD_FACTORY_OUT"),
        ):
            text = Path(path).read_text()
            interface_classes.update(
                class_name
                for class_name in re.findall(rf"{macro}\(([^)]+)\)", text)
                if class_name != "_class_"
            )

        self.assertEqual(interface_classes, FACTORY_CLASSES)
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


if __name__ == "__main__":
    unittest.main()
