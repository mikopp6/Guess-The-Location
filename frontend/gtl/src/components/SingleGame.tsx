import React, { useState, useEffect } from "react"
import ILocation from "../types/Location"
import { makeStyles } from "@material-ui/core/styles"

const useStyles = makeStyles(theme => ({
    image: {
        position: "fixed",
        backgroundSize: "cover",
    }
}))
interface Props {
    locations: Array<ILocation>
    count: number
    answer: string | undefined
}
const SingleGame: React.FC<Props> = ({locations, count, answer}) => {
    const classes = useStyles()
    if (answer) {
        if (answer == locations?.[count - 1]?.country_name) {
            console.log("oikein meni")
        }
    }
    return (
        <img className={classes.image} src={"../static/images/" + locations?.[count]?.image_path}
            onError={({ currentTarget }) => {
                currentTarget.onerror = null // prevents looping
                currentTarget.src="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
            }} />
    )
}
export default SingleGame