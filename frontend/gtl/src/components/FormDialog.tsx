import * as React from "react"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Dialog from "@mui/material/Dialog"
import Box from "@mui/material/Box"
import DialogActions from "@mui/material/DialogActions"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"
import ILocation from "../types/Location"
import { Dispatch, SetStateAction } from "react"

interface Props {
    correct: number
    setCount: Dispatch<SetStateAction<number>>
    setCorrect: Dispatch<SetStateAction<number>>
    count: number
    locations: Array<ILocation>
}
const FormDialog: React.FC<Props> = ({setCount, count, locations, correct, setCorrect}) => {
    const [errors, setErrors] = React.useState(false)
    const [inputValue, setInputValue] = React.useState("")
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const answer: string = data.get("answer") as string
        setInputValue("")
        if (answer === "") {
            setErrors(true)
        } else {
            if (answer.toUpperCase() === locations?.[count]?.country_name.toUpperCase() || answer.toUpperCase() === locations?.[count]?.town_name.toUpperCase()) {
                setCorrect(correct + 1)
            }
            setErrors(false)
            setCount(count + 1)
        }
    }
    const handleUserInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value)
    }
    const handleGiveUp = () => {
        setCount(count + 1)
        setErrors(false)
    }
    return (
        <Dialog fullWidth open={true}>
            <DialogTitle>Where is this from?</DialogTitle>
            <Box component="form" onSubmit={handleSubmit} >
                <DialogContent>
                    <TextField
                        id="answer"
                        label="City, country, or both"
                        type="text"
                        name="answer"
                        value={inputValue}
                        onChange={handleUserInput}
                        variant="standard"
                        fullWidth
                        inputProps={{ maxLength: 255 }}
                        error={errors}
                        helperText={errors ? "Empty field!" : " "}
                        // errorText= {this.state.errorText}
                    />
                </DialogContent>
                <DialogActions>
                    <Button type="submit">Submit</Button>
                    <div style={{flex: "1 0 0"}} />
                    <Button onClick={handleGiveUp}>Give up</Button>
                </DialogActions>
            </Box>
        </Dialog>
    )
}
export default FormDialog