export type RecordingConfig = {
    type: 'spikeforest'
    id: string
    notes: string
    parameters: {
        study_name: string
        recording_name: string
    }
}

export type SorterConfig = {
    type: 'spikeinterface'
    id: string
    algorithm: string
    sorting_parameters: any
}

export type SortingConfig = {
    recording: string
    sorter: string
}

export type SpikeSortingConfig = {
    recordings: RecordingConfig[]
    sorters: SorterConfig[]
    sortings: SortingConfig[]
}