import React, { useState } from "react"
import {Button, Grid, Container} from "@mui/material" //importing material ui component
import { ThemeProvider, Theme, StyledEngineProvider } from "@mui/material/styles"
import HighScoreModal from "../components/highScoreModal"
import LogInModal from "../components/LogInModal"
import theme from "../theme"
import { useNavigate } from "react-router-dom"


declare module "@mui/styles/defaultTheme" {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface DefaultTheme extends Theme {}
}


// export interface IHomePageProps {}



const HomePage: React.FC = () => {
    const [showLoginModal, setShowLoginModal] = useState(false)

    const logKey = (e: any) => {
        if (e.keyCode === 76 && e.altKey) {
            setShowLoginModal(true)
        }
    }
    document.addEventListener("keydown", logKey)
    const navigate = useNavigate()
    return (
        <Container className="App">
            <Grid>
                <Button onClick={() => navigate("/game")} variant="outlined" size="large">
        New game
                </Button>
                {showLoginModal &&
        <LogInModal />
                }
                <HighScoreModal modifiable={false}/>
            </Grid>
        </Container>
    )
}

export default HomePage