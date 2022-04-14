import React, { useState, useEffect } from "react"
import LocationList from "../components/LocationList"
import FormDialog from "../components/FormDialog"
import LocationService from "../services/LocationService"
import ILocation from "../types/Location"
import { ThemeProvider } from "@material-ui/core/styles"
import theme from "../theme"
import { Container } from "@material-ui/core" //importing material ui component


// export interface IGamePageProps {}
const GamePage: React.FC = () => {
    const [location, setlocation] = useState<Array<ILocation>>([])
    const [fetchIsDone, setFetchIsDone] = useState(false)
  
    useEffect(() => {
        retrievelocations()
    }, [])
    const retrievelocations = () => {
        LocationService.getAll()
            .then((response: any) => {
                setlocation(response.data.items)
                setFetchIsDone(true)
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }
    console.log(location)
    return (
        <ThemeProvider theme={theme}>
            <Container className="Home">
                {fetchIsDone && <LocationList locations={location}/>}
                <FormDialog/>
            </Container>
        </ThemeProvider>
    )
}

export default GamePage