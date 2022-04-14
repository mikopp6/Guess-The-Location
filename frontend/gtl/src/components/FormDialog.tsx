import * as React from "react"
import Button from "@material-ui/core/Button"
import TextField from "@material-ui/core/TextField"
import Dialog from "@material-ui/core/Dialog"
import Box from "@material-ui/core/Box"
import DialogActions from "@material-ui/core/DialogActions"
import DialogContent from "@material-ui/core/DialogContent"
import DialogTitle from "@material-ui/core/DialogTitle"

export default function FormDialog() {
    const [errors, setErrors] = React.useState<{ answer: string }>()
    const [answer, setAnswer] = React.useState<string>()

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const answer = data.get("answer")
        console.log("täsä",answer)
    }

    return (
        <Dialog fullWidth open={true}>
            <DialogTitle>Where is this from?</DialogTitle>
            <Box component="form" onSubmit={handleSubmit} >
                <DialogContent>
                    <TextField
                        // margin="dense"
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
                    <Button type="submit">Submit</Button>
                    <div style={{flex: "1 0 0"}} />
                    <Button >Give up</Button>
                </DialogActions>
            </Box>
        </Dialog>
    )
}