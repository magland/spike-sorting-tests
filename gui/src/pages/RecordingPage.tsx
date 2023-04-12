import { Table, TableBody, TableCell, TableRow } from '@mui/material'
import { FunctionComponent, useContext, useMemo } from 'react'
import Hyperlink from '../components/Hyperlink'
import { serviceBaseUrl } from '../config'
import { SpikeSortingConfigContext } from '../MainWindow'
import useRoute from '../useRoute'
import SortingsTable from './SortingsTable'
import useRecordingInfo from './useRecordingInfo'
import { useRtcshareYamlFile } from './useRtcshareFile'

const RecordingPage: FunctionComponent<{recordingId: string}> = ({recordingId}) => {
    const {setRoute} = useRoute()
    const spikeSortingConfig = useContext(SpikeSortingConfigContext)
    const sortings = spikeSortingConfig.sortings
    const pathDir = `visualizations/recordings/${recordingId}`
    const path = `${pathDir}/view.yaml`
    const {content: viewYaml} = useRtcshareYamlFile(path)
    const viewUrl = useMemo(() => {
        if (!viewYaml) return undefined
        return `https://figurl.org/f?v=${viewYaml.v}&d=${viewYaml.d}&dir=rtcshare://${pathDir}&sh=${serviceBaseUrl}&label=${encodeURIComponent(viewYaml.label)}`
    }, [viewYaml, pathDir])

    const {info} = useRecordingInfo(recordingId)

    return (
        <div style={{margin: 20}}>
            <p><Hyperlink onClick={() => setRoute({page: 'home'})}>Back to recordings</Hyperlink></p>
            <h3>Recording</h3>
            <Table className="CustomTable">
                <TableBody>
                    <TableRow key="recordingId">
                        <TableCell style={{fontWeight: 'bold'}}>Recording:</TableCell>
                        <TableCell>{recordingId}</TableCell>
                    </TableRow>
                    <TableRow key="samplingFrequency">
                        <TableCell style={{fontWeight: 'bold'}}>Sampling frequency (Hz):</TableCell>
                        <TableCell>{info?.sampling_frequency}</TableCell>
                    </TableRow>
                    <TableRow key="numChannels">
                        <TableCell style={{fontWeight: 'bold'}}>Num. channels:</TableCell>
                        <TableCell>{info?.num_channels}</TableCell>
                    </TableRow>
                    <TableRow key="durationSec">
                        <TableCell style={{fontWeight: 'bold'}}>Duration (sec):</TableCell>
                        <TableCell>{info?.duration_sec}</TableCell>
                    </TableRow>
                    <TableRow key="numTrueUnits">
                        <TableCell style={{fontWeight: 'bold'}}>Num. true units:</TableCell>
                        <TableCell>{info?.num_true_units}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
            <h3>Sortings</h3>
            <hr />
            <SortingsTable recordingId={recordingId} sortings={sortings} />
            <hr />
            <p>
                {viewUrl && <a href={viewUrl} target="_blank" rel="noreferrer">View recording with ground truth</a>}
            </p>
        </div>
    )
}

export default RecordingPage