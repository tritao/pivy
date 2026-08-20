import unittest

from tools.pivy_stub_typing_policy import (
    FIELD_TYPE_POLICIES,
    MULTIFIELD_TYPE_POLICIES,
    classify_incomplete,
    field_method_type_overrides,
    multifield_iter_element_types,
    multifield_setvalues_types,
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


if __name__ == "__main__":
    unittest.main()
