import * as React from "react"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Dialog from "@mui/material/Dialog"
import Box from "@mui/material/Box"
import DialogActions from "@mui/material/DialogActions"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"

interface Props {
    setAnswer: any
    setCount: any
    count: number
}
const FormDialog: React.FC<Props> = ({setAnswer, setCount, count}) => {
    const [errors, setErrors] = React.useState<{ answer: string }>()
    // const [answer, setAnswer] = React.useState<string>()
    let answer: any
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        answer = data.get("answer")
        setAnswer(answer)
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
                        value={answer}
                        variant="standard"
                        fullWidth
                        inputProps={{ maxLength: 255 }}
                        error={Boolean(errors?.answer)}
                        helperText={(errors?.answer)}
                        // errorText= {this.state.errorText}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setCount(count + 1)} type="submit">Submit</Button>
                    <div style={{flex: "1 0 0"}} />
                    <Button >Give up</Button>
                </DialogActions>
            </Box>
        </Dialog>
    )
}
export default FormDialog