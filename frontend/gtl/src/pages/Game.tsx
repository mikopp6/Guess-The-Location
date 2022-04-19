import React, { useState, useEffect } from "react"
import { ThemeProvider } from "@material-ui/core/styles"
import { Container } from "@material-ui/core"
import { AxiosResponse } from "axios"

import theme from "../theme"
import LocationList from "../components/LocationList"
import FormDialog from "../components/FormDialog"
import LocationService from "../services/LocationService"
import ILocation from "../types/Location"


// export interface IGamePageProps {}
const GamePage: React.FC = () => {
    const [location, setlocation] = useState<Array<ILocation>>([])
    const [fetchIsDone, setFetchIsDone] = useState(false)
  
    useEffect(() => {
        retrievelocations()
    }, [])
    const retrievelocations = () => {
        LocationService.getAll()
            .then((response: AxiosResponse) => {
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