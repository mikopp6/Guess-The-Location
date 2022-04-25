import React, { useState, useEffect } from "react"
import { ThemeProvider, Theme, StyledEngineProvider } from "@mui/material/styles"
import { Container } from "@mui/material"
import { AxiosResponse } from "axios"

import theme from "../theme"
import SingleGame from "../components/SingleGame"
import SaveGameModal from "../components/SaveGameModal"
import LocationService from "../services/LocationService"
import ILocation from "../types/Location"



declare module "@mui/styles/defaultTheme" {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface DefaultTheme extends Theme {}
}

// export interface IGamePageProps {}
const GamePage: React.FC = () => {
    const [allLocations, setlocations] = useState<Array<ILocation>>([])
    const [fetchIsDone, setFetchIsDone] = useState(false)
    const [count, setCount] = useState(0)
    // const [answer, setAnswer] = useState()
    const [correct, setCorrect] = useState(0)
  
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
            <Container className="Home">
                {fetchIsDone && <SingleGame 
                    locations={allLocations} 
                    // answer={answer} 
                    count={count} 
                    correct={correct}
                    setCorrect={setCorrect}
                    // setAnswer={setAnswer} 
                    setCount={setCount}/>}
                {/* <FormDialog count={count} setAnswer={setAnswer} setCount={setCount}/> */}
            </Container>
        )
    } else {
        return (
            <Container className="App">
                <ThemeProvider theme={theme}>
                    <Container className="Home">
                        <SaveGameModal/>
                    </Container>
                </ThemeProvider>
            </Container>
        )
    }
}

export default GamePage