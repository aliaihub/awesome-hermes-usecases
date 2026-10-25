import importlib.util
from pathlib import Path
import unittest

EXAMPLES = Path(__file__).resolve().parents[1] / "recipes/examples"


def load(name):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


watchdog = load("disk_watchdog")
receipt = load("validate_receipt")


class RecipeExampleTests(unittest.TestCase):
    def test_watchdog_silence_and_threshold_boundary(self):
        self.assertEqual(watchdog.alert_for(89, 100, 90), "")
        self.assertIn("90.0%", watchdog.alert_for(90, 100, 90))
        self.assertIn("99.0%", watchdog.alert_for(99, 100, 90))

    def test_receipt_accepts_expected_contract(self):
        import json
        receipt.validate(json.loads((EXAMPLES / "receipt.expected.json").read_text()))

    def test_receipt_rejects_unsafe_or_wrong_types(self):
        good = {"vendor": "Example", "total": 8.4, "currency": "CAD", "tags": ["office"]}
        for changes in ({"total": True}, {"total": -1}, {"total": float("nan")},
                        {"total": float("inf")}, {"total": "8.40"}, {"currency": "cad"},
                        {"tags": "office"}, {"vendor": ""}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                receipt.validate(dict(good, **changes))
        with self.assertRaises(ValueError):
            receipt.validate(dict(good, invented_field="extra"))


if __name__ == "__main__":
    unittest.main()
