import React, { useState } from "react"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Dialog from "@mui/material/Dialog"
import Box from "@mui/material/Box"
import Stack from "@mui/material/Stack"
import DialogActions from "@mui/material/DialogActions"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"
import makeStyles from "@mui/styles/makeStyles"
import { useNavigate } from "react-router-dom"
import GameService from "../services/GameService"
import Alert from "@mui/material/Alert"
import moment from "moment"

const useStyles = makeStyles({
    dialogTitle: {
        textAlign: "center",
        paddingBottom: 0
    },
    stack: {
        paddingTop: 5,
    },
    MuiDialog: {
        "& .MuiDialog-container": {
            height: "100%"
        },
        "& .MuiPaper-root": {
            maxWidth: 330,
        }
    },
})

interface Props {
    correct: number
}

const SaveGameModal: React.FC<Props> = ({correct}) => {
    const [errors, setErrors] = useState(false)
    const [errorOpen, setErrorOpen] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")
    const maxPoints = 5000 * 3
    const classes = useStyles()
    const navigate = useNavigate()
    const userCorrect = (correct * 1000) * 3
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const answer: string = data.get("answer") as string
        if (answer.length < 3) {
            setErrors(true)
        } else {
            const today = new Date()
            const formattedDate = (moment(today)).format("YYYY-MM-DDTHH:mm:ss.SSS")
            GameService.create(answer.toUpperCase(), userCorrect, formattedDate, 1)
                .then(() => { 
                    navigate("/")
                })
                .catch((e: Error) => {
                    setErrorMessage(e.message)
                    setErrorOpen(!errorOpen)
                })
        }
    }

    return (
        <Dialog fullWidth className={classes.MuiDialog} open={true}>
            {errorOpen && 
                <Alert severity="error" onClose={() => setErrorOpen(false)}>
                    {errorMessage}
                </Alert>}
            <DialogTitle className={classes.dialogTitle}>Your score: <br /> {userCorrect} / {maxPoints}
            </DialogTitle>
            <Box component="form" onSubmit={handleSubmit} >
                <DialogContent className={classes.stack}>
                    <Stack alignItems="center">
                        <TextField
                            id="playername"
                            label="Initials"
                            type="text"
                            name="answer"
                            variant="standard"
                            inputProps={{ maxLength: 3 }}
                            error={errors}
                            helperText={errors ? "Minimum 3 characters!" : " "}
                        />
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button type="submit">Submit</Button>
                    <div style={{flex: "1 0 0"}} />
                    <Button onClick={() => navigate("/")}>Dont submit</Button>
                </DialogActions>
            </Box>
        </Dialog>
    )
}
export default SaveGameModal