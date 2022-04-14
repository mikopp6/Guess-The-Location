import "./css/App.css"
import React from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import HomePage from "./pages/Home"
import GamePage from "./pages/Game"
import AdminPage from "./pages/Admin"


const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/game" element={<GamePage/>}/>
                <Route path="/admin" element={<AdminPage/>}/>
            </Routes>
        </BrowserRouter>
    )
}

export default App