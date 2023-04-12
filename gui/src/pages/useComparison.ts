import { useMemo } from "react"
import { useRtcshareJsonFile, useRtcshareJsonFiles } from "./useRtcshareFile"

export type Comparison = {
    event_counts1: {id: number, count: number}[]
    event_counts2: {id: number, count: number}[]
    matching_event_counts: {id1: number, id2: number, count: number}[]
}

const useComparison = (recordingId: string, sorterId1: string, sorterId2: string) => {
    const pathDir = `recordings/${recordingId}/sortings/${sorterId1}/comparisons/${sorterId2}`

    const comparisonJsonPath = `${pathDir}/comparison.json`
    const {content: comparison} = useRtcshareJsonFile(comparisonJsonPath)

    return {
        comparison: comparison ? comparison as Comparison : undefined
    }
}

export const useComparisons = (recordingId: string, sorterId1: string, sorterId2s: string[]) => {
    const pathDirs = useMemo(() => ( // important to memoize this
        sorterId2s.map(sorterId2 => (`recordings/${recordingId}/sortings/${sorterId1}/comparisons/${sorterId2}`))
    ), [recordingId, sorterId1, sorterId2s])

    const comparisonJsonPaths = useMemo(() => ( // important to memoize this
        pathDirs.map(pathDir => (`${pathDir}/comparison.json`))
    ), [pathDirs])
    const {contents: comparisons} = useRtcshareJsonFiles(comparisonJsonPaths)

    return {
        comparisons: comparisons ? comparisons as (Comparison | undefined)[] : undefined
    }
}

export default useComparison