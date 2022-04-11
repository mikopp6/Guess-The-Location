import React, { useState, useEffect } from "react"
import LocationList from '../components/LocationList'
import LocationService from "../services/LocationService"
import ILocation from '../types/Location'
import { ThemeProvider } from '@material-ui/core/styles';
import theme from '../theme';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  image: {
    position: 'fixed',
    top: 0,
    width: '100%',
    height: '100%',
    backgroundSize: 'cover'
  }
}));

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
      <div className="Home">
        {fetchIsDone && <LocationList locations={location}/>}
      </div>
    </ThemeProvider>
)
}

export default GamePage