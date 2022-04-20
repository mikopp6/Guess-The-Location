import React from "react"
import makeStyles from "@mui/styles/makeStyles"
import Modal from "@mui/material/Modal"
import Backdrop from "@mui/material/Backdrop"
import Fade from "@mui/material/Fade"
import LogInCard from "./LogInCard"

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

const AddLocation: React.FC = () => {
    const classes = useStyles()
    const [open, setOpen] = React.useState(true)
    const handleClose = () => {
        setOpen(false)
    }
    return (
        <>
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
                }}>
                <Fade in={open}>
                    <div className={classes.paper}>
                        <LogInCard />
                    </div>
                </Fade>
            </Modal>
        </>
    )
}
export default AddLocation