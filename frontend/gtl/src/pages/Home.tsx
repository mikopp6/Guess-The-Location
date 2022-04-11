import React from 'react';
import {Button, Grid, Container} from '@material-ui/core'; //importing material ui component
import { ThemeProvider } from '@material-ui/core/styles';
import HighScoreModal from '../components/highScoreModal'
import theme from '../theme';
import { useNavigate } from 'react-router-dom';

// export interface IHomePageProps {}

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  return (
    <ThemeProvider theme={theme}>
     <Container className="App">
        <Grid>
          <Button onClick={() => navigate('/game')} variant="outlined" size="large">
            New game
          </Button>
          <HighScoreModal />
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default HomePage;