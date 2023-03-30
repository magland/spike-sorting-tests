import os
import argparse
import yaml
import json
import numpy as np
import numpy.typing as npt
import spikeinterface as si
import spikeinterface.extractors as se
import sortingview.views as vv
import figurl as fg
from load_config import load_config
from config_classes import RecordingConfig, SortingConfig
from extract_snippets import extract_snippets


def parse_arguments():
    parser = argparse.ArgumentParser(description="Execute spike sorting tests.")
    parser.add_argument('--sorter', type=str, help='Filter sortings to only those that use the specified sorter ID')
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = load_config()
    
    filtered_sortings = config.sortings
    
    if args.sorter:
        filtered_sortings = [sorting for sorting in config.sortings if sorting.sorter == args.sorter]
    
    for recording in config.recordings:
        print(f'Generating visualization for {recording.id}')
        recording_visualization_folder = f'output/visualizations/recordings/{recording.id}'
        if not os.path.exists(recording_visualization_folder):
            os.makedirs(recording_visualization_folder)
        if not os.path.exists(f'{recording_visualization_folder}/view.yaml'):
            view = create_recording_view(recording)
            os.environ['KACHERY_STORE_FILE_DIR'] = f'{recording_visualization_folder}'
            os.environ['KACHERY_STORE_FILE_PREFIX'] = f'$dir'
            url_dict = view.url_dict(label=recording.id)
            view = {
                'type': 'figurl',
                'v': url_dict['v'],
                'd': url_dict['d']
            }
            with open(f'{recording_visualization_folder}/view.yaml', 'w') as f:
                yaml.dump(view, f)
        else:
            print(f'View already exists')

    for sorting in filtered_sortings:
        print(f"Generating visualization for {sorting.recording} and {sorting.sorter}")
        sorting_folder = f'output/recordings/{sorting.recording}/sortings/{sorting.sorter}'
        if not os.path.exists(sorting_folder):
            print(f'Sorting folder does not exist. Skipping')
            continue
        sorting_visualization_folder = f'output/visualizations/recordings/{sorting.recording}/sortings/{sorting.sorter}'
        if not os.path.exists(sorting_visualization_folder):
            os.makedirs(sorting_visualization_folder)
        if not os.path.exists(f'{sorting_visualization_folder}/view.yaml'):
            view = create_sorting_view(sorting)
            os.environ['KACHERY_STORE_FILE_DIR'] = f'{sorting_visualization_folder}'
            os.environ['KACHERY_STORE_FILE_PREFIX'] = f'$dir'
            url_dict = view.url_dict(label=recording.id)
            view = {
                'type': 'figurl',
                'v': url_dict['v'],
                'd': url_dict['d']
            }
            with open(f'{sorting_visualization_folder}/view.yaml', 'w') as f:
                yaml.dump(view, f)
        else:
            print(f'View already exists')

def create_recording_view(recording: RecordingConfig):
    view_traces = vv.EphysTraces(
        format='spikeinterface.binary',
        uri=f'rtcshare://recordings/{recording.id}/recording'
    )
    view_traces_preprocessed = vv.EphysTraces(
        format='spikeinterface.binary',
        uri=f'rtcshare://recordings/{recording.id}/recording_preprocessed'
    )
    view = vv.TabLayout(
        items=[
            vv.TabLayoutItem(label='Raw traces', view=view_traces),
            vv.TabLayoutItem(label='Preprocessed traces', view=view_traces_preprocessed)
        ]
    )
    return view

def create_sorting_view(sorting: SortingConfig):
    recording_folder = f'output/recordings/{sorting.recording}'
    sorting_folder = f'{recording_folder}/sortings/{sorting.sorter}'
    sorting_visualization_folder = f'output/visualizations/recordings/{sorting.recording}/sortings/{sorting.sorter}'
    
    # Load recording and sorting extractors
    recording_extractor: si.BaseRecording = si.load_extractor(f'{recording_folder}/recording_preprocessed')
    sorting_extractor = se.NpzSortingExtractor(f'{sorting_folder}/output/sorter_output/firings.npz')

    print('Loading traces')
    # Load traces
    traces = recording_extractor.get_traces()

    print('Computing templates')
    # Compute templates and peak channels
    templates = compute_templates(traces=traces, sorting=sorting_extractor)
    K = len(sorting_extractor.unit_ids)
    peak_channels = {
        sorting_extractor.unit_ids[i]: recording_extractor.channel_ids[np.argmin(np.min(templates[i], axis=0))]
        for i in range(K)
    }
    
    # Create sorting.json
    print('Creating sorting.json')
    sorting_data = {
        'samplingFrequency': sorting_extractor.get_sampling_frequency(),
        'units': [
            {
                'unitId': unit_id,
                'peakChannelId': peak_channels[unit_id],
                'spikeTrain': sorting_extractor.get_unit_spike_train(unit_id).astype(np.int32)
            }
            for unit_id in sorting_extractor.unit_ids
            if len(sorting_extractor.get_unit_spike_train(unit_id)) > 0
        ]
    }
    with open(f'{sorting_visualization_folder}/sorting.json', 'w') as f:
        json.dump(fg.serialize_data(sorting_data), f)

    v_ut = create_units_table_view(sorting=sorting_extractor)
    v_traces = vv.EphysTraces(
        format='spikeinterface.binary',
        uri=f'rtcshare://recordings/{sorting.recording}/recording_preprocessed',
        sorting_uri='$dir/sorting.json'
    )
    view = vv.Box(
        direction='horizontal',
        items=[
            vv.LayoutItem(view=v_ut, min_size=150, max_size=150),
            vv.LayoutItem(view=v_traces)
        ]
    )
    return view

def compute_templates(*, traces: npt.NDArray[np.float32], sorting: si.BaseSorting):
    unit_ids = sorting.unit_ids
    K = len(unit_ids)
    M = traces.shape[1]
    T1 = 20
    T2 = 20
    T = T1 + T2
    print('Compute templates')
    templates = np.zeros((K, T, M), dtype=np.float32)
    for i in range(K):
        unit_id = unit_ids[i]
        times1 = sorting.get_unit_spike_train(unit_id, segment_index=0)
        snippets1 = extract_snippets(traces, times=times1, T1=T1, T2=T2)
        templates[i] = np.median(snippets1, axis=0)
    return templates

def create_units_table_view(sorting: si.BaseSorting):
    v_ut = vv.UnitsTable(
        columns=[
        ],
        rows=[
            vv.UnitsTableRow(unit_id, {
            })
            for unit_id in sorting.unit_ids
        ]
    )
    return v_ut

if __name__ == '__main__':
    main()