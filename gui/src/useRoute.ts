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
} | {
    page: 'comparison'
    recordingId: string
    sorterId1: string
    sorterId2: string
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
        else if (location.pathname.startsWith('/comparison/')) {
            const a = location.pathname.split('/')
            const recordingId = a[2]
            const sorterId1 = a[3]
            const sorterId2 = a[4]
            return {
                page: 'comparison',
                recordingId,
                sorterId1,
                sorterId2
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
        else if (r.page === 'comparison') {
            navigate({...location, pathname: `/comparison/${r.recordingId}/${r.sorterId1}/${r.sorterId2}`})
        }
    }, [location, navigate])

    return {
        route,
        setRoute
    }    
}

export default useRoute