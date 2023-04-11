import { useRtcshareTextFile } from "./useRtcshareFile"

const useSortingOutputLog = (recordingId: string, sorterId: string): string | undefined => {
    const pathDir = `recordings/${recordingId}/sortings/${sorterId}`

    const outputLogPath = `${pathDir}/output.log`

    const {content: outputLog} = useRtcshareTextFile(outputLogPath)

    return outputLog
}

export default useSortingOutputLog