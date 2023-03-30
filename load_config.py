import yaml
from jsonschema import validate, ValidationError
import json
from config_classes import dict_to_spike_sorting_config


def load_config():
    config_file = 'spike_sorting_config.yaml'
    schema_file = 'spike_sorting_config_schema.json'

    config_data = load_yaml_file(config_file)
    schema_data = load_json_file(schema_file)

    if validate_config(config_data, schema_data):
        print("The configuration is valid.")
        config = dict_to_spike_sorting_config(config_data)
        return config
    else:
        raise Exception("The configuration is not valid. Please fix the errors and try again.")

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_config(config_data, schema_data):
    try:
        validate(instance=config_data, schema=schema_data)
        return True
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        return False