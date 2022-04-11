import './css/App.css';
import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/Home';
import GamePage from './pages/Game';


const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/game" element={<GamePage/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;