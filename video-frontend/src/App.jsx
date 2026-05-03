import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SignIn, SignUp } from "@clerk/clerk-react";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Watch from "./pages/Watch";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/sign-in" element={<SignIn />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/videos/:id" element={<Watch />} />
      </Routes>
    </BrowserRouter>
  );
}