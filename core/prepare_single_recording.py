from typing import Optional
import numpy as np
import os
import json
import time
import spikeinterface as si
import spikeinterface.sorters as ss
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spre
import spikeforest as sf
from spikeforest.load_spikeforest_recordings.SFRecording import SFRecording
from core.config_classes import SpikeSortingTestsConfig, RecordingConfig


def prepare_single_recording(config: SpikeSortingTestsConfig, recording: RecordingConfig):
    # Make sure the output directory exists
    if not os.path.exists('output/recordings'):
        os.makedirs('output/recordings')
    recording_folder = f'output/recordings/{recording.id}'
    if not os.path.exists(recording_folder):
        os.mkdir(f'output/recordings/{recording.id}')

    if recording.type == 'spikeforest':
        print('Loading spikeforest recording')
        sf_rec = load_spikeforest_recording(recording.parameters['study_name'], recording.parameters['recording_name'])
        recording_name = sf_rec.recording_name
        study_name = sf_rec.study_name
        study_set_name = sf_rec.study_set_name
        num_true_units = sf_rec.num_true_units

        if not os.path.exists(f'{recording_folder}/recording'):
            recording_extractor = sf_rec.get_recording_extractor()
            print('Creating recording directory')
            write_binary_recording(recording_extractor, f'{recording_folder}/recording')
        else:
            print('recording directory already exists')
    elif recording.type == 'spyglass':
        print('Loading spyglass recording')
        sf_rec = None
        recording_name = recording.parameters['nwb_file']
        study_name = 'spyglass'
        study_set_name = 'spyglass'
        num_true_units = 0
        if not os.path.exists(f'{recording_folder}/recording'):
            recording_extractor = load_spyglass_recording_extractor(
                nwb_file=recording.parameters['nwb_file'],
                group_id=recording.parameters['group_id'],
                start_frame=recording.parameters['start_frame'],
                end_frame=recording.parameters['end_frame'],
                num_channels=recording.parameters.get('num_channels', None)
            )
            print(f'Loaded recording with {recording_extractor.get_num_channels()} channels and {recording_extractor.get_num_frames()} frames and {recording_extractor.get_sampling_frequency()} Hz sampling rate')
            print('Creating recording directory')
            write_binary_recording(recording_extractor, f'{recording_folder}/recording')
        else:
            print('recording directory already exists')
    else:
        raise Exception(f"Recording type {recording.type} not supported")
    
    recording_extractor: si.BaseRecording = si.load_extractor(f'{recording_folder}/recording')
    if not os.path.exists(f'{recording_folder}/recording_preprocessed'):
        recording_filtered = spre.bandpass_filter(recording_extractor, freq_min=300, freq_max=6000)
        recording_preprocessed = spre.whiten(recording_filtered, dtype='float32')
        print('Creating recording_preprocessed directory')
        write_binary_recording(recording_preprocessed, f'{recording_folder}/recording_preprocessed')
    else:
        print('recording_preprocessed directory already exists')

    if sf_rec is not None:
        sorting_true_extractor: si.BaseSorting = sf_rec.get_sorting_true_extractor()
        if sorting_true_extractor is not None:
            sorting_true_folder = f'{recording_folder}/sorting_true'
            if not os.path.exists(sorting_true_folder):
                print('Creating sorting_true directory')
                os.mkdir(sorting_true_folder)
                si.NpzSortingExtractor.write_sorting(sorting_true_extractor, sorting_true_folder + '/sorting.npz')
            else:
                print('sorting_true directory already exists')
    
    recording_info = {
        'recording_name': recording_name,
        'study_name': study_name,
        'study_set_name': study_set_name,
        'sampling_frequency': recording_extractor.sampling_frequency,
        'num_channels': recording_extractor.get_num_channels(),
        'duration_sec': recording_extractor.get_total_duration(),
        'num_true_units': num_true_units,
    }
    with open(f'{recording_folder}/recording_info.json', 'w') as f:
        json.dump(recording_info, f, indent=4)
    with open(f'{recording_folder}/timestamp', 'w') as f:
        f.write(str(time.time()))

def write_binary_recording(recording: si.BaseRecording, folder: str):
    recording.save(folder=folder, format='binary')

def load_spikeforest_recording(study_name: str, recording_name: str):
    if study_name == 'paired_english':
        uri = 'sha1://dfb1fd134bfc209ece21fd5f8eefa992f49e8962?paired-english-spikeforest-recordings.json'
    elif study_name == 'hybrid_janelia':
        uri = 'sha1://43298d72b2d0860ae45fc9b0864137a976cb76e8?hybrid-janelia-spikeforest-recordings.json'
    elif study_name == 'synth_monotrode':
        uri = 'sha1://3b265eced5640c146d24a3d39719409cceccc45b?synth-monotrode-spikeforest-recordings.json'
    elif study_name == 'paired_boyden':
        uri = 'sha1://849e53560c9241c1206a82cfb8718880fc1c6038?paired-boyden-spikeforest-recordings.json'
    elif study_name == 'paired_kampff':
        uri = 'sha1://b8b571d001f9a531040e79165e8f492d758ec5e0?paired-kampff-spikeforest-recordings.json'
    else:
        raise Exception(f'Unknown study name: {study_name}')

    recordings = sf.load_spikeforest_recordings(uri)
    r = [rec for rec in recordings if rec.study_name == study_name and rec.recording_name == recording_name][0]
    return r

def load_spyglass_recording_extractor(nwb_file: str, group_id: int, start_frame: int, end_frame: int, num_channels: Optional[int] = None):
    nwb_fname = os.environ['SPYGLASS_BASE_DIR'] + f'/raw/{nwb_file}'
    recording: si.BaseRecording = se.read_nwb_recording(nwb_fname, load_time_vector=True)

    channel_indices = np.where(recording.get_channel_groups() == group_id)[0]
    channel_ids = recording.channel_ids[channel_indices]

    if num_channels is not None:
        channel_ids = channel_ids[:num_channels]

    print(f'Channel ids: {channel_ids}')

    recording1 = recording.channel_slice(channel_ids)

    recording2 = recording1.frame_slice(
        start_frame=start_frame, end_frame=end_frame
    )

    return recording2