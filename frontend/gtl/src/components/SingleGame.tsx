import React from "react"
import FormDialog from "../components/FormDialog"
import ILocation from "../types/Location"
import makeStyles from "@mui/styles/makeStyles"
import { Dispatch, SetStateAction } from "react"

const useStyles = makeStyles({
    image: {
        position: "fixed",
        backgroundSize: "cover",
    }
})
interface Props {
    locations: Array<ILocation>
    count: number
    correct: number
    setCount: Dispatch<SetStateAction<number>>
    setCorrect: Dispatch<SetStateAction<number>>
}
const SingleGame: React.FC<Props> = ({locations, count, correct, setCorrect, setCount}) => {
    const classes = useStyles()
    return (
        <>
            <img className={classes.image} src={"../static/images/" + locations?.[count]?.image_path}
                onError={({ currentTarget }) => {
                    currentTarget.onerror = null // prevents looping
                    currentTarget.src="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png"
                }} />
            <FormDialog count={count} correct={correct} setCorrect={setCorrect} setCount={setCount} locations={locations}/>
        </>
    )
}
export default SingleGame