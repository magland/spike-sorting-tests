import WebrtcConnectionToService from "./WebrtcConnectionToService"

const urlSearchParams = new URLSearchParams(window.location.search)
const queryParams = Object.fromEntries(urlSearchParams.entries())

export const defaultServiceBaseUrl = 'http://localhost:61752'

export const serviceBaseUrl = queryParams.sh ? ( // remove the queryParams.s in the future
    queryParams.sh // remove the queryParams.s in the future
) : (
    defaultServiceBaseUrl
)

export const useWebrtc = queryParams.webrtc !== '0'

export let webrtcConnectionToService: WebrtcConnectionToService | undefined

if ((useWebrtc) && (!webrtcConnectionToService)) {
    webrtcConnectionToService = new WebrtcConnectionToService()
}