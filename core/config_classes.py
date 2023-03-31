from typing import List
from dataclasses import dataclass

@dataclass
class RecordingConfig:
    id: str
    type: str
    parameters: dict
    notes: str = ""

@dataclass
class SorterConfig:
    id: str
    type: str
    algorithm: str
    sorting_parameters: dict

@dataclass
class SortingConfig:
    recording: str
    sorter: str

@dataclass
class SpikeSortingTestsConfig:
    recordings: List[RecordingConfig]
    sorters: List[SorterConfig]
    sortings: List[SortingConfig]

def dict_to_spike_sorting_config(config_data):
    recordings = [RecordingConfig(**recording) for recording in config_data['recordings']]
    sorters = [SorterConfig(**sorter) for sorter in config_data['sorters']]
    sortings = [SortingConfig(**sorting) for sorting in config_data['sortings']]
    
    return SpikeSortingTestsConfig(recordings=recordings, sorters=sorters, sortings=sortings)