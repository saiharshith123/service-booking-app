import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import { LoginPage, RegisterPage } from "./pages/AuthPages";
import SlotsPage from "./pages/SlotsPage";
import HistoryPage from "./pages/HistoryPage";
import AdminPage from "./pages/AdminPage";
import "./styles.css";

function AppRoutes(){return <Routes><Route element={<Layout/>}>
  <Route path="/login" element={<LoginPage/>}/><Route path="/register" element={<RegisterPage/>}/>
  <Route path="/" element={<ProtectedRoute><SlotsPage/></ProtectedRoute>}/>
  <Route path="/history" element={<ProtectedRoute><HistoryPage/></ProtectedRoute>}/>
  <Route path="/admin" element={<ProtectedRoute adminOnly><AdminPage/></ProtectedRoute>}/>
  <Route path="*" element={<Navigate to="/" replace/>}/>
</Route></Routes>}
export default function App(){return <BrowserRouter><AuthProvider><AppRoutes/></AuthProvider></BrowserRouter>}
