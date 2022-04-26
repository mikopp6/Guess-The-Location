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
import Alert from "@mui/material/Alert"

import ILocation from "../types/Location"
import LocationService from "../services/LocationService"


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

const ModifiableLocationTable: React.FC = () => {
    useEffect(() => {
        retrieveLocations()
    }, [])
    const [locations, setLocations] = useState<Array<ILocation>>([])
    const [listItems, setListItems] = useState(10)
    const [errorOpen, setErrorOpen] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")
    
    const retrieveLocations = () => {
        LocationService.getAll()
            .then((response: AxiosResponse) => {
                setLocations(response.data.items)
            })
            .catch((e: Error) => {
                setErrorMessage(e.message)
                setErrorOpen(!errorOpen)
            })
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleDelete = (row: any) => {
        LocationService.remove(row["@controls"].self.href)
            .then(() => {
                retrieveLocations()
            })
            .catch((e: Error) => {
                setErrorMessage(e.message)
                setErrorOpen(!errorOpen)
            })
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleModify = (row: any) => {
        LocationService.update(row["@controls"].self.href, row.image_path, row.country_name, row.town_name, row.person_id)
            .then(() => {
                retrieveLocations()
            })
            .catch((e: Error) => {
                setErrorMessage(e.message)
                setErrorOpen(!errorOpen)
            })
    }
    const classes = useStyles()

    let nextButton
    let noButton
    if (locations.length > listItems) {
        nextButton = <Button className={classes.nextButton} variant="text" onClick={() => setListItems(listItems + 10)}>Next<NavigateNextIcon/></Button>
    } else if (locations.length === 0) {
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
                            <TableCell>Path</TableCell>
                            <TableCell align="center" >IMG</TableCell>
                            <TableCell>Country</TableCell>
                            <TableCell>Town</TableCell>
                            <TableCell></TableCell>
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {locations.slice(listItems - 10, listItems).map((row) => (
                            <TableRow key={row.image_path + Math.random()}>
                                <TableCell component="th" scope="row" width={250} >
                                    <TextField
                                        hiddenLabel
                                        id="image_path"
                                        defaultValue={row.image_path}
                                        variant="filled"
                                        size="small"
                                        onChange={(event) => row.image_path = event.target.value}
                                    />
                                </TableCell>
                                <TableCell align="center" width={10}>
                                    <Button variant="text" onClick={()=> window.open(("http://localhost:8080/static/images/" + row.image_path))}>view</Button>
                                </TableCell>
                                <TableCell align="center" width={150} >
                                    <TextField
                                        hiddenLabel
                                        id="score"
                                        defaultValue={row.country_name}
                                        variant="filled"
                                        size="small"
                                        onChange={(event) => row.country_name = event.target.value}
                                    />
                                </TableCell>
                                <TableCell align="center" width={150} >
                                    <TextField
                                        hiddenLabel
                                        id="score"
                                        defaultValue={row.town_name}
                                        variant="filled"
                                        size="small"
                                        onChange={(event) => row.town_name = event.target.value}
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
            {errorOpen && 
                <Alert severity="error" onClose={() => setErrorOpen(false)}>
                    {errorMessage}
                </Alert>}
        </>
    )
}
export default ModifiableLocationTable