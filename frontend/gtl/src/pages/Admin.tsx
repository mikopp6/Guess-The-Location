import React from "react"
import { ThemeProvider, Theme, StyledEngineProvider } from "@mui/material/styles"
import { Button, Container, Grid } from "@mui/material" //importing material ui component
import { useNavigate } from "react-router-dom"

import theme from "../theme"
import HighScoreModal from "../components/highScoreModal"
import LocationModal from "../components/locationModal"
import AddLocationModal from "../components/AddLocationModal"



declare module "@mui/styles/defaultTheme" {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface DefaultTheme extends Theme {}
}



// export interface IAdminPageProps {}
const AdminPage: React.FC = () => {
    const navigate = useNavigate()

    return (
        <Container className="App">
            <Grid>
                <AddLocationModal />
                <LocationModal modifiable={true}/>
                <HighScoreModal modifiable={true}/>
                <Button onClick={() => navigate("/")} variant="outlined" size="large">
                    Log out
                </Button>
            </Grid>
        </Container>
    )
}

export default AdminPage