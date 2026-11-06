import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../services/auth';
import { Alert, DealerImage, Spinner } from './common';

/** Dealer grid with a state filter. `state` comes from the URL (/dealers/:state). */
export default function DealerList({ state = 'All', basePath = '/dealers' }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [allStates, setAllStates] = useState([]);
  const [dealers, setDealers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');

  // Load the full list once for the state dropdown.
  useEffect(() => {
    api.dealers().then((d) => setAllStates([...new Set(d.dealers.map((x) => x.state))].sort())).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    setError('');
    api.dealers(state)
      .then((d) => setDealers(d.dealers))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [state]);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return dealers;
    return dealers.filter((d) => `${d.full_name} ${d.city} ${d.zip}`.toLowerCase().includes(q));
  }, [dealers, query]);

  function onStateChange(e) {
    const value = e.target.value;
    navigate(value === 'All' ? basePath : `/dealers/${encodeURIComponent(value)}`);
  }

  return (
    <section className="dealers">
      <div className="toolbar">
        <div>
          <h2 className="section-title">
            {state === 'All' ? 'All dealerships' : `Dealerships in ${state}`}
          </h2>
          <p className="muted">{loading ? 'Loading…' : `${visible.length} dealership${visible.length === 1 ? '' : 's'} found`}</p>
        </div>
        <div className="filters">
          <input
            className="input"
            type="search"
            placeholder="Search name, city or ZIP"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Search dealers"
          />
          <select className="input" value={state} onChange={onStateChange} aria-label="Filter by state">
            <option value="All">All states</option>
            {allStates.map((s) => <option key={s} value={s}>{s}</option>)}
            {state !== 'All' && !allStates.includes(state) && <option value={state}>{state}</option>}
          </select>
        </div>
      </div>

      <Alert type="error">{error}</Alert>
      {loading ? <Spinner label="Loading dealerships…" /> : (
        <div className="grid">
          {visible.map((d) => (
            <article className="card dealer-card" key={d.id}>
              <Link to={`/dealer/${d.id}`} className="card-media">
                <DealerImage src={d.image} alt={d.full_name} />
                <span className="chip">{d.st}</span>
              </Link>
              <div className="card-body">
                <h3><Link to={`/dealer/${d.id}`}>{d.full_name}</Link></h3>
                <p className="muted small">📍 {d.address}, {d.city}, {d.state} {d.zip}</p>
                <p className="muted small">📞 {d.phone}</p>
                <p className="desc">{d.description}</p>
              </div>
              <div className="card-actions">
                <Link className="btn btn-outline btn-sm" to={`/dealer/${d.id}`}>View reviews</Link>
                {user && <Link className="btn btn-accent btn-sm" to={`/postreview/${d.id}`}>Post Review</Link>}
              </div>
            </article>
          ))}
          {!visible.length && !error && <p className="empty">No dealerships match your filters.</p>}
        </div>
      )}
    </section>
  );
}
