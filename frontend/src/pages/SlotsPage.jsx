import { useEffect, useState } from "react";
import { CalendarClock, MapPin } from "lucide-react";
import api from "../api/client";

function pretty(date) { return new Date(date).toLocaleString([], { dateStyle: "medium", timeStyle: "short" }); }
export default function SlotsPage() {
  const [slots,setSlots]=useState([]); const [error,setError]=useState(""); const [message,setMessage]=useState("");
  async function load() { try { const {data}=await api.get("/slots"); setSlots(data); } catch { setError("Could not load appointments. Check that the API is running."); } }
  useEffect(()=>{load();},[]);
  async function book(slotId) { setError(""); setMessage(""); try { await api.post("/bookings",{slot_id:slotId}); setMessage("Appointment booked successfully."); await load(); } catch(e) { setError(e.response?.data?.detail || "Booking failed."); } }
  return <><section className="hero"><div><p className="eyebrow">CARE THAT FITS YOUR DAY</p><h1>Book your next appointment.</h1><p>Choose a service and a time that works for you.</p></div><div className="hero-icon"><CalendarClock size={54}/></div></section>
    <div className="section-heading"><div><h2>Available appointments</h2><p className="muted">Upcoming appointment slots</p></div><button className="secondary" onClick={load}>Refresh</button></div>
    {message && <p className="success" role="status">{message}</p>}{error && <p className="error" role="alert">{error}</p>}
    <div className="slot-grid">{slots.filter(s=>s.available).map(slot=><article className="slot-card" key={slot.id}>
      <span className="pill">Available</span><h3>{slot.service_name}</h3><p><CalendarClock size={16}/> {pretty(slot.starts_at)}</p><p><MapPin size={16}/> {slot.location}</p>
      <button className="primary full" onClick={()=>book(slot.id)}>Book appointment</button></article>)}</div>
    {slots.filter(s=>s.available).length===0 && !error && <div className="empty">No upcoming slots are available right now. Please check again later.</div>}
  </>;
}
