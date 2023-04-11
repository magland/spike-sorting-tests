import { Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material'
import { FunctionComponent } from 'react'
import Hyperlink from '../components/Hyperlink'
import { SortingConfig } from '../SpikeSortingConfig'
import useRoute from '../useRoute'
import './CustomTable.css'
import { formatNumber } from './SortingPage'
import useSortingInfo from './useSortingInfo'

type Props = {
    recordingId: string
    sortings: SortingConfig[]
}

const SortingsTable: FunctionComponent<Props> = ({ recordingId, sortings }) => {
    return (
        <Table className="CustomTable">
            <TableHead>
                <TableRow>
                    <TableCell>Sorting</TableCell>
                    <TableCell>Num. units</TableCell>
                    <TableCell>Run time (sec)</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {
                    sortings.filter(s => (s.recording === recordingId)).map(s => (
                        <SortingRow key={s.sorter} sorting={s} />
                    ))
                }
            </TableBody>
        </Table>
    )
}

const SortingRow: FunctionComponent<{sorting: SortingConfig}> = ({sorting}) => {
    const {setRoute} = useRoute()
    const sortingInfo = useSortingInfo(sorting.recording, sorting.sorter)
    const s = sorting
    return (
        <TableRow key={s.sorter}>
            <TableCell>
                <Hyperlink onClick={() => setRoute({page: 'sorting', recordingId: s.recording, sorterId: s.sorter})}>{s.sorter}</Hyperlink>
            </TableCell>
            <TableCell>
                {sortingInfo.info ? (sortingInfo.info.num_units) : <span />}
            </TableCell>
            <TableCell>
                {sortingInfo.info ? (formatNumber(sortingInfo.spikeInterfaceLog?.run_time, 2)) : <span />}
            </TableCell>
        </TableRow>
    )
}

export default SortingsTable