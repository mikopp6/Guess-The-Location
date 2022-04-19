import React from "react"
import Button from "@material-ui/core/Button"
import TextField from "@material-ui/core/TextField"
import Box from "@material-ui/core/Box"


/**
 * AddLocationCard
 *
 * 
 * 
 */


const AddLocationCard: React.FC = () => {
    const handleSubmit = () => {
        console.log("yes")
    }

    return (
        <Box sx={{ width: 300, height: 225 }}>
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
            <Button type="submit" variant="outlined" onClick={() => handleSubmit()}>
                Submit
            </Button>
        </Box>
    )
}
export default AddLocationCard