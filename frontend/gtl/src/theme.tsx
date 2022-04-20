import { createTheme, adaptV4Theme } from "@mui/material/styles"


export const theme = createTheme(adaptV4Theme({
    palette: {
        primary: {
            main: "#f00"
        }
    },
    typography: {
        "fontFamily": "\"Roboto\", \"Helvetica\", \"Arial\", sans-serif",
        "fontSize": 14,
        "fontWeightLight": 300,
        "fontWeightRegular": 400,
        "fontWeightMedium": 500
    },
    overrides: {
        MuiButton: {
            outlinedSizeLarge: {
                fontSize: 28,
                fontWeight: 500,
                lineHeight: "unset",
                maxWidth: 200,
                maxHeight: 100,
                marginRight: 20,
                marginLeft: 20,
                borderRadius: 10,
                borderWidth: 8,
                borderColor: "#000"
            }
        },
        MuiContainer: {
            root: {
                width: "100%",
                display: "flex"
            },
        },
        MuiDialog: {
            paper: {
                backgroundColor: "#d7d7d7ba",
            },
            paperWidthSm: {
                maxWidth: 438,
            },
            container: {
                height: "unset",
            },
        },
        MuiBackdrop: {
            root: {
                backgroundColor: "unset"
            }
        },
    }
}))

export default theme