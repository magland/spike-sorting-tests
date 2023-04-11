import { FunctionComponent, useContext } from "react";
import { SpikeSortingConfigContext } from "../MainWindow";
import RecordingsTable from "./RecordingsTable";

const Home: FunctionComponent = () => {
    const spikeSortingConfig = useContext(SpikeSortingConfigContext)
    return (
        <div style={{margin: 20}}>
            <RecordingsTable recordings={spikeSortingConfig.recordings} sortings={spikeSortingConfig.sortings} />
        </div>
    )
}

export default Home