import React from "react"
import Button from "@mui/material/Button"
import makeStyles from "@mui/styles/makeStyles"
import Modal from "@mui/material/Modal"
import Backdrop from "@mui/material/Backdrop"
import Fade from "@mui/material/Fade"

import ScoreTable from "./highScoreTable"
import ModifiableLocationTable from "./ModifiableLocationTable"

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
const LocationModal: React.FC<{modifiable: boolean}>= ({modifiable}) => {
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
            {modifiable && 
                <Button variant="outlined" size="large" onClick={handleOpen}>
                    Modify Locations
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
                            ? <ModifiableLocationTable />
                            : <ScoreTable />
                        }
                    </div>
                </Fade>
            </Modal>
        </>
    )
}
export default LocationModal