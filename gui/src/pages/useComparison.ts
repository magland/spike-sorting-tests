import { useRtcshareJsonFile } from "./useRtcshareFile"

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

export default useComparison