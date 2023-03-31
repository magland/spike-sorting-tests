import os
import spikeinterface as si
import spikeinterface.sorters as ss
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spre
import spikeforest as sf
from core.config_classes import SpikeSortingTestsConfig, RecordingConfig


def prepare_single_recording(config: SpikeSortingTestsConfig, recording: RecordingConfig):
    if not os.path.exists('output/recordings'):
        os.makedirs('output/recordings')
    recording_folder = f'output/recordings/{recording.id}'
    if not os.path.exists(recording_folder):
        os.mkdir(f'output/recordings/{recording.id}')

    print('Loading spikeforest recording')
    sf_rec = load_spikeforest_recording(recording.parameters['study_name'], recording.parameters['recording_name'])

    if not os.path.exists(f'{recording_folder}/recording'):
        recording_extractor = sf_rec.get_recording_extractor()
        print('Creating recording directory')
        write_binary_recording(recording_extractor, f'{recording_folder}/recording')
    else:
        print('recording directory already exists')
    
    if not os.path.exists(f'{recording_folder}/recording_preprocessed'):
        recording_extractor: si.BaseRecording = si.load_extractor(f'{recording_folder}/recording')
        recording_filtered = spre.bandpass_filter(recording_extractor, freq_min=300, freq_max=6000)
        recording_preprocessed = spre.whiten(recording_filtered)
        print('Creating recording_preprocessed directory')
        write_binary_recording(recording_preprocessed, f'{recording_folder}/recording_preprocessed')
    else:
        print('recording_preprocessed directory already exists')
    sorting_true_extractor: si.BaseSorting = sf_rec.get_sorting_true_extractor()
    if sorting_true_extractor is not None:
        sorting_true_folder = f'{recording_folder}/sorting_true'
        if not os.path.exists(sorting_true_folder):
            print('Creating sorting_true directory')
            os.mkdir(sorting_true_folder)
            si.NpzSortingExtractor.write_sorting(sorting_true_extractor, sorting_true_folder + '/sorting.npz')
        else:
            print('sorting_true directory already exists')

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