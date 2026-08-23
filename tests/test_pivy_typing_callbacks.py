"""Tests for first-class callback lifecycle contracts."""

import unittest

from tools.pivy_typing.callbacks import (
    CALLBACK_CONTRACTS,
    CallbackRemoval,
    CallbackRetention,
    callback_method_checks,
)


class CallbackContractTests(unittest.TestCase):
    def test_every_adapted_callback_has_a_reviewed_lifecycle(self):
        self.assertGreaterEqual(len(CALLBACK_CONTRACTS), 80)
        for contract in CALLBACK_CONTRACTS.values():
            self.assertTrue(contract.python_safe)
            self.assertTrue(contract.source)
            self.assertTrue(contract.reason)
            self.assertIsInstance(contract.retention, CallbackRetention)
            self.assertIsInstance(contract.removal, CallbackRemoval)

    def test_representative_lifecycles_are_explicit(self):
        sensor = CALLBACK_CONTRACTS[("SoSensor", "setFunction")]
        self.assertEqual(sensor.retention, CallbackRetention.SENSOR_LIFETIME)
        self.assertEqual(sensor.removal, CallbackRemoval.REPLACE_OR_CLEAR)
        self.assertFalse(sensor.nullable)

        scheduled = CALLBACK_CONTRACTS[
            ("SoGLCacheContextElement", "scheduleDeleteCallback")
        ]
        self.assertEqual(scheduled.retention, CallbackRetention.UNTIL_DISPATCH)
        self.assertEqual(scheduled.removal, CallbackRemoval.DISPATCH)

        selection = CALLBACK_CONTRACTS[("SoSelection", "addSelectionCallback")]
        self.assertEqual(selection.removal, CallbackRemoval.IDENTITY)
        self.assertTrue(selection.has_userdata)

    def test_contract_checks_preserve_existing_validator_shapes(self):
        coin_checks = callback_method_checks(module="coin.pyi")
        soqt_checks = callback_method_checks(module="gui/soqt.pyi")

        self.assertIn(
            (
                "SoCallbackAction",
                "addPreCallback",
                {
                    "type": "SoType",
                    "pyfunc": "SoCallbackActionNodeCallback",
                    "userdata": "object",
                },
                "None",
            ),
            coin_checks,
        )
        self.assertIn(
            (
                "SoQtViewer",
                "setAutoClippingStrategy",
                {
                    "strategy": "SoQtNearPlaneMode",
                    "value": "float",
                    "cb": "SoQtAutoClippingCallback | None",
                    "cbuserdata": "object | None",
                },
                "None",
            ),
            soqt_checks,
        )

if __name__ == "__main__":
    unittest.main()
