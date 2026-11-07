import { useEffect, useState } from "react";
import api from "../api/client";
const fmt = d => new Date(d).toLocaleString([], {dateStyle:"medium",timeStyle:"short"});
export default function HistoryPage() {
  const [items,setItems]=useState([]); const [slots,setSlots]=useState([]); const [error,setError]=useState("");
  async function load(){try{const [b,s]=await Promise.all([api.get("/bookings/mine"),api.get("/slots?available_only=true")]);setItems(b.data);setSlots(s.data);}catch{setError("Unable to load booking history.");}}
  useEffect(()=>{load();},[]);
  async function cancel(id){if(!confirm("Cancel this appointment?"))return;try{await api.patch(`/bookings/${id}/cancel`);load();}catch(e){setError(e.response?.data?.detail||"Cancellation failed");}}
  async function reschedule(id){const choice=prompt("Enter the ID of the new available slot:\n"+slots.map(s=>`${s.id}: ${s.service_name} — ${fmt(s.starts_at)}`).join("\n"));if(!choice)return;try{await api.patch(`/bookings/${id}/reschedule`,{slot_id:Number(choice)});load();}catch(e){setError(e.response?.data?.detail||"Reschedule failed");}}
  return <><div className="page-heading"><p className="eyebrow">YOUR ACTIVITY</p><h1>My bookings</h1><p className="muted">Review, reschedule or cancel your appointments.</p></div>
    {error&&<p className="error" role="alert">{error}</p>}
    <div className="history-list">{items.map(b=><article className="history-card" key={b.id}><div><span className={b.status==="confirmed"?"pill":"pill cancelled"}>{b.status}</span><h3>{b.slot.service_name}</h3><p>{fmt(b.slot.starts_at)} · {b.slot.location}</p>{b.notes&&<small>{b.notes}</small>}</div>
      {b.status==="confirmed"&&<div className="actions"><button className="secondary" onClick={()=>reschedule(b.id)}>Reschedule</button><button className="danger" onClick={()=>cancel(b.id)}>Cancel</button></div>}</article>)}</div>
    {items.length===0&&!error&&<div className="empty">You have not booked any appointments yet.</div>}
  </>;
}
