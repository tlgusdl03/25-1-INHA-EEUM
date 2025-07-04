import { Routes, Route } from "react-router";
import DetailPage from "./pages/DetailPage";
import ListPage from "./pages/ListPage";
import "./App.css";
function App() {
  return (
    <Routes>
      <Route element={<ListPage />} path="/" />
      <Route element={<DetailPage />} path="/:location_id" />
    </Routes>
  );
}

export default App;
