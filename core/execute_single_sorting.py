import os
import json
import shutil
import time
import spikeinterface as si
import spikeinterface.sorters as ss
import spikeinterface.extractors as se
from core.config_classes import SpikeSortingTestsConfig, SortingConfig
from core.capture_console_output import capture_console_output, setup_logger


def execute_single_sorting(config: SpikeSortingTestsConfig, sorting_config: SortingConfig):
    sorter = next((s for s in config.sorters if s.id == sorting_config.sorter), None)
    if sorter is None:
        print(f'Sorter {sorting_config.sorter} not found in config. Skipping.')
        return
    recording = next((r for r in config.recordings if r.id == sorting_config.recording), None)
    if recording is None:
        print(f'Recording {sorting_config.recording} not found in config. Skipping.')
        return

    recording_folder = f'output/recordings/{recording.id}'
    if not os.path.exists(recording_folder):
        os.mkdir(recording_folder)
    if not os.path.exists(f'{recording_folder}/sortings'):
        os.mkdir(f'{recording_folder}/sortings')
    sorting_folder = f'{recording_folder}/sortings/{sorter.id}'
    if not os.path.exists(sorting_folder):
        os.mkdir(sorting_folder)
    
    if not os.path.exists(f'output/recordings/{recording.id}/recording'):
        print('Recording directory does not exist. Skipping.')
        return

    if os.path.exists(f'{sorting_folder}/sorting.npz'):
        print('Sorting result already exists. Skipping.')
        return
    
    if os.path.exists(f'{sorting_folder}/output'):
        shutil.rmtree(f'{sorting_folder}/output')

    recording_extractor: si.BaseRecording = si.load_extractor(f'{recording_folder}/recording')

    print(f'Running spike sorting: {sorter.algorithm}')
    kwargs = {**sorter.sorting_parameters}
    if sorter.algorithm == 'spykingcircus2':
        kwargs['job_kwargs'] = {'n_jobs': 4}
    logger = setup_logger(f'{sorting_folder}/output.log')
    with capture_console_output(logger):
        sorting_config = ss.run_sorter(
            sorter.algorithm,
            recording=recording_extractor,
            output_folder=sorting_folder + '/output',
            **kwargs
        )

    print('Writing sorting')
    se.NpzSortingExtractor.write_sorting(sorting_config, f'{sorting_folder}/sorting.npz')

    print('Writing sorting info')
    sorting_info = {
        'timestamp': time.time(),
        'num_units': len(sorting_config.unit_ids)
    }
    with open(f'{sorting_folder}/sorting_info.json', 'w') as f:
        json.dump(sorting_info, f, indent=4)

    print('Unit IDs:')
    print(sorting_config.unit_ids)