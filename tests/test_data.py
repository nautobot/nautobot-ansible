# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

# Load test data from a json file, for a pytest parametrize
def load_test_data(path, test_path):
    with open(f"{path}/test_data/{test_path}/data.json", "r") as f:
        data = json.loads(f.read())
    tests = []
    for test in data:
        tuple_data = tuple(test.values())
        tests.append(tuple_data)
    return tests
