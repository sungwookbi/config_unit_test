# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 21:33:37 2023

@author: sungw
"""

import pytest
import tempfile
from pathlib import Path

from src.config_reader import read_yaml_file, read_json_cfg, overwrite_json_cfg

## bad arguments, special arguments, normal arguments, exceptions, return values
## pytest utils/test_config_reader.py::test_read_json_cfg
## pytest -k "read" or pytest -k "config", -v for verbose, -x for stopping after first failure


@pytest.fixture(scope='module')
def yaml_file():
    # Create temporary YAML file for testing
    with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
        f.write(b"key1: value1\nkey2: value2\n_comment: comment1\n")
        f.flush()
        yield Path(f.name)
    Path.unlink(Path(f.name))

@pytest.fixture(scope='module')
def json_file():
    # Create temporary JSON file for testing
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        f.write(b'{"key1": "value1", "key2": "value2"}')
        f.flush()
        yield Path(f.name)
    Path.unlink(Path(f.name))

def test_read_yaml_file(yaml_file):
    # Test reading a YAML file
    expected_output = {'key1': 'value1', 'key2': 'value2'}
    actual_output = read_yaml_file(yaml_file)
    assert actual_output == expected_output, f"Failed to read YAML file: {yaml_file}"

def test_read_json_cfg(json_file):
    # Test reading a JSON file
    expected_output = {'key1': 'value1', 'key2': 'value2'}
    actual_output = read_json_cfg(json_file)
    assert actual_output == expected_output, f"Failed to read JSON file: {json_file}"

def test_overwrite_json_cfg(json_file):
    # Test overwriting a JSON file
    expected_output = {'key1': 'new_value1', 'key2': 'new_value2'}
    overwrite_json_cfg(expected_output, json_file)
    actual_output = read_json_cfg(json_file)
    assert actual_output == expected_output, f"Failed to overwrite JSON file: {json_file}"

def test_read_non_dict_yaml_file(yaml_file):
    # Test reading a non-dictionary YAML file
    with open(yaml_file, 'w') as f:
        f.write('not a dictionary')
    with pytest.raises(TypeError):
        read_yaml_file(yaml_file)

def test_read_non_dict_json_cfg(json_file):
    # Test reading a non-dictionary JSON file
    with open(json_file, 'w') as f:
        f.write('"not a dictionary"')
    with pytest.raises(TypeError):
        read_json_cfg(json_file)

def test_overwrite_with_non_dict_json_cfg(json_file):
    # Test overwriting a JSON file with a non-dictionary
    with pytest.raises(TypeError):
        overwrite_json_cfg('not a dictionary', json_file)


# for unit test not yet implemented, and it should fail
@pytest.mark.xfail(reason="bad argument not yet implemented")
def test_bad_argument():
    print('This should fail')

# skip tests conditionally
import sys
@pytest.mark.skipif(sys.version_info > (2, 7), reason="requires Python 2.7 or lower")
def test_skip_conditionally():
    print('This should skip')
