import React, { useEffect, useState } from "react"
import Button from "@material-ui/core/Button"
import TextField from "@material-ui/core/TextField"
import Box from "@material-ui/core/Box"

import IPerson from "../types/Person"
import PersonService from "../services/PersonService"
import { useNavigate } from "react-router-dom"
import { AxiosResponse } from "axios"

/**
 * AddLocationCard
 *
 * 
 * 
 */


const AddLocationCard: React.FC = () => {
    const [persons, setPersons] = useState<Array<IPerson>>([])
    const [fetchIsDone, setFetchIsDone] = useState(false)

    const navigate = useNavigate()

    useEffect(() => {
        retrievePersons()
    }, [])
  
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const email = data.get("email")
        const password = data.get("password")
        console.log("Submitted: ", email, password)
        for(const key in persons){
            const person = persons[key]
            if (person.email === email && person.password === password){
                if (fetchIsDone){
                    navigate("/admin")
                }
            }
        }
    }

    const retrievePersons = () => {
        PersonService.getAll()
            .then((response: AxiosResponse) => {
                setPersons(response.data.items)
                setFetchIsDone(true)
            })
            .catch((e: Error) => {
                console.log(e)
            })
    }
    return (
        <Box component="form" onSubmit={handleSubmit} >
            <TextField 
                type="file"
                name="image"
            />
            <TextField
                margin="normal"
                required
                fullWidth
                name="Country"
                label="Country"
                type="Country"
                id="Country"
            />
            <TextField
                margin="normal"
                required
                fullWidth
                id="Town"
                label="Town"
                name="Town"
            />
            <Button type="submit" variant="outlined" >
                Submit
            </Button>
        </Box>
    )
}
export default AddLocationCard