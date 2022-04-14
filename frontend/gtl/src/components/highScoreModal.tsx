import React from "react"
import Button from "@material-ui/core/Button"
import { makeStyles } from "@material-ui/core/styles"
import Modal from "@material-ui/core/Modal"
import Backdrop from "@material-ui/core/Backdrop"
import Fade from "@material-ui/core/Fade"
import ScoreTable from "./highScoreTable"
import ModifiableScoreTable from "./modifiableHighScoreTable"
const useStyles = makeStyles(theme => ({
    modal: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
    paper: {
        fontFamily: "Roboto",
        backgroundColor: theme.palette.background.paper,
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 3, 1),
    },
}))
const HighScoreModal: React.FC<{modifiable: boolean}>= ({modifiable}) => {
    const classes = useStyles()
    const [open, setOpen] = React.useState(false)

    const handleOpen = () => {
        setOpen(true)
    }
    const handleClose = () => {
        setOpen(false)
    }
    return (
        <>  
            {modifiable 
                ? <Button variant="outlined" size="large" onClick={handleOpen}>
                Modify Scores
                </Button>
                : <Button variant="outlined" size="large" onClick={handleOpen}>
                High Scores
                </Button>
            }
            <Modal
                aria-labelledby="transition-modal-title"
                aria-describedby="transition-modal-description"
                className={classes.modal}
                open={open}
                onClose={handleClose}
                closeAfterTransition
                BackdropComponent={Backdrop}
                BackdropProps={{
                    timeout: 500,
                }}
            >
                <Fade in={open}>
                    <div className={classes.paper}>
                        {modifiable 
                            ? <ModifiableScoreTable />
                            : <ScoreTable />
                        }
                    </div>
                </Fade>
            </Modal>
        </>
    )
}
export default HighScoreModal