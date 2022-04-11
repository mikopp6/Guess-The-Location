import { createTheme } from "@material-ui/core/styles"


export const theme = createTheme({
    palette: {
        primary: {
            main: "#f00"
        }
    },
    typography: {
        "fontFamily": `"Roboto", "Helvetica", "Arial", sans-serif`,
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
                lineHeight: 'unset',
                maxWidth: 200,
                maxHeight: 100,
                marginRight: 20,
                marginLeft: 20,
                borderRadius: 10,
                borderWidth: 8,
                borderColor: '#000'
            }
        },
        MuiContainer: {
            root: {
                width: '100%',
                display: 'flex'
            },
        },
    }
})

export default theme;