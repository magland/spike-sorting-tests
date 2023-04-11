import { useCallback, useMemo } from "react"
import { useLocation, useNavigate } from "react-router-dom"

export type Route = {
    page: 'home'
} | {
    page: 'recording'
    recordingId: string
} | {
    page: 'sorting'
    recordingId: string
    sorterId: string
}

const useRoute = () => {
    const location = useLocation()
    const navigate = useNavigate()

    const route: Route = useMemo(() => {
        if (location.pathname.startsWith('/recording/')) {
            const a = location.pathname.split('/')
            const recordingId = a[2]
            return {
                page: 'recording',
                recordingId
            }
        }
        else if (location.pathname.startsWith('/sorting/')) {
            const a = location.pathname.split('/')
            const recordingId = a[2]
            const sorterId = a[3]
            return {
                page: 'sorting',
                recordingId,
                sorterId
            }
        }
        else {
            return {
                page: 'home'
            }
        }
    }, [location])

    const setRoute = useCallback((r: Route) => {
        if (r.page === 'home') {
            navigate({...location, pathname: ''})
        }
        else if (r.page === 'recording') {
            navigate({...location, pathname: `/recording/${r.recordingId}`})
        }
        else if (r.page === 'sorting') {
            navigate({...location, pathname: `/sorting/${r.recordingId}/${r.sorterId}`})
        }
    }, [location, navigate])

    return {
        route,
        setRoute
    }    
}

export default useRoute