import React from "react";
import "./App.css";
import "./css/main.css";
import Hitas from "./pages/hitas";
import Home from "./pages/home";
import Gregorian from "./pages/greg_to_heb";
import Hebrew from "./pages/heb_to_greg";
import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/chumash" element={<Hitas title="chumash/" />} />
      <Route path="/tehillim" element={<Hitas title="tehillim/" />} />
      <Route path="/tanya" element={<Hitas title="tanya/" />} />
      <Route path="/hayom_yoma" element={<Hitas title="hayom_yoma/" />} />
      <Route path="/rambam" element={<Hitas title="rambam/" />} />
      <Route path="/moshiach" element={<Hitas title="moshiach/" />} />
      <Route path="/greg-to-heb" element={<Gregorian />} />
      <Route path="/heb-to-greg" element={<Hebrew />} />
      <Route path="/" element={<Home />} />
      {/* <Route path="*" element={<NotFound />} /> */}
    </Routes>
  );
}

export default App;
