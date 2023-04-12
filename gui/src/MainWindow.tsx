import React, { FunctionComponent, useEffect, useState } from "react";
import { defaultServiceBaseUrl, serviceBaseUrl, useWebrtc } from "./config";
import Home from "./pages/Home";
import useRoute from "./useRoute";
import { useRtcshare } from "./useRtcshare";
import YAML from 'js-yaml'
import { SpikeSortingConfig } from "./SpikeSortingConfig";
import RecordingPage from "./pages/RecordingPage";
import SortingPage from "./pages/SortingPage";
import ComparisonPage from "./pages/ComparisonPage";

type Props = any

const MainWindow: FunctionComponent<Props> = () => {
	const { route } = useRoute()

	const {connectedToService, webrtcConnectionStatus} = useRtcshare()

	const {client} = useRtcshare()
	const [spikeSortingConfig, setSpikeSortingConfig] = useState<SpikeSortingConfig>()

	useEffect(() => {
		if (!client) return
		;(async () => {
			const dec = new TextDecoder()
			const a = dec.decode(await client.readFile('spike_sorting_config.yaml'))
			const config = YAML.load(a) as SpikeSortingConfig
			setSpikeSortingConfig(config)
		})()
	}, [client])

	if (webrtcConnectionStatus === 'error') {
		return (
			<div>Unable to connect to service using WebRTC: {serviceBaseUrl}</div>
		)
	}

	if (connectedToService === undefined) {
		return (
			<div>Connecting to service{useWebrtc ? ' using WebRTC' : ''}: {serviceBaseUrl}</div>
		)
	}

	if (connectedToService === false) {
		return (
			<div style={{margin: 60}}>
				<div style={{color: 'darkred'}}>Not connected to service {serviceBaseUrl}</div>
				{
					serviceBaseUrl === defaultServiceBaseUrl && (
						<p><a href="https://github.com/scratchrealm/rtcshare" target="_blank" rel="noreferrer">How to run a local service</a></p>
					)
				}
			</div>
		)
	}

	return (
		<div>
			<SpikeSortingConfigContext.Provider value={spikeSortingConfig || defaultSpikeSortingConfig}>
				{
					route.page === 'home' ? (
						<Home />
					) : route.page === 'recording' ? (
						<RecordingPage recordingId={route.recordingId} />
					) : route.page === 'sorting' ? (
						<SortingPage recordingId={route.recordingId} sorterId={route.sorterId} />
					) : route.page === 'comparison' ? (
						<ComparisonPage recordingId={route.recordingId} sorterId1={route.sorterId1} sorterId2={route.sorterId2} />
					) : (
						<div>Unknown page: {(route as any).page}</div>
					)
				}
			</SpikeSortingConfigContext.Provider>
		</div>
	)
}

const defaultSpikeSortingConfig: SpikeSortingConfig = {
	recordings: [],
	sorters: [],
	sortings: []
}
export const SpikeSortingConfigContext = React.createContext<SpikeSortingConfig>(defaultSpikeSortingConfig)

export default MainWindow
