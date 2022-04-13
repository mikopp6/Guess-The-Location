import React from "react"

import { ThemeProvider } from '@material-ui/core/styles';
import theme from '../theme';
import { Button, Container, Grid } from '@material-ui/core'; //importing material ui component
import { useNavigate } from "react-router-dom";


// export interface IGamePageProps {}
const AdminPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <ThemeProvider theme={theme}>
     <Container className="App">
        <Grid>
          <Button variant="outlined" size="large">
            Add Location
          </Button>
          <Button variant="outlined" size="large">
            Modify Locations
          </Button>
          <Button variant="outlined" size="large">
            Modify Scores
          </Button>
          <Button onClick={() => navigate('/')} variant="outlined" size="large">
            Log out
          </Button>
        </Grid>
      </Container>
    </ThemeProvider>
  )
}

export default AdminPage