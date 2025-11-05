import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
// @ts-ignore
import SimpleReactFlow from "../pages/simpleReactFlow";
import App from "../App";
import SimpleReactFlow2 from "../pages/simpleReactFlow2";
import MuiReactFlow from "../pages/muiReactFlow";

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/simple" element={<SimpleReactFlow />} />
        <Route path="/simple2" element={<SimpleReactFlow2 />} />
        <Route path="/mui" element={<MuiReactFlow />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
