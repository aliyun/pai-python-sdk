from __future__ import absolute_import

import unittest
from decimal import Decimal

from pai.pipeline.parameter import Interval, ParameterValidator, create_pipeline_parameter
from test import BaseTestCase


class TestParameter(BaseTestCase):

    def testParameter(self):
        cases = [
            {
                "name": "integer_type_param",
                "input": {
                    "name": "treeNum",
                    "kind": "input",
                    "typ": int,
                    "value": 100,
                    "feasible": {
                        "range": "[1, 1000]"
                    },
                },
                "expected": {
                    "name": "treeNum",
                    "type": "Int",
                    "value": 100,
                    "feasible": {
                        "range": "[1, 1000]"
                    }
                },
            },
            {
                "name": "str_type_param",
                "input": {
                    "name": "outputTableName",
                    "kind": "input",
                    "typ": str,
                    "required": True,
                    "value": "pai_temp_18090911",
                },
                "expected": {
                    "name": "outputTableName",
                    "type": "String",
                    "value": "pai_temp_18090911",
                    "required": True,
                },
            },
        ]

        for case in cases:
            param = create_pipeline_parameter(**case["input"])
            self.assertDictEqual(param.to_dict(), case["expected"])
            self.assertEqual(param.kind, case["input"]["kind"])

    def testParameterRangeValidator(self):
        cases = [
            {
                "name": "integer_range",
                "input": {
                    "feasible": {
                        "range": "[-100, 2929)",
                    },
                    "candidates": [-200, -100, 200, 2929, 3000],
                },
                "expected": [False, True, True, False, False],
            },
            {
                "name": "inf_range",
                "input": {
                    "feasible": {
                        "range": "(-INF, INF)",
                    },
                    "candidates": [-200, -100, 200, 2929, 3000],
                },
                "expected": [True, True, True, True, True],
            },
            {
                "name": "neg_inf_range",
                "input": {
                    "feasible": {
                        "range": "(-INF, 1000]",
                    },
                    "candidates": [Decimal("-INF"), -200, -100, 200, 1000, 3000, Decimal("INF")],
                },
                "expected": [False, True, True, True, True, False, False],
            },
            {
                "name": "pos_inf_range",
                "input": {
                    "feasible": {
                        "range": "(-INF, 1000]",
                    },
                    "candidates": [-200, -100, 200, 1000, 3000],
                },
                "expected": [True, True, True, True, False],
            }
        ]

        for case in cases:
            validator = ParameterValidator.load(case["input"]["feasible"])
            results = [validator.validate(candidate) for candidate in case["input"]["candidates"]]
            self.assertListEqual(results, case["expected"],
                                 "Unexpected validate result, case:%s, expected:%s, result:%s" % (
                                 case["name"], case["expected"], results))

    @staticmethod
    def interval_helper(interval):
        return [interval.min_, interval.min_inclusive, interval.max_, interval.max_inclusive]

    def testIntervalLoad(self):
        success_cases = [
            {
                "name": "integer_interval_1",
                "input": "(-100, 2929]",
                "expected": [-100, False, 2929, True]
            },
            {
                "name": "integer_interval_1",
                "input": "(100, 2929]",
                "expected": [100, False, 2929, True]
            },
            {
                "name": "integer_interval_1",
                "input": "(0, 100]",
                "expected": [0, False, 100, True]
            },
            {
                "name": "float_interval",
                "input": "[-3.14, 3.1425)",
                "expected": [Decimal("-3.14"), True, Decimal("3.1425"), False],
            },
            {
                "name": "infinity_case1",
                "input": "[-INF, INF]",
                "expected": [Decimal("-inf"), True, Decimal("inf"), True],
            },
            {
                "name": "infinity_float_case1",
                "input": "[-INF, 11.23]",
                "expected": [Decimal("-inf"), True, Decimal("11.23"), True]
            }
        ]

        for case in success_cases:
            result = self.interval_helper(Interval.load(case["input"]))
            self.assertListEqual(
                case["expected"],
                result,
                "Unexpected interval result. case:%s, expected:%s, result:%s" % (
                    case["name"], case["expected"], result)
            )

        error_cases = [
            {
                "name": "lower_greater_1",
                "input": "(300, 200]",
            },
            {
                "name": "lower_greater_2",
                "input": "[INF, -INF]",
            },
            {
                "name": "invalid_range",
                "input": "(1, 1)",
            },
            {
                "name": "lower_greater_3",
                "input": "[INF, 10.11]",
            },
            {
                "name": "invalid_pattern_1",
                "input": "[-3.14, 3.1425))",
            },
            {
                "name": "invalid_pattern_2",
                "input": "[-INF11, 11.23INF]",
            },
            {
                "name": "invalid_pattern_3",
                "input": "[-INF11, 11.23INF]",

            },
        ]

        for case in error_cases:
            with self.assertRaises(ValueError):
                Interval.load(case["input"])


if __name__ == '__main__':
    unittest.main()
