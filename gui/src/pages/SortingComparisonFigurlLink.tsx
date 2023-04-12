import { FunctionComponent, useMemo } from "react"
import { serviceBaseUrl } from "../config"
import { useRtcshareYamlFile } from "./useRtcshareFile"

const SortingComparisonFigurlLink: FunctionComponent<{recordingId: string, sorterId1: string, sorterId2: string}> = ({recordingId, sorterId1, sorterId2}) => {
    const pathDir = `visualizations/recordings/${recordingId}/sortings/${sorterId1}/comparisons/${sorterId2}`
    const path = `${pathDir}/view.yaml`
    const {content: viewYaml} = useRtcshareYamlFile(path)
    const viewUrl = useMemo(() => {
        if (!viewYaml) return undefined
        return `https://figurl.org/f?v=${viewYaml.v}&d=${viewYaml.d}&dir=rtcshare://${pathDir}&sh=${serviceBaseUrl}&label=${encodeURIComponent(viewYaml.label)}`
    }, [viewYaml, pathDir])
    if (!viewUrl) return <span />
    return (
        <a href={viewUrl} target="_blank" rel="noreferrer">View comparison</a>
    )
}

export default SortingComparisonFigurlLink
