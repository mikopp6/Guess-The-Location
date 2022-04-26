import React, { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Box from "@mui/material/Box"
import Alert from "@mui/material/Alert"

import { AxiosResponse } from "axios"
import IPerson from "../types/Person"
import PersonService from "../services/PersonService"


/**
 * LogInCard
 *
 * The window inside LogInModal that allows logging in.
 * The actual "login" is just checking if the email and pw
 * match someone that was retrieved from the api.
 * 
 */


const LogInCard: React.FC = () => {
    const [persons, setPersons] = useState<Array<IPerson>>([])
    const [fetchIsDone, setFetchIsDone] = useState(false)
    const [errorOpen, setErrorOpen] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

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
            if (person.email === email && person.password === password) {
                if (fetchIsDone){
                    navigate("/admin")
                }
            } else {
                setErrorMessage("Wrong username or password!")
                setErrorOpen(!errorOpen)
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
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
            />
            <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
            />
            <Button type="submit" variant="outlined" >
                Log In
            </Button>
            {errorOpen && 
                <Alert severity="error" onClose={() => setErrorOpen(false)}>
                    {errorMessage}
                </Alert>}
        </Box>
    )
}
export default LogInCard