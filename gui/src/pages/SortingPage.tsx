import { FunctionComponent, PropsWithChildren, useMemo, useState } from 'react'
import { serviceBaseUrl } from '../config'
import { useRtcshareYamlFile } from './useRtcshareFile'
import { Table, TableBody, TableCell, TableRow } from '@mui/material'
import useSortingInfo from './useSortingInfo'
import useSortingOutputLog from './useSortingOutputLog'
import { ExpandLess, ExpandMore, ExpandRounded } from '@mui/icons-material'
import Hyperlink from '../components/Hyperlink'
import useRoute from '../useRoute'

const SortingPage: FunctionComponent<{recordingId: string, sorterId: string}> = ({recordingId, sorterId}) => {
    const {setRoute} = useRoute()
    const pathDir = `visualizations/recordings/${recordingId}/sortings/${sorterId}`
    const path = `${pathDir}/view.yaml`
    const {content: viewYaml} = useRtcshareYamlFile(path)
    const viewUrl = useMemo(() => {
        if (!viewYaml) return undefined
        return `https://figurl.org/f?v=${viewYaml.v}&d=${viewYaml.d}&dir=rtcshare://${pathDir}&sh=${serviceBaseUrl}&label=${encodeURIComponent(viewYaml.label)}`
    }, [viewYaml, pathDir])

    const sortingInfo = useSortingInfo(recordingId, sorterId)

    return (
        <div style={{margin: 20}}>
            <p><Hyperlink onClick={() => setRoute({page: 'home'})}>Back to recordings</Hyperlink></p>
            <Table className="CustomTable">
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
                </TableBody>
            </Table>
            <p>
                {viewUrl && <a href={viewUrl} target="_blank" rel="noreferrer">View sorting</a>}
            </p>
            <hr />
            <Expandable label="Output log">
                <OutputLog recordingId={recordingId} sorterId={sorterId} />
            </Expandable>
        </div>
    )
}

const formatNumber = (num: number | undefined, precision: number) => {
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