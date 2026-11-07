import { useEffect, useState } from "react";
import api from "../api/client";
const localInput = d => { const date=new Date(d); return new Date(date.getTime()-date.getTimezoneOffset()*60000).toISOString().slice(0,16); };
export default function AdminPage(){
  const [slots,setSlots]=useState([]); const [bookings,setBookings]=useState([]); const [service,setService]=useState("General consultation"); const [start,setStart]=useState(""); const [end,setEnd]=useState(""); const [location,setLocation]=useState("Main branch"); const [error,setError]=useState(""); const [message,setMessage]=useState("");
  async function load(){try{const [s,b]=await Promise.all([api.get("/slots"),api.get("/bookings")]);setSlots(s.data);setBookings(b.data);}catch(e){setError(e.response?.data?.detail||"Admin data could not be loaded");}}
  useEffect(()=>{load();},[]);
  async function addSlot(e){e.preventDefault();setError("");setMessage("");try{await api.post("/slots",{service_name:service,starts_at:new Date(start).toISOString(),ends_at:new Date(end).toISOString(),location});setMessage("Slot created.");setStart("");setEnd("");load();}catch(e){setError(e.response?.data?.detail||"Could not create slot");}}
  async function cancel(id){try{await api.patch(`/bookings/${id}/cancel`);load();}catch(e){setError(e.response?.data?.detail||"Could not cancel booking");}}
  async function deactivate(id){try{await api.patch(`/slots/${id}/deactivate`);load();}catch(e){setError(e.response?.data?.detail||"Could not deactivate slot");}}
  return <><div className="page-heading"><p className="eyebrow">ADMINISTRATION</p><h1>Admin dashboard</h1><p className="muted">Create appointment slots and manage bookings.</p></div>
    {error&&<p className="error" role="alert">{error}</p>}{message&&<p className="success" role="status">{message}</p>}
    <section className="panel"><h2>Create an appointment slot</h2><form className="slot-form" onSubmit={addSlot}>
      <label>Service name<input required value={service} onChange={e=>setService(e.target.value)}/></label>
      <label>Start date/time<input type="datetime-local" required value={start} onChange={e=>setStart(e.target.value)}/></label>
      <label>End date/time<input type="datetime-local" required value={end} onChange={e=>setEnd(e.target.value)}/></label>
      <label>Location<input required value={location} onChange={e=>setLocation(e.target.value)}/></label>
      <button className="primary">Create slot</button></form></section>
    <section className="panel"><h2>Appointment slots</h2><div className="table-wrap"><table><thead><tr><th>Service</th><th>Starts</th><th>Availability</th><th>Action</th></tr></thead><tbody>{slots.map(s=><tr key={s.id}><td>{s.service_name}</td><td>{new Date(s.starts_at).toLocaleString()}</td><td>{s.available?"Available":"Booked"}</td><td>{s.is_active&&<button className="danger" onClick={()=>deactivate(s.id)}>Deactivate</button>}</td></tr>)}</tbody></table></div></section>
    <section className="panel"><h2>All bookings</h2><div className="table-wrap"><table><thead><tr><th>Customer</th><th>Service</th><th>Time</th><th>Status</th><th>Action</th></tr></thead><tbody>{bookings.map(b=><tr key={b.id}><td>{b.customer?.name||`User ${b.customer_id}`}</td><td>{b.slot.service_name}</td><td>{new Date(b.slot.starts_at).toLocaleString()}</td><td>{b.status}</td><td>{b.status==="confirmed"&&<button className="danger" onClick={()=>cancel(b.id)}>Cancel</button>}</td></tr>)}</tbody></table></div></section>
  </>;
}
