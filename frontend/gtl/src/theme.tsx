import { createTheme, } from "@mui/material/styles"


export const theme = createTheme({
    palette: {
        primary: {
            main: "#000"
        }
    },
    typography: {
        "fontFamily": "\"Roboto\", \"Helvetica\", \"Arial\", sans-serif",
        "fontSize": 14,
        "fontWeightLight": 300,
        "fontWeightRegular": 400,
        "fontWeightMedium": 500
    },
    components: {
        MuiButton: {
            styleOverrides: {
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
                    borderColor: "#000",
                    "&:hover": {
                        borderRadius: 10,
                        borderWidth: 8,
                        borderColor: "#000"
                    },
                }
            },
        },
        MuiContainer: {
            styleOverrides: {
                root: {
                    width: "100%",
                    display: "flex",
                },
            }
        },
        MuiDialog: {
            styleOverrides: {
                paper: {
                    backgroundColor: "#d7d7d7ba",
                },
                paperWidthSm: {
                    maxWidth: 438,
                },
                container: {
                    height: "unset",
                },
            }
        },
        MuiBackdrop: {
            styleOverrides: {
                root: {
                    backgroundColor: "unset"
                }
            }
        },
    }
})

export default theme