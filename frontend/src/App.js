import { BrowserRouter, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import Home from "./components/Home";
import Navigation from "./components/Navigation";
import ProductMaster from "./components/ProductMaster";
import Customers from "./components/Customers";
import Sales from "./components/Sales";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<ProductMaster />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/sales" element={<Sales />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;