"""Tests for the lossless Phase 1 semantic stub model."""

from pathlib import Path
import unittest
from collections import Counter

from tools.pivy_typing.boundaries import resolve_incomplete_boundaries
from tools.pivy_typing.model import parse_stub, render_stub


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class SemanticStubModelTests(unittest.TestCase):
    def test_tracked_coin_stub_round_trips_byte_for_byte(self):
        source = (PROJECT_ROOT / "pivy" / "coin.pyi").read_text(encoding="utf-8")
        model = parse_stub(source, name="pivy.coin")

        self.assertEqual(render_stub(model), source)
        self.assertGreater(len(model.classes), 800)
        self.assertIn("SoMFDouble", {item.name for item in model.classes})

    def test_model_records_classes_methods_attributes_and_overloads(self):
        source = (PROJECT_ROOT / "pivy" / "coin.pyi").read_text(encoding="utf-8")
        model = parse_stub(source, name="pivy.coin")
        classes = {item.name: item for item in model.classes}

        multifield = classes["SoMFDouble"]
        methods = {item.name: item for item in multifield.methods}
        self.assertEqual(methods["getValues"].overloads[0].return_type.text, "list[float]")
        self.assertEqual(methods["__getitem__"].overloads[0].parameters[1].kind, "positional_or_keyword")
        self.assertIn("overload", methods["setValues"].decorators)

        cube = classes["SoCube"]
        attributes = {item.name: item for item in cube.attributes}
        self.assertEqual(attributes["width"].type.text, "SoSFFloat")

    def test_parser_preserves_signature_details(self):
        source = '''
from typing import overload

class Example:
    value: int

    @overload
    def read(self, index: int, /, *, strict: bool = False) -> str: ...

    @overload
    def read(self, name: str, /, *, strict: bool = False) -> str: ...

    def invoke(self, *args: object, **kwargs: object) -> None: ...
'''
        example = parse_stub(source, name="example").classes[0]
        methods = {item.name: item for item in example.methods}

        read = methods["read"]
        self.assertEqual(len(read.overloads), 2)
        self.assertEqual(read.overloads[0].parameters[1].kind, "positional_only")
        self.assertEqual(read.overloads[0].parameters[2].default, "False")
        self.assertEqual(read.overloads[0].parameters[2].kind, "keyword_only")
        self.assertEqual(read.overloads[0].return_type.text, "str")

        invoke = methods["invoke"].overloads[0].parameters
        self.assertEqual(invoke[1].kind, "var_positional")
        self.assertEqual(invoke[2].kind, "var_keyword")

    def test_incomplete_boundaries_resolve_to_the_quality_baseline(self):
        source = (PROJECT_ROOT / "pivy" / "coin.pyi").read_text(encoding="utf-8")
        boundaries = resolve_incomplete_boundaries(
            parse_stub(source, name="pivy.coin")
        )
        categories = Counter(boundary.category for boundary in boundaries)

        self.assertEqual(len(boundaries), 436)
        self.assertEqual(categories["uncategorized"], 0)
        self.assertEqual(categories["raw C pointers"], 103)
        self.assertEqual(categories["dynamic/runtime API"], 267)


if __name__ == "__main__":
    unittest.main()
