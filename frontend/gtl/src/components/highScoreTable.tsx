import React, { useEffect, useState } from 'react';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import GameService from "../services/GameService";
import { makeStyles } from '@material-ui/core/styles';
import IGame from '../types/Game';
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';

const useStyles = makeStyles(theme => ({
    table: {
        textTransform: 'uppercase',
        minWidth: 300,
        '& thead th' :{
            "fontSize": 20,
            "font-weight": 600,
        }
    },
    nextButton: {
        marginTop: 5,
        fontSize: 16,
    },
    noButton: {
        textAlign: 'center',
    }
}));

const ScoreTable: React.FC = () => {
useEffect(() => {
    retrievelocations();
}, []);
const [games, setGames] = useState<Array<IGame>>([]);
const [listItems, setListItems] = useState(10)
const retrievelocations = () => {
    GameService.getAll()
        .then((response: any) => {
        setGames(response.data.items);
        })
        .catch((e: Error) => {
        console.log(e);
        });
};
const classes = useStyles();
let nextButton;
let noButton;
if (games.length > listItems) {
    nextButton = <Button className={classes.nextButton} variant="text" onClick={() => setListItems(listItems + 10)}>Next<NavigateNextIcon/></Button>
} else if (games.length === 0) {
    noButton = <p className={classes.noButton}>There are no any highscores.</p>
} else {
    nextButton = <Button className={classes.nextButton} variant="text" onClick={() => setListItems(listItems - 10)}><NavigateBeforeIcon/>Back</Button>
}
  return (
      <>
    <TableContainer>
      <Table className={classes.table} size="medium" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="right">Score</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {games.slice(listItems - 10, listItems).map((row) => (
            <TableRow key={row.player_name + Math.random()}>
              <TableCell component="th" scope="row">
                {row.player_name}
              </TableCell>
              <TableCell align="right">{row.score}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    {nextButton ? nextButton : noButton}
    </>
  );
}
export default ScoreTable;