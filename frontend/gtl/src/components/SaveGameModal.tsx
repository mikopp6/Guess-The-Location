import * as React from "react"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Dialog from "@mui/material/Dialog"
import Box from "@mui/material/Box"
import Stack from "@mui/material/Stack"
import DialogActions from "@mui/material/DialogActions"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"
import makeStyles from "@mui/styles/makeStyles"

const useStyles = makeStyles(theme => ({
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
}))

const SaveGameModal: React.FC = () => {
    const classes = useStyles()
    return (
        <Dialog fullWidth className={classes.MuiDialog} open={true}>
            <DialogTitle className={classes.dialogTitle}>Your score: <br /> 1123/1500
            </DialogTitle>
            <Box component="form">
                <DialogContent className={classes.stack}>
                    <Stack alignItems="center">
                        <TextField
                            id="playername"
                            label="Initials"
                            type="text"
                            name="answer"
                            // value={inputValue}
                            // onChange={handleUserInput}
                            variant="standard"
                            inputProps={{ maxLength: 255 }}
                            // error={errors}
                            // helperText={errors ? "Empty field!" : " "}
                            // errorText= {this.state.errorText}
                        />
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button type="submit">Submit</Button>
                    <div style={{flex: "1 0 0"}} />
                    <Button>Dont submit</Button>
                </DialogActions>
            </Box>
        </Dialog>
    )
}
export default SaveGameModal