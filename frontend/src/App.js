import { BrowserRouter, Routes, Route } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.min.css";

import "./App.css";
import ProductMaster from "./components/ProductMaster";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ProductMaster />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;