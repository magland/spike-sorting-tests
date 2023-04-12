import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import { FunctionComponent, useMemo } from "react"
import Hyperlink from "../components/Hyperlink"
import useRoute from "../useRoute"
import SortingFigurlLink from "./SortingFigurlLink"
import useComparison, { Comparison } from "./useComparison"

type Props = {
    recordingId: string
    sorterId1: string
    sorterId2: string
}

const ComparisonPage: FunctionComponent<Props> = ({recordingId, sorterId1, sorterId2}) => {
    const {setRoute} = useRoute()
    const {comparison} = useComparison(recordingId, sorterId1, sorterId2)
    const rows = useMemo(() => {
        const ret: {
            unit: number
            numEvents: number
            bestMatchingUnitId: number
            agreement: number
        }[] = []
        if (!comparison) return ret
        for (const a of comparison.event_counts1) {
            const {bestMatchingUnitId, agreement, numEvents} = getBestMatch(a.id, comparison)
            ret.push({
                unit: a.id,
                numEvents: numEvents,
                bestMatchingUnitId,
                agreement
            })
        }
        return ret
    }, [comparison])
    return (
        <div>
            <h3>Comparison</h3>
            <Table className="CustomTable">
                <TableBody>
                    <TableRow key="recordingId">
                        <TableCell style={{fontWeight: 'bold'}}>Recording:</TableCell>
                        <TableCell>
                            <Hyperlink onClick={() => setRoute({page: 'recording', recordingId})}>{recordingId}</Hyperlink>
                        </TableCell>
                    </TableRow>
                    <TableRow key="sorterId1">
                        <TableCell style={{fontWeight: 'bold'}}>Sorter 1 (reference):</TableCell>
                        <TableCell>
                            <Hyperlink onClick={() => setRoute({page: 'sorting', recordingId, sorterId: sorterId1})}>{sorterId1}</Hyperlink>
                            &nbsp;(
                                <SortingFigurlLink recordingId={recordingId} sorterId={sorterId1} />
                            )
                        </TableCell>
                    </TableRow>
                    <TableRow key="sorterId2">
                        <TableCell style={{fontWeight: 'bold'}}>Sorter 2:</TableCell>
                        <TableCell>
                            <Hyperlink onClick={() => setRoute({page: 'sorting', recordingId, sorterId: sorterId2})}>{sorterId2}</Hyperlink>
                            &nbsp;(
                                <SortingFigurlLink recordingId={recordingId} sorterId={sorterId2} />
                            )
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
            <hr />
            <Table className="CustomTable">
                <TableHead>
                    <TableCell>Unit</TableCell>
                    <TableCell>Num. events</TableCell>
                    <TableCell>Best matching unit</TableCell>
                    <TableCell>Agreement</TableCell>
                </TableHead>
                <TableBody>
                    {
                        rows.map(r => (
                            <TableRow key={r.unit}>
                                <TableCell>{r.unit}</TableCell>
                                <TableCell>{r.numEvents}</TableCell>
                                <TableCell>{r.bestMatchingUnitId}</TableCell>
                                <TableCell>{r.agreement.toFixed(3)}</TableCell>
                            </TableRow>
                        ))
                    }
                </TableBody>
            </Table>
        </div>
    )
}

function getBestMatch(unitId: number, comparison: Comparison) {
    let bestMatchingUnitId = -1
    let bestAgreement = -1

    const counts1: {[key: number]: number} = {}
    for (const a of comparison.event_counts1) {
        counts1[a.id] = a.count
    }
    const counts2: {[key: number]: number} = {}
    for (const a of comparison.event_counts2) {
        counts2[a.id] = a.count
    }

    for (const a of comparison.matching_event_counts) {
        const numer = a.count
        const denom = counts1[a.id1] + counts2[a.id2] - a.count
        const agreement = denom ? numer / denom : 0
        if ((a.id1 === unitId) && (agreement > bestAgreement)) {
            bestMatchingUnitId = a.id2
            bestAgreement = agreement
        }
    }
    return {bestMatchingUnitId, agreement: Math.max(bestAgreement, 0), numEvents: counts1[unitId]}
}

export default ComparisonPage