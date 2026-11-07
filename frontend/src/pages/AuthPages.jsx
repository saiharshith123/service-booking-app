import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function LoginPage() {
  const { login } = useAuth(); const nav = useNavigate();
  const [email, setEmail] = useState(""); const [password, setPassword] = useState(""); const [error, setError] = useState("");
  async function submit(e) { e.preventDefault(); setError(""); try { await login(email, password); nav("/"); } catch (err) { setError(err.response?.data?.detail || "Login failed"); } }
  return <section className="auth-card"><p className="eyebrow">WELCOME BACK</p><h1>Sign in to CarePoint</h1><p className="muted">Manage your appointments in one place.</p>
    <form onSubmit={submit}><label>Email<input type="email" required value={email} onChange={e=>setEmail(e.target.value)} autoComplete="email"/></label>
      <label>Password<input type="password" required value={password} onChange={e=>setPassword(e.target.value)} autoComplete="current-password"/></label>
      {error && <p className="error" role="alert">{error}</p>}<button className="primary full">Sign in</button></form>
    <p className="muted">New here? <Link to="/register">Create an account</Link></p></section>;
}

export function RegisterPage() {
  const { register } = useAuth(); const nav = useNavigate();
  const [name,setName]=useState(""); const [email,setEmail]=useState(""); const [password,setPassword]=useState(""); const [error,setError]=useState("");
  async function submit(e) { e.preventDefault(); setError(""); try { await register(name,email,password); nav("/"); } catch(err) { setError(err.response?.data?.detail || "Registration failed"); } }
  return <section className="auth-card"><p className="eyebrow">GET STARTED</p><h1>Create your account</h1>
    <form onSubmit={submit}><label>Full name<input required minLength="2" value={name} onChange={e=>setName(e.target.value)}/></label>
      <label>Email<input type="email" required value={email} onChange={e=>setEmail(e.target.value)}/></label>
      <label>Password<input type="password" minLength="8" required value={password} onChange={e=>setPassword(e.target.value)}/><small>At least 8 characters.</small></label>
      {error && <p className="error" role="alert">{error}</p>}<button className="primary full">Create account</button></form>
    <p className="muted">Already registered? <Link to="/login">Sign in</Link></p></section>;
}
