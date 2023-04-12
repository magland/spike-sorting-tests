import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import { FunctionComponent, useContext, useMemo } from "react"
import Hyperlink from "../components/Hyperlink"
import { SpikeSortingConfigContext } from "../MainWindow"
import useRoute from "../useRoute"

const ComparisonsTable: FunctionComponent<{recordingId: string, sorterId: string}> = ({recordingId, sorterId}) => {
    const {setRoute} = useRoute()
    const {sortings} = useContext(SpikeSortingConfigContext)
    const sorterIds = useMemo(() => (
        sortings.filter(s => (s.recording === recordingId && s.sorter !== sorterId)).map(s => s.sorter)
    ), [sortings, recordingId, sorterId])
    return (
        <Table className="CustomTable">
            <TableHead>
                <TableCell>Sorter</TableCell>
            </TableHead>
            <TableBody>
                {
                    sorterIds.map(sorterId2 => (
                        <TableRow key={sorterId2}>
                            <TableCell>
                                <Hyperlink onClick={() => setRoute({page: 'comparison', recordingId, sorterId1: sorterId, sorterId2: sorterId2})}>{sorterId2}</Hyperlink>
                            </TableCell>
                        </TableRow>
                    ))
                }
            </TableBody>
        </Table>
    )
}

export default ComparisonsTable