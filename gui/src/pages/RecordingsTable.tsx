import { Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material'
import React, { FunctionComponent } from 'react'
import Hyperlink from '../components/Hyperlink'
import { RecordingConfig, SortingConfig } from '../SpikeSortingConfig'
import useRoute from '../useRoute'
import './CustomTable.css'
import useRecordingInfo from './useRecordingInfo'

type Props = {
    recordings: RecordingConfig[]
    sortings: SortingConfig[]
}

const RecordingsTable: FunctionComponent<Props> = ({ recordings, sortings }) => {
    return (
        <Table className="CustomTable">
            <TableHead>
                <TableRow>
                    <TableCell>Recording</TableCell>
                    <TableCell>Num. chan.</TableCell>
                    <TableCell>Sampling freq. (Hz)</TableCell>
                    <TableCell>Duration (sec)</TableCell>
                    <TableCell>Num. true units</TableCell>
                    <TableCell>Notes</TableCell>
                    <TableCell>Sortings</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {
                    recordings.map(r => (
                        <RecordingRow key={r.id} recording={r} sortings={sortings} />
                    ))
                }
            </TableBody>
        </Table>
    )
}

const RecordingRow: FunctionComponent<{recording: RecordingConfig, sortings: SortingConfig[]}> = ({recording, sortings}) => {
    const {setRoute} = useRoute()
    const recordingInfo = useRecordingInfo(recording.id)
    const r = recording
    return (
        <TableRow key={r.id}>
            <TableCell>
                <Hyperlink onClick={() => setRoute({page: 'recording', recordingId: r.id})}>{r.id}</Hyperlink>
            </TableCell>
            <TableCell>
                {recordingInfo.info ? (recordingInfo.info.num_channels) : <span />}
            </TableCell>
            <TableCell>
                {recordingInfo.info ? (recordingInfo.info.sampling_frequency) : <span />}
            </TableCell>
            <TableCell>
                {recordingInfo.info ? (recordingInfo.info.duration_sec.toFixed(0)) : <span />}
            </TableCell>
            <TableCell>
                {recordingInfo.info ? (recordingInfo.info.num_true_units) : <span />}
            </TableCell>
            <TableCell>{r.notes}</TableCell>
            <TableCell>
                <SortingsForRecordingElement sortings={sortings} recordingId={r.id} />
            </TableCell>
        </TableRow>
    )
}

const SortingsForRecordingElement: FunctionComponent<{sortings: SortingConfig[], recordingId: string}> = ({sortings, recordingId}) => {
    const {setRoute} = useRoute()
    const sortingsForRecording = sortings.filter(s => s.recording === recordingId)
    return (
        <div style={{overflow: 'hidden'}}>
            {
                sortingsForRecording.map((s, i) => (
                    <div style={{float: 'left'}} key={s.sorter}>
                        {i > 0 && <span>&nbsp;|&nbsp;</span>}
                        <Hyperlink onClick={() => setRoute({page: 'sorting', recordingId, sorterId: s.sorter})}>{s.sorter}</Hyperlink>
                    </div>
                ))
            }
        </div>
    )
}

export default RecordingsTable