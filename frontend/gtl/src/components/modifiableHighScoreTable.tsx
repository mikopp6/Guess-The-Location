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
import TextField from "@mui/material/TextField"
import { AxiosResponse } from "axios"

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

const ModifiableScoreTable: React.FC = () => {
    useEffect(() => {
        retrieveGames()
    }, [])
    const [games, setGames] = useState<Array<IGame>>([])
    const [listItems, setListItems] = useState(10)
    
    const retrieveGames = () => {
        GameService.getAll()
            .then((response: AxiosResponse) => {
                setGames(response.data.items)
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleDelete = (row: any) => {
        console.log(row)
        GameService.remove(row["@controls"].self.href)
            .then(() => {
                retrieveGames()
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleModify = (row: any) => {
        console.log(row)
        GameService.update(row["@controls"].self.href, row.player_name, row.score, row.timestamp, row.game_type)
            .then(() => {
                retrieveGames()
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }
    const classes = useStyles()

    let nextButton
    let noButton
    if (games.length > listItems) {
        nextButton = <Button className={classes.nextButton} variant="text" onClick={() => setListItems(listItems + 10)}>Next<NavigateNextIcon/></Button>
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
                            <TableCell>Score</TableCell>
                            <TableCell></TableCell>
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {games.slice(listItems - 10, listItems).map((row) => (
                            <TableRow key={row.player_name + Math.random()}>
                                <TableCell component="th" scope="row" width={50} >
                                    <TextField
                                        hiddenLabel
                                        id="player_name"
                                        defaultValue={row.player_name}
                                        variant="filled"
                                        size="small"
                                        onChange={(event) => row.player_name = event.target.value}
                                        inputProps={{ maxLength: 3 }}
                                    />
                                </TableCell>
                                <TableCell align="center" width={70} >
                                    <TextField
                                        hiddenLabel
                                        id="score"
                                        defaultValue={row.score}
                                        variant="filled"
                                        size="small"
                                        onChange={(event) => row.score = Number(event.target.value)}
                                        inputProps={{ maxLength: 5 }}
                                    />
                                </TableCell>
                                <TableCell align="right">
                                    <Button variant="text" onClick={() => handleDelete(row)}>DELETE</Button>
                                </TableCell>
                                <TableCell align="right">
                                    <Button type="submit" variant="text" onClick={() => handleModify(row)}>MODIFY</Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            {nextButton ? nextButton : noButton}
        </>
    )
}
export default ModifiableScoreTable