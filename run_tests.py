import yaml
from jsonschema import validate, ValidationError
import json
from config_classes import dict_to_spike_sorting_config, SpikeSortingTestsConfig
from run_sorting import run_sorting

def main():
    config_file = 'spike_sorting_config.yaml'
    schema_file = 'spike_sorting_config_schema.json'

    config_data = load_yaml_file(config_file)
    schema_data = load_json_file(schema_file)

    if validate_config(config_data, schema_data):
        print("The configuration is valid.")
        config = dict_to_spike_sorting_config(config_data)
        run_spike_sorting(config)
    else:
        print("The configuration is not valid. Please fix the errors and try again.")

def run_spike_sorting(config: SpikeSortingTestsConfig):
    for sorting in config.sortings:
        print(f"Running spike sorting for {sorting.recording} using {sorting.sorter}")
        run_sorting(config, sorting)

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

if __name__ == '__main__':
    main()
