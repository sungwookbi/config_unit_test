# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:26:41 2023

@author: sungw
"""

import yaml
import json
import pathlib


def read_yaml_file(yaml_file_path):
    '''
    turn yaml into simple dictionary (inner dictionary)
    '''
    if not isinstance(yaml_file_path, pathlib.PurePath):
        raise TypeError("Expected 'yaml_file_path' to be a pathlib path")
    # Load YAML configuration file
    with open(yaml_file_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Create variables from inner dictionary keys and values, excluding _comment
    if isinstance(config, dict):
        # if config is a dictionary
        cfg = {k: v for k, v in config.items() if k != '_comment'}
    elif isinstance(config, list):
        # if config is a list
        cfg = {k: v for d in config[0].values() for k, v in d.items() 
               if d.get('_comment') is None or '_comment' not in k}
    elif not isinstance(config, dict):
        raise TypeError("Expected 'config' to be a dictionary")

    return cfg


def read_json_cfg(file_path):
    if not isinstance(file_path, pathlib.PurePath):
        raise TypeError("Expected 'file_path' to be a pathlib path")
    with open(file_path, 'r') as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise TypeError("JSON file does not contain a dictionary")
        return data


def overwrite_json_cfg(my_dict, file_path):
    if not isinstance(my_dict, dict):
        raise TypeError("Expected 'my_dict' to be a dictionary")
    if not isinstance(file_path, pathlib.PurePath):
        raise TypeError("Expected 'file_path' to be a pathlib path")
    with open(file_path, 'w') as f:
        json.dump(my_dict, f)

