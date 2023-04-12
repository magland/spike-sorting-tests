import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import { FunctionComponent, useContext, useMemo } from "react"
import { SpikeSortingConfigContext } from "../MainWindow"
import { getBestMatch } from "./ComparisonPage"
import { Comparison, useComparisons } from "./useComparison"

const ComparisonAgreementsTable: FunctionComponent<{recordingId: string, sorterId: string}> = ({recordingId, sorterId}) => {
    const {sortings} = useContext(SpikeSortingConfigContext)
    const sorterIds = useMemo(() => (
        sortings.filter(s => (s.recording === recordingId && s.sorter !== sorterId)).map(s => s.sorter)
    ), [sortings, recordingId, sorterId])
    const {comparisons} = useComparisons(recordingId, sorterId, sorterIds)
    const rows = useMemo(() => {
        const ret: {
            unit: number
            agreements: number[]
        }[] = []
        if (!comparisons) return ret
        const firstDefinedComparison: Comparison | undefined = comparisons.find(c => (c !== undefined))
        if (!firstDefinedComparison) return ret
        for (const a of firstDefinedComparison.event_counts1) {
            const agreements: number[] = []
            for (const cc of comparisons) {
                if (cc) {
                    const {agreement} = getBestMatch(a.id, cc)
                    agreements.push(agreement)
                } else {
                    agreements.push(0)
                }
            }
            ret.push({
                unit: a.id,
                agreements
            })
        }
        return ret
    }, [comparisons])
    return (
        <Table className="CustomTable">
            <TableHead>
                <TableRow>
                    <TableCell>{sorterId} unit</TableCell>
                    {sorterIds.map(sorterId2 => (
                        <TableCell key={sorterId2}>{sorterId2}</TableCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody>
                {
                    rows.map(row => (
                        <TableRow key={row.unit}>
                            <TableCell>{row.unit}</TableCell>
                            {row.agreements.map((agreement, i) => (
                                <TableCell key={i}>{agreement.toFixed(3)}</TableCell>
                            ))}
                        </TableRow>
                    ))
                }
            </TableBody>
        </Table>
    )
}

export default ComparisonAgreementsTable