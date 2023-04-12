#!/bin/bash

set -ex

python copy_config_file.py
python prepare_recordings.py
python execute_sortings.py
python execute_comparisons.py
python generate_visualizations.py