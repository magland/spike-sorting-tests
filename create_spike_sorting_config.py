import yaml


def main():
    # These are the sorters that we want to run
    sorters = [
        {
            'id': 'truth',
            'type': 'truth',
            'algorithm': 'truth',
            'sorting_parameters': {}
        },
        {
            'id': 'mountainsort5',
            'type': 'spikeinterface',
            'algorithm': 'mountainsort5',
            'sorting_parameters': {}
        },
        {
            'id': 'spykingcircus2',
            'type': 'spikeinterface',
            'algorithm': 'spykingcircus2',
            'sorting_parameters': {}
        },
        {
            'id': 'kilosort2_5',
            'type': 'spikeinterface',
            'algorithm': 'kilosort2_5',
            'sorting_parameters': {}
        },
    ]

    recordings = []
    sortings = []

    ########################################
    # paired_english
    # These are the recordings that have ground truth units with snr >= 7 as reported on the spikeforest website
    paired_english_recordings = [
        'm139_200114_222743',
        'm15_190315_152315_cell1',
        'm113_191125_213423',
        'm139_200114_230220',
        'm14_190326_160710_cell1'
    ]
    paired_english_sorters = ['truth', 'mountainsort5', 'spykingcircus2', 'kilosort2_5']
    for a in paired_english_recordings:
        recordings.append({
            'id': f'spikeforest.paired_english.{a}',
            'type': 'spikeforest',
            'parameters': {
                'study_name': 'paired_english',
                'recording_name': a
            },
            'notes': ''
        })
        for b in paired_english_sorters:
            sortings.append({
                'recording': f'spikeforest.paired_english.{a}',
                'sorter': b
            })
    
    ########################################
    # paired_kampff
    # These are the recordings that have ground truth units with snr >= 7 as reported on the spikeforest website
    paired_kampff_recordings = [
        '2014_11_25_Pair_3_0',
        '2015_09_03_Pair_9_0A',
        '2015_09_03_Pair_9_0B',
        'c14',
        'c26',
        'c28',
        'c45',
        'c46'
    ]
    paired_kampff_sorters = ['truth', 'mountainsort5', 'spykingcircus2', 'kilosort2_5']
    for a in paired_kampff_recordings:
        recordings.append({
            'id': f'spikeforest.paired_kampff.{a}',
            'type': 'spikeforest',
            'parameters': {
                'study_name': 'paired_kampff',
                'recording_name': a
            },
            'notes': ''
        })
        for b in paired_kampff_sorters:
            sortings.append({
                'recording': f'spikeforest.paired_kampff.{a}',
                'sorter': b
            })

    config = {
        'recordings': recordings,
        'sorters': sorters,
        'sortings': sortings
    }
    with open('spike_sorting_config.yaml', 'w') as f:
        yaml.dump(config, f)

# This function trims the whitespace the beginning and end of each line
def trim_lines(s: str):
    # First we split the string into lines
    lines = s.splitlines()
    # Then we strip the whitespace from the beginning and end of each line
    lines = [line.strip() for line in lines]
    # Finally we join the lines back together
    return '\n'.join(lines)

if __name__ == '__main__':
    main()