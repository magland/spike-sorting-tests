import { useMemo } from "react"
import { useRtcshareJsonFile } from "./useRtcshareFile"

type SpikeInterfaceLog = {
    sorter_name: string
    sorter_version: string
    datetime: string
    runtime_trace: any[]
    error: boolean
    run_time: number
}

type SpikeInterfaceParams = {
    sorter_name: string
    sorter_params: any
}

const useSortingInfo = (recordingId: string, sorterId: string): {
    info: {num_units: number} | undefined
    spikeInterfaceLog: SpikeInterfaceLog | undefined
    spikeInterfaceParams: SpikeInterfaceParams | undefined
} => {
    const pathDir = `recordings/${recordingId}/sortings/${sorterId}`

    const spikeinterfaceLogPath = `${pathDir}/output/spikeinterface_log.json`
    const {content: spikeInterfaceLog} = useRtcshareJsonFile(spikeinterfaceLogPath)

    const spikeinterfaceParamsPath = `${pathDir}/output/spikeinterface_params.json`
    const {content: spikeInterfaceParams} = useRtcshareJsonFile(spikeinterfaceParamsPath)

    const infoPath = `${pathDir}/sorting_info.json`
    const {content: sortingInfo} = useRtcshareJsonFile(infoPath)

    const info = useMemo(() => ({
        info: sortingInfo ? sortingInfo as {num_units: number} : undefined,
        spikeInterfaceLog: spikeInterfaceLog ? spikeInterfaceLog as SpikeInterfaceLog : undefined,
        spikeInterfaceParams: spikeInterfaceParams ? spikeInterfaceParams as any : undefined
    }), [spikeInterfaceLog, spikeInterfaceParams, sortingInfo])
    return info
}

export default useSortingInfo