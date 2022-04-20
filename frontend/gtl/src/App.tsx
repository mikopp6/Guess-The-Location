import "./css/App.css"
import React from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import HomePage from "./pages/Home"
import GamePage from "./pages/Game"
import AdminPage from "./pages/Admin"
import theme from "./theme"
import { ThemeProvider, Theme, StyledEngineProvider } from "@mui/material/styles"


declare module "@mui/styles/defaultTheme" {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface DefaultTheme extends Theme {}
}


const App: React.FC = () => {
    return (
        <StyledEngineProvider injectFirst>
            <ThemeProvider theme={theme}>
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<HomePage/>}/>
                        <Route path="/game" element={<GamePage/>}/>
                        <Route path="/admin" element={<AdminPage/>}/>
                    </Routes>
                </BrowserRouter>
            </ThemeProvider>
        </StyledEngineProvider>
    )
}

export default App