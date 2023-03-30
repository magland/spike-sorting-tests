import os
import spikeinterface as si
import spikeinterface.sorters as ss
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spre
import spikeforest as sf
from config_classes import SpikeSortingTestsConfig, SortingConfig
from capture_console_output import capture_console_output, setup_logger


def perform_single_sorting(config: SpikeSortingTestsConfig, sorting: SortingConfig):
    recording = [rec for rec in config.recordings if rec.id == sorting.recording][0]
    sorter = [s for s in config.sorters if s.id == sorting.sorter][0]

    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('output/recordings'):
        os.mkdir('output/recordings')
    recording_folder = f'output/recordings/{recording.id}'
    if not os.path.exists(recording_folder):
        os.mkdir(f'output/recordings/{recording.id}')
    if not os.path.exists(f'{recording_folder}/recording'):
        sf_rec = load_spikeforest_recording(recording.parameters['study_name'], recording.parameters['recording_name'])
        recording_extractor = sf_rec.get_recording_extractor()
        write_binary_recording(recording_extractor, f'{recording_folder}/recording')
    if not os.path.exists(f'{recording_folder}/recording_preprocessed'):
        recording_extractor: si.BaseRecording = si.load_extractor(f'{recording_folder}/recording')
        recording_filtered = spre.bandpass_filter(recording_extractor, freq_min=300, freq_max=6000)
        recording_preprocessed = spre.whiten(recording_filtered)
        write_binary_recording(recording_preprocessed, f'{recording_folder}/recording_preprocessed')
    if not os.path.exists(f'{recording_folder}/sortings'):
        os.mkdir(f'{recording_folder}/sortings')
    output_folder = f'{recording_folder}/sortings/{sorter.id}'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    if os.path.exists(f'{output_folder}/output'):
        print('Sorting output already exists. Skipping.')
    else:
        recording_extractor: si.BaseRecording = si.load_extractor(f'{recording_folder}/recording')
        logger = setup_logger(f'{output_folder}/output.log')
        with capture_console_output(logger):
            ss.run_sorter(sorter.algorithm, recording=recording_extractor, output_folder=output_folder + '/output', **sorter.sorting_parameters)

        sorting_extractor = se.NpzSortingExtractor(output_folder + '/output/sorter_output/firings.npz')
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