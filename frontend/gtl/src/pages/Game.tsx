import React, { useState, useEffect } from "react"
import { ThemeProvider } from "@material-ui/core/styles"
import { Container } from "@material-ui/core"
import { AxiosResponse } from "axios"

import theme from "../theme"
import SingleGame from "../components/SingleGame"
import FormDialog from "../components/FormDialog"
import LocationService from "../services/LocationService"
import ILocation from "../types/Location"


// export interface IGamePageProps {}
const GamePage: React.FC = () => {
    const [allLocations, setlocations] = useState<Array<ILocation>>([])
    const [fetchIsDone, setFetchIsDone] = useState(false)
    const [count, setCount] = useState(0)
    const [answer, setAnswer] = useState()
  
    useEffect(() => {
        retrievelocations()
    }, [])
    const retrievelocations = () => {
        LocationService.getAll()
            .then((response: AxiosResponse) => {
                randomlocations(response.data.items)
                setFetchIsDone(true)
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }
    const randomlocations = (data: any) => {
        const newArray: any = []
        for (let i = 0; i < 5; i++) {
            newArray.push(data[i])
        }
        setlocations(newArray)
    }
    if (count < 5) {
        return (
            <ThemeProvider theme={theme}>
                <Container className="Home">
                    {fetchIsDone && <SingleGame locations={allLocations} answer={answer} count={count}/>}
                    <FormDialog count={count} setAnswer={setAnswer} setCount={setCount}/>
                </Container>
            </ThemeProvider>
        )
    } else {
        return (
            <ThemeProvider theme={theme}>
                <Container className="Home">
                    <p>Peli loppu :)</p>
                </Container>
            </ThemeProvider>
        )
    }
}

export default GamePage