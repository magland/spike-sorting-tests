import { useMemo } from "react"
import { useRtcshareJsonFile } from "./useRtcshareFile"

const useRecordingInfo = (recordingId: string): {
    info: {
        recording_name: string
        study_name: string
        study_set_name: string
        sampling_frequency: number
        num_channels: number
        duration_sec: number
        num_true_units: number
    }
} => {
    const pathDir = `recordings/${recordingId}`

    const recordingInfoPath = `${pathDir}/recording_info.json`
    const {content: info} = useRtcshareJsonFile(recordingInfoPath)

    return {info}
}

export default useRecordingInfo