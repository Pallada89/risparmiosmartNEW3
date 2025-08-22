import { useEffect, useState } from "react";

const API = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export default function App() {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/offers`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setOffers(data.offers || []);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <main style={{fontFamily:"system-ui, sans-serif", padding:16, maxWidth:900, margin:"0 auto"}}>
      <h1>RisparmioSmart: Offerte automatiche</h1>
      <p style={{opacity:.8}}>Pipeline (crawler → OCR → AI) con output in <code>offers.json</code>.</p>

      <div style={{margin:"12px 0"}}>
        <button onClick={load} disabled={loading}>
          {loading ? "Aggiorno…" : "Aggiorna offerte"}
        </button>
        {!process.env.REACT_APP_API_BASE && (
          <span style={{marginLeft:12, color:"crimson"}}>
            ⚠️ REACT_APP_API_BASE non configurata: uso {API}
          </span>
        )}
      </div>

      {error && <div style={{color:"crimson"}}>Errore: {error}</div>}

      {offers.length === 0 && !loading && (
        <div>Nessuna offerta trovata. Esegui <code>crawler.py</code> e poi <code>ocr_ai.py</code> nel backend.</div>
      )}

      <ul>
        {offers.map((o, i) => (
          <li key={i} style={{padding:"8px 0", borderBottom:"1px solid #eee"}}>
            <strong>{o.product}</strong>{" "}
            <span style={{opacity:.8}}>{o.quantity}</span>{" "}
            — <span>{o.price} €</span>
            {o.file ? <span style={{opacity:.6}}> (src: {o.file})</span> : null}
          </li>
        ))}
      </ul>
    </main>
  );
}
