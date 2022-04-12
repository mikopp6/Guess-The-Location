import React, { useState, useEffect } from "react";
import ILocation from '../types/Location';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  image: {
    position: 'fixed',
    // width: '100%',
    // height: '100%',
    backgroundSize: 'cover',
  }
}));

const LocationList: React.FC<{locations: Array<ILocation>}>= ({locations}) => {
  useEffect(() => {
    setlocations(locations)
    randomlocation(locations)
  }, []);

  const [location, setlocation] = useState<ILocation | null>();
  const [allLocations, setlocations] = useState<Array<ILocation>>();
  const randomlocation = (data: any) => {
      const min = 0;
      const max = data.length - 1;
      const rand = Math.floor(min + Math.random() * (max - min));
      setlocation(data[rand])
  };
  const classes = useStyles();

  // const currentImg = location?.image_path
  return (
      <img className={classes.image} src={'../static/images/' + location?.image_path}
      onError={({ currentTarget }) => {
        currentTarget.onerror = null; // prevents looping
        currentTarget.src="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png";
      }} />
  );

};
export default LocationList;