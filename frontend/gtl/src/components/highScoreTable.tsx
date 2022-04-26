import React, { useEffect, useState } from "react"
import Button from "@mui/material/Button"
import Table from "@mui/material/Table"
import TableBody from "@mui/material/TableBody"
import TableCell from "@mui/material/TableCell"
import TableContainer from "@mui/material/TableContainer"
import TableHead from "@mui/material/TableHead"
import TableRow from "@mui/material/TableRow"
import makeStyles from "@mui/styles/makeStyles"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"
import NavigateBeforeIcon from "@mui/icons-material/NavigateBefore"
import { AxiosResponse } from "axios"
import Alert from "@mui/material/Alert"


import IGame from "../types/Game"
import GameService from "../services/GameService"



const useStyles = makeStyles(() => ({
    table: {
        textTransform: "uppercase",
        minWidth: 300,
        "& thead th" :{
            "fontSize": 20,
            "font-weight": 600,
        }
    },
    nextButton: {
        marginTop: 5,
        fontSize: 16,
    },
    noButton: {
        textAlign: "center",
    }
}))

const ScoreTable: React.FC = () => {
    useEffect(() => {
        retrieveGames()
    }, [])
    const [games, setGames] = useState<Array<IGame>>([])
    const [listItems, setListItems] = useState(10)
    const [errorOpen, setErrorOpen] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    const retrieveGames = () => {
        GameService.getAll()
            .then((response: AxiosResponse) => {
                setGames(response.data.items)
            })
            .catch((e: Error) => {
                setErrorMessage(e.message)
                setErrorOpen(!errorOpen)
            })
    }
    const classes = useStyles()
    let nextButton
    let noButton
    console.log(games.length, listItems)
    if (games.length > listItems) {
        nextButton = <Button className={classes.nextButton} variant="text" onClick={() => setListItems(listItems + 10)}>Next<NavigateNextIcon/></Button>
    } else if (games.length < 10) {
        noButton = ""
    } else if (games.length === 0) {
        noButton = <p className={classes.noButton}>There are no highscores.</p>
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
            {errorOpen && 
                <Alert severity="error" onClose={() => setErrorOpen(false)}>
                    {errorMessage}
                </Alert>}
        </>
    )
}
export default ScoreTable