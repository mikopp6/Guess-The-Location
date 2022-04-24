import React, { useState, useEffect } from "react"
import FormDialog from "../components/FormDialog"
import ILocation from "../types/Location"
import makeStyles from "@mui/styles/makeStyles"

const useStyles = makeStyles(theme => ({
    image: {
        position: "fixed",
        backgroundSize: "cover",
    }
}))
interface Props {
    locations: Array<ILocation>
    count: number
    correct: number
    setCount: any
    setCorrect: any
}
const SingleGame: React.FC<Props> = ({locations, count, correct, setCorrect, setCount}) => {
    const [answer, setAnswer] = useState("")
    // const [correct, setCorrect] = useState(0)
    const classes = useStyles()

    return (
        <>
            <img className={classes.image} src={"../static/images/" + locations?.[count]?.image_path}
                onError={({ currentTarget }) => {
                    currentTarget.onerror = null // prevents looping
                    currentTarget.src="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
                }} />
            <FormDialog count={count} correct={correct} setCorrect={setCorrect} setAnswer={setAnswer} setCount={setCount} locations={locations}/>
        </>
    )
}
export default SingleGame