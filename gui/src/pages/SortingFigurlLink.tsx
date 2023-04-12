import { FunctionComponent, useMemo } from "react"
import { serviceBaseUrl } from "../config"
import { useRtcshareYamlFile } from "./useRtcshareFile"

const SortingFigurlLink: FunctionComponent<{recordingId: string, sorterId: string}> = ({recordingId, sorterId}) => {
    const pathDir = `visualizations/recordings/${recordingId}/sortings/${sorterId}`
    const path = `${pathDir}/view.yaml`
    const {content: viewYaml} = useRtcshareYamlFile(path)
    const viewUrl = useMemo(() => {
        if (!viewYaml) return undefined
        return `https://figurl.org/f?v=${viewYaml.v}&d=${viewYaml.d}&dir=rtcshare://${pathDir}&sh=${serviceBaseUrl}&label=${encodeURIComponent(viewYaml.label)}`
    }, [viewYaml, pathDir])
    if (!viewUrl) return <span />
    return (
        <a href={viewUrl} target="_blank" rel="noreferrer">View sorting</a>
    )
}

export default SortingFigurlLink
