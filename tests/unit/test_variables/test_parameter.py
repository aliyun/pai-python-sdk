#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import

import unittest
from decimal import Decimal

from pai.pipeline.types import ParameterType, PipelineParameter
from pai.pipeline.types.parameter import Interval, ParameterValidator
from tests.unit import BaseUnitTestCase


class TestParameter(BaseUnitTestCase):
    def testParameter(self):
        cases = [
            {
                "name": "integer_type_param",
                "input": {
                    "name": "treeNum",
                    "io_type": "inputs",
                    "typ": int,
                    "default": 100,
                    "feasible": {"range": "[1, 1000]"},
                },
                "expected": {
                    "name": "treeNum",
                    "type": "Int",
                    "value": 100,
                    "feasible": {"range": "[1, 1000]"},
                },
            },
            {
                "name": "str_type_param",
                "input": {
                    "name": "outputTableName",
                    "io_type": "inputs",
                    "typ": str,
                    "default": "pai_temp_18090911",
                },
                "expected": {
                    "name": "outputTableName",
                    "type": "String",
                    "value": "pai_temp_18090911",
                },
            },
        ]

        for case in cases:
            param = PipelineParameter(**case["input"])
            self.assertDictEqual(param.to_dict(), case["expected"])
            self.assertEqual(param.io_type, case["input"]["io_type"])

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
                    "candidates": [
                        Decimal("-INF"),
                        -200,
                        -100,
                        200,
                        1000,
                        3000,
                        Decimal("INF"),
                    ],
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
            },
        ]

        for case in cases:
            validator = ParameterValidator.load(case["input"]["feasible"])
            results = [
                validator.validate(candidate)
                for candidate in case["input"]["candidates"]
            ]
            self.assertListEqual(
                results,
                case["expected"],
                "Unexpected validate result, case:%s, expected:%s, result:%s"
                % (case["name"], case["expected"], results),
            )

    @staticmethod
    def interval_helper(interval):
        return [
            interval.min_,
            interval.min_inclusive,
            interval.max_,
            interval.max_inclusive,
        ]

    def testIntervalLoad(self):
        success_cases = [
            {
                "name": "integer_interval_1",
                "input": "(-100, 2929]",
                "expected": [-100, False, 2929, True],
            },
            {
                "name": "integer_interval_1",
                "input": "(100, 2929]",
                "expected": [100, False, 2929, True],
            },
            {
                "name": "integer_interval_1",
                "input": "(0, 100]",
                "expected": [0, False, 100, True],
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
                "expected": [Decimal("-inf"), True, Decimal("11.23"), True],
            },
        ]

        for case in success_cases:
            result = self.interval_helper(Interval.load(case["input"]))
            self.assertListEqual(
                case["expected"],
                result,
                "Unexpected interval result. case:%s, expected:%s, result:%s"
                % (case["name"], case["expected"], result),
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

    def test_parameter_type_transform(self):
        cases = [
            {
                "name": "case_int_1",
                "input": "int",
                "expected": ParameterType.Integer,
            },
            {
                "name": "case_int_2",
                "input": "integer",
                "expected": ParameterType.Integer,
            },
            {
                "name": "case_int_3",
                "input": int,
                "expected": ParameterType.Integer,
            },
            {
                "name": "case_int_4",
                "input": ParameterType.Integer,
                "expected": ParameterType.Integer,
            },
            {
                "name": "case_str_1",
                "input": str,
                "expected": ParameterType.String,
            },
            {
                "name": "case_str_1",
                "input": "string",
                "expected": ParameterType.String,
            },
            {
                "name": "case_float_1",
                "input": "float",
                "expected": ParameterType.Double,
            },
            {
                "name": "case_float_2",
                "input": float,
                "expected": ParameterType.Double,
            },
            {
                "name": "case_float_3",
                "input": "double",
                "expected": ParameterType.Double,
            },
            {
                "name": "case_bool_1",
                "input": bool,
                "expected": ParameterType.Bool,
            },
            {
                "name": "case_bool_2",
                "input": "boolean",
                "expected": ParameterType.Bool,
            },
            {
                "name": "case_bool_3",
                "input": "Bool",
                "expected": ParameterType.Bool,
            },
            {
                "name": "case_bool_4",
                "input": ParameterType.Bool,
                "expected": ParameterType.Bool,
            },
            {
                "name": "case_map_1",
                "input": dict,
                "expected": ParameterType.Map,
            },
            {
                "name": "case_map_2",
                "input": "Map",
                "expected": ParameterType.Map,
            },
        ]

        for case in cases:
            result = ParameterType.normalize_typ(case["input"])
            self.assertEqual(result, case["expected"])


if __name__ == "__main__":
    unittest.main()
