import { Link, NavLink, Outlet } from "react-router-dom";
import { CalendarDays, LogOut, ShieldCheck } from "lucide-react";
import { useAuth } from "../context/AuthContext";
export default function Layout() {
  const { user, logout } = useAuth();
  return <div className="app-shell">
    <header className="topbar"><Link className="brand" to="/"><CalendarDays /> CarePoint</Link>
      <nav aria-label="Main navigation">
        {user ? <><NavLink to="/">Available slots</NavLink><NavLink to="/history">My bookings</NavLink>{user.role === "admin" && <NavLink to="/admin"><ShieldCheck size={16}/> Admin</NavLink>}
          <span className="user-name">{user.name}</span><button className="link-button" onClick={logout}><LogOut size={16}/> Logout</button></> :
          <><NavLink to="/login">Login</NavLink><NavLink className="nav-cta" to="/register">Create account</NavLink></>}
      </nav>
    </header>
    <main className="container"><Outlet /></main>
    <footer>CarePoint · Simple, secure appointment booking</footer>
  </div>;
}
