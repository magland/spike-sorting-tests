import os
import json
import shutil
import time
import numpy as np
import spikeinterface as si
from core.config_classes import SpikeSortingTestsConfig, SortingConfig


def execute_single_comparison(config: SpikeSortingTestsConfig, sorting1_config: SortingConfig, sorting2_config: SortingConfig):
    sorter1 = next((s for s in config.sorters if s.id == sorting1_config.sorter), None)
    sorter2 = next((s for s in config.sorters if s.id == sorting2_config.sorter), None)
    if sorter1 is None:
        print(f'Sorter {sorting1_config.sorter} not found in config. Skipping.')
        return
    if sorter2 is None:
        print(f'Sorter {sorting2_config.sorter} not found in config. Skipping.')
        return
    recording = next((r for r in config.recordings if r.id == sorting1_config.recording), None)
    if recording is None:
        print(f'Recording {sorting1_config.recording} not found in config. Skipping.')
        return

    recording_folder = f'output/recordings/{recording.id}'
    if not os.path.exists(recording_folder):
        os.mkdir(recording_folder)
    if not os.path.exists(f'{recording_folder}/sortings'):
        os.mkdir(f'{recording_folder}/sortings')
    sorting1_folder = f'{recording_folder}/sortings/{sorter1.id}'
    if not os.path.exists(sorting1_folder):
        os.mkdir(sorting1_folder)
    sorting2_folder = f'{recording_folder}/sortings/{sorter2.id}'
    if not os.path.exists(sorting2_folder):
        os.mkdir(sorting2_folder)
    
    if not os.path.exists(f'output/recordings/{recording.id}/recording'):
        print('Recording directory does not exist. Skipping.')
        return

    if not os.path.exists(f'{sorting1_folder}/sorting.npz'):
        print('Sorting result does not exist. Skipping.')
        return
    
    if not os.path.exists(f'{sorting2_folder}/sorting.npz'):
        print('Sorting result does not exist. Skipping.')
        return
    
    if not os.path.exists(f'{sorting1_folder}/comparisons'):
        os.mkdir(f'{sorting1_folder}/comparisons')
    
    comparison_folder = f'{sorting1_folder}/comparisons/{sorter2.id}'
    if os.path.exists(comparison_folder + '/comparison_info.json'):
        print('Comparison already exists. Skipping.')
        return
    
    if os.path.exists(comparison_folder):
        shutil.rmtree(comparison_folder)
    
    os.mkdir(comparison_folder)

    sorting1_extractor = si.NpzSortingExtractor(sorting1_folder + '/sorting.npz')
    sorting2_extractor = si.NpzSortingExtractor(sorting2_folder + '/sorting.npz')

    comparison = do_comparison(sorting1_extractor, sorting2_extractor)

    with open(f'{comparison_folder}/comparison.json', 'w') as f:
        json.dump(comparison, f)
    
    comparison_info = {
        'timestamp': time.time()
    }
    with open(f'{comparison_folder}/comparison_info.json', 'w') as f:
        json.dump(comparison_info, f)

def do_comparison(sorting1: si.BaseSorting, sorting2: si.BaseSorting, tol=20):
    event_counts1 = []
    event_counts2 = []
    matching_event_counts = []
    unit_ids1 = sorting1.unit_ids
    unit_ids2 = sorting2.unit_ids
    for uid1 in unit_ids1:
        event_counts1.append({
            'id': int(uid1),
            'count': len(sorting1.get_unit_spike_train(uid1))
        })
    for uid2 in unit_ids2:
        event_counts2.append({
            'id': int(uid2),
            'count': len(sorting2.get_unit_spike_train(uid2))
        })
    for uid1 in unit_ids1:
        st1 = sorting1.get_unit_spike_train(uid1)
        for uid2 in unit_ids2:
            if uid1 == uid2:
                continue
            st2 = sorting2.get_unit_spike_train(uid2)
            num = get_num_matching_events(np.array(st1), np.array(st2), tol)
            if (num >= 0.05 * len(st1)) and (num >= 0.05 * len(st2)):
                matching_event_counts.append({
                    'id1': int(uid1),
                    'id2': int(uid2),
                    'count': num
                })
    return {
        'event_counts1': event_counts1,
        'event_counts2': event_counts2,
        'matching_event_counts': matching_event_counts
    }

def get_num_matching_events(st1: np.array, st2: np.array, tol: int):
    num_matching_events = 0
    i = 0
    for t in st1:
        while i < len(st2) and st2[i] < t - tol:
            i += 1
        if i < len(st2) and st2[i] <= t + tol:
            num_matching_events += 1
            i += 1
    return num_matching_events