import { ExpandLess, ExpandMore } from '@mui/icons-material'
import { Table, TableBody, TableCell, TableRow } from '@mui/material'
import { FunctionComponent, PropsWithChildren, useState } from 'react'
import Hyperlink from '../components/Hyperlink'
import useRoute from '../useRoute'
import ComparisonAgreementsTable from './ComparisonAgreementsTable'
import ComparisonsTable from './ComparisonsTable'
import SortingFigurlLink from './SortingFigurlLink'
import useSortingInfo from './useSortingInfo'
import useSortingOutputLog from './useSortingOutputLog'

const SortingPage: FunctionComponent<{recordingId: string, sorterId: string}> = ({recordingId, sorterId}) => {
    const {setRoute} = useRoute()

    const sortingInfo = useSortingInfo(recordingId, sorterId)

    return (
        <div style={{margin: 20}}>
            <p><Hyperlink onClick={() => setRoute({page: 'home'})}>Back to recordings</Hyperlink></p>
            <h3>Sorting</h3>
            <Table className="CustomTable" style={{maxWidth: 1000}}>
                <TableBody>
                    <TableRow key="recordingId">
                        <TableCell style={{fontWeight: 'bold'}}>Recording:</TableCell>
                        <TableCell><Hyperlink onClick={() => setRoute({page: 'recording', recordingId})}>{recordingId}</Hyperlink></TableCell>
                    </TableRow>
                    <TableRow key="sorterId">
                        <TableCell style={{fontWeight: 'bold'}}>Sorter:</TableCell>
                        <TableCell>{sorterId}</TableCell>
                    </TableRow>
                    <TableRow key="sorterParams">
                        <TableCell style={{fontWeight: 'bold'}}>Sorter params:</TableCell>
                        <TableCell><FormattedSorterParams sorterParams={sortingInfo.spikeInterfaceParams?.sorter_params}/></TableCell>
                    </TableRow>
                    <TableRow key="runTime">
                        <TableCell style={{fontWeight: 'bold'}}>Run time (sec):</TableCell>
                        <TableCell>{formatNumber(sortingInfo.spikeInterfaceLog?.run_time, 2)}</TableCell>
                    </TableRow>
                    <TableRow key="numUnits">
                        <TableCell style={{fontWeight: 'bold'}}>Num. units:</TableCell>
                        <TableCell>{sortingInfo.info?.num_units}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
            <p>
                <SortingFigurlLink recordingId={recordingId} sorterId={sorterId} />
            </p>
            <hr />
            <h3>Comparisons</h3>
            <ComparisonsTable recordingId={recordingId} sorterId={sorterId} />
            <hr />
            <ComparisonAgreementsTable recordingId={recordingId} sorterId={sorterId} />
            <hr />
            <Expandable label="Output log">
                <OutputLog recordingId={recordingId} sorterId={sorterId} />
            </Expandable>
        </div>
    )
}

export const formatNumber = (num: number | undefined, precision: number) => {
    return num !== undefined ? num.toFixed(precision) : undefined
}

const FormattedSorterParams: FunctionComponent<{sorterParams: {[key: string]: any} | undefined}> = ({sorterParams}) => {
    if (!sorterParams) return <span>None</span>
    return (
        <div>{JSON.stringify(sorterParams, undefined, 2)}</div>
    )
}

const Expandable: FunctionComponent<PropsWithChildren<{label: string}>> = ({label, children}) => {
    const [expanded, setExpanded] = useState(false)
    return (
        <div>
            <div onClick={() => {setExpanded(!expanded)}} style={{cursor: 'pointer'}}>
                {expanded ? <ExpandMore /> : <ExpandLess />}
                {label}
            </div>
            {expanded && children}
        </div>
    )
}

const OutputLog: FunctionComponent<{recordingId: string, sorterId: string}> = ({recordingId, sorterId}) => {
    const outputLog = useSortingOutputLog(recordingId, sorterId)
    return (
        <div>
            <pre>{outputLog}</pre>
        </div>
    )
}

export default SortingPage