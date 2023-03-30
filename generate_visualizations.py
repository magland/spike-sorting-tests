import os
import argparse
import yaml
import json
import shutil
from typing import List, Dict
import numpy as np
import numpy.typing as npt
import spikeinterface as si
import spikeinterface.extractors as se
import sortingview.views as vv
import figurl as fg
from load_config import load_config
from config_classes import RecordingConfig, SortingConfig
from extract_snippets import extract_snippets
from helpers.create_autocorrelograms_view import create_autocorrelograms_view
from helpers.compute_correlogram_data import compute_correlogram_data


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
            shutil.rmtree(f'{recording_visualization_folder}/sha1')
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
            shutil.rmtree(f'{sorting_visualization_folder}/sha1')
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

    print('Creating units table view')
    v_ut = create_units_table_view(sorting=sorting_extractor)

    print('Creating auto-correlograms view')
    v_ac = create_autocorrelograms_view(sorting=sorting_extractor)

    print('Loading traces')
    # Load traces
    traces = recording_extractor.get_traces()

    # Get channel locations
    channel_locations = recording_extractor.get_channel_locations()

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
    
    v_cc = create_cross_correlograms_view(
        sorting=sorting_extractor,
        adjacency_radius=150,
        channel_locations=channel_locations,
        peak_channels=peak_channels,
        channel_ids=recording_extractor.channel_ids
    )

    print('Creating average waveforms view')
    channel_locations_dict = {
        str(channel_id): channel_locations[i].astype(np.float32).tolist()
        for i, channel_id in enumerate(recording_extractor.channel_ids)
    }
    average_waveform_items: List[vv.AverageWaveformItem] = []
    for i, unit_id in enumerate(sorting_extractor.unit_ids):
        peak_channel_id = peak_channels[unit_id]
        neighborhood_channel_indices, neighborhood_channel_ids = get_channel_neighborhood(channel_locations=channel_locations, channel_ids=recording_extractor.channel_ids, channel_id=peak_channel_id, radius=100)
        average_waveform_items.append(vv.AverageWaveformItem(
            unit_id=unit_id,
            channel_ids=neighborhood_channel_ids,
            waveform=templates[i][:, neighborhood_channel_indices].T
        ))
    v_aw = vv.AverageWaveforms(
        channel_locations=channel_locations_dict,
        average_waveforms=average_waveform_items,
        show_reference_probe=False
    )

    v_traces = vv.EphysTraces(
        format='spikeinterface.binary',
        uri=f'rtcshare://recordings/{sorting.recording}/recording_preprocessed',
        sorting_uri='$dir/sorting.json'
    )

    v_tab = vv.TabLayout(
        items=[
            vv.TabLayoutItem(label='Traces', view=v_traces),
            vv.TabLayoutItem(label='Cross-correlograms', view=v_cc),
            vv.TabLayoutItem(label='Average waveforms', view=v_aw)
        ]
    )

    view = vv.Box(
        direction='horizontal',
        items=[
            vv.LayoutItem(view=v_ut, min_size=150, max_size=150),
            vv.LayoutItem(view=vv.Box(
                direction='horizontal',
                items=[
                    vv.LayoutItem(view=v_ac, min_size=300, max_size=300),
                    vv.LayoutItem(view=v_tab)
                ]
            ))
        ]
    )
    return view

def compute_templates(*, traces: npt.NDArray[np.float32], sorting: si.BaseSorting):
    unit_ids = sorting.unit_ids
    K = len(unit_ids)
    M = traces.shape[1]
    T1 = 30
    T2 = 30
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

def get_channel_neighborhood(*, channel_locations: npt.NDArray[np.float32], channel_ids: List[int], channel_id: int, radius: int):
    channel_index = [id for id in channel_ids].index(channel_id)
    channel_location = channel_locations[channel_index]
    dists = np.sqrt(np.sum((channel_locations - channel_location) ** 2, axis=1))
    neighborhood_channel_indices = np.where(dists <= radius)[0]
    neighborhood_channel_ids = [channel_ids[i] for i in neighborhood_channel_indices]
    return neighborhood_channel_indices, neighborhood_channel_ids

def create_cross_correlograms_view(*,
    sorting: si.BaseSorting,
    adjacency_radius: int,
    channel_locations: npt.NDArray[np.float32],
    peak_channels: Dict[int, int],
    channel_ids: List
):
    M = len(channel_ids)
    adjacency = {}
    for m in range(M):
        adjacency[channel_ids[m]] = []
        for m2 in range(M):
            dist0 = np.sqrt(np.sum((channel_locations[m] - channel_locations[m2]) ** 2))
            if dist0 <= adjacency_radius:
                adjacency[channel_ids[m]].append(channel_ids[m2])

    # cross-correlograms
    print('Cross correlograms')
    cross_correlogram_items: List[vv.CrossCorrelogramItem] = []
    for unit_id1 in sorting.unit_ids:
        for unit_id2 in sorting.unit_ids:
            if peak_channels[unit_id1] in adjacency[peak_channels[unit_id2]]:
                a = compute_correlogram_data(sorting=sorting, unit_id1=unit_id1, unit_id2=unit_id2, window_size_msec=80, bin_size_msec=1)
                bin_edges_sec = a['bin_edges_sec']
                bin_counts = a['bin_counts']
                cross_correlogram_items.append(
                    vv.CrossCorrelogramItem(
                        unit_id1 = unit_id1,
                        unit_id2 = unit_id2,
                        bin_edges_sec = bin_edges_sec,
                        bin_counts = bin_counts
                    )
                )
    v_cc = vv.CrossCorrelograms(
        cross_correlograms=cross_correlogram_items,
        hide_unit_selector=True
    )
    return v_cc

if __name__ == '__main__':
    main()