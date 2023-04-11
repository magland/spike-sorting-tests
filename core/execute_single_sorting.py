import os
import json
import shutil
import spikeinterface as si
import spikeinterface.sorters as ss
import spikeinterface.extractors as se
import spikeforest as sf
from core.config_classes import SpikeSortingTestsConfig, SortingConfig
from core.capture_console_output import capture_console_output, setup_logger


def execute_single_sorting(config: SpikeSortingTestsConfig, sorting_extractor: SortingConfig):
    sorter = next((s for s in config.sorters if s.id == sorting_extractor.sorter), None)
    if sorter is None:
        print(f'Sorter {sorting_extractor.sorter} not found in config. Skipping.')
        return
    recording = next((r for r in config.recordings if r.id == sorting_extractor.recording), None)
    if recording is None:
        print(f'Recording {sorting_extractor.recording} not found in config. Skipping.')
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
        sorting_extractor = ss.run_sorter(
            sorter.algorithm,
            recording=recording_extractor,
            output_folder=sorting_folder + '/output',
            **kwargs
        )

    print('Writing sorting')
    se.NpzSortingExtractor.write_sorting(sorting_extractor, f'{sorting_folder}/sorting.npz')

    print('Writing sorting info')
    sorting_info = {
        'num_units': len(sorting_extractor.unit_ids)
    }
    with open(f'{sorting_folder}/sorting_info.json', 'w') as f:
        json.dump(sorting_info, f, indent=4)

    print('Unit IDs:')
    print(sorting_extractor.unit_ids)

def write_binary_recording(recording: si.BaseRecording, folder: str):
    recording.save(folder=folder, format='binary')

def load_spikeforest_recording(study_name: str, recording_name: str):
    if study_name == 'paired_english':
        uri = 'sha1://dfb1fd134bfc209ece21fd5f8eefa992f49e8962?paired-english-spikeforest-recordings.json'
    else:
        raise Exception(f'Unknown study name: {study_name}')

    recordings = sf.load_spikeforest_recordings(uri)
    r = [rec for rec in recordings if rec.study_name == study_name and rec.recording_name == recording_name][0]
    return r