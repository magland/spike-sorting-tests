import os
import argparse
import yaml
import sortingview.views as vv
from load_config import load_config
from config_classes import RecordingConfig, SortingConfig


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
        sorting_visualization_folder = f'output/visualizations/recordings/{sorting.recording}/sortings/{sorting.sorter}'
        if not os.path.exists(sorting_visualization_folder):
            os.makedirs(sorting_visualization_folder)
        if not os.path.exists(f'{sorting_visualization_folder}/view.yaml'):
            view = create_sorting_view(sorting)
            os.environ['KACHERY_STORE_FILE_DIR'] = f'{recording_visualization_folder}'
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
    view_traces = vv.EphysTraces(
        format='spikeinterface.binary',
        uri=f'rtcshare://recordings/{sorting.recording}/recording_preprocessed'
    )
    view = vv.TabLayout(
        items=[
            vv.TabLayoutItem(label='Traces', view=view_traces)
        ]
    )
    return view

if __name__ == '__main__':
    main()