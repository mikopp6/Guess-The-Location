import React, { useEffect, useState } from "react"
import Button from "@material-ui/core/Button"
import Table from "@material-ui/core/Table"
import TableBody from "@material-ui/core/TableBody"
import TableCell from "@material-ui/core/TableCell"
import TableContainer from "@material-ui/core/TableContainer"
import TableHead from "@material-ui/core/TableHead"
import TableRow from "@material-ui/core/TableRow"
import makeStyles from "@material-ui/core/styles/makeStyles"
import NavigateNextIcon from "@material-ui/icons/NavigateNext"
import NavigateBeforeIcon from "@material-ui/icons/NavigateBefore"
import TextField from "@material-ui/core/TextField"
import { AxiosResponse } from "axios"

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
    
    const retrieveLocations = () => {
        LocationService.getAll()
            .then((response: AxiosResponse) => {
                setLocations(response.data.items)
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleDelete = (row: any) => {
        console.log(row)
        LocationService.remove(row["@controls"].self.href)
            .then(() => {
                retrieveLocations()
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleModify = (row: any) => {
        console.log(row)
        LocationService.update(row["@controls"].self.href, row.image_path, row.country_name, row.town_name, row.person_id)
            .then(() => {
                retrieveLocations()
            })
            .catch((e: Error) => {
                console.log(e)
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
                            <TableCell>Country</TableCell>
                            <TableCell>Town</TableCell>
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
        </>
    )
}
export default ModifiableLocationTable