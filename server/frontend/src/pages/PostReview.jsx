import { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../services/auth';
import { Alert, Spinner } from '../components/common';

const today = () => new Date().toISOString().slice(0, 10);

export default function PostReview() {
  const { id } = useParams();
  const { user, loading } = useAuth();
  const navigate = useNavigate();
  const [dealer, setDealer] = useState(null);
  const [cars, setCars] = useState([]);
  const [form, setForm] = useState({ review: '', purchase: true, purchase_date: '', car_id: '', rating: 0 });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.dealer(id).then((d) => setDealer(d.dealer)).catch((e) => setMessage(e.message));
    api.cars().then((c) => setCars(c.CarModels)).catch(() => {});
  }, [id]);

  if (loading) return <div className="container page"><Spinner /></div>;
  if (!user) return <Navigate to="/login" state={{ from: `/postreview/${id}` }} replace />;

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.type === 'checkbox' ? e.target.checked : e.target.value });

  async function submit(e) {
    e.preventDefault();
    const local = {};
    if (form.review.trim().length < 5) local.review = 'Please write at least 5 characters.';
    if (!form.rating) local.rating = 'Please choose a rating.';
    if (form.purchase && !form.purchase_date) local.purchase_date = 'Please enter the purchase date.';
    if (!form.car_id) local.car = 'Please choose your car.';
    setErrors(local);
    if (Object.keys(local).length) return;
    setSubmitting(true);
    setMessage('');
    try {
      const res = await api.addReview({
        ...form,
        dealership: Number(id),
        rating: Number(form.rating),
        car_id: Number(form.car_id),
        purchase_date: form.purchase ? form.purchase_date : '',
      });
      navigate(`/dealer/${id}`, { state: { newReviewId: res.review.id } });
    } catch (err) {
      setErrors(err.errors || {});
      setMessage(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="container page narrow">
      <Link to={`/dealer/${id}`} className="back-link">← Back to dealer</Link>
      <div className="card form-card">
        <h1>Post a review</h1>
        <p className="muted">{dealer ? <>for <strong>{dealer.full_name}</strong>, {dealer.city}, {dealer.state}</> : 'Loading dealer…'}</p>
        <Alert type="error">{message}</Alert>
        <form onSubmit={submit} noValidate>
          <label className="field">
            <span>Your review</span>
            <textarea className="input" rows="5" maxLength="2000" value={form.review} onChange={set('review')}
              placeholder="Tell other buyers about your experience…" />
            {errors.review && <small className="error-text">{errors.review}</small>}
          </label>

          <div className="field">
            <span>Rating</span>
            <div className="rating-input" role="radiogroup" aria-label="Rating">
              {[1, 2, 3, 4, 5].map((n) => (
                <button type="button" key={n} role="radio" aria-checked={Number(form.rating) === n}
                  className={n <= form.rating ? 'star-btn on' : 'star-btn'} onClick={() => setForm({ ...form, rating: n })}>★</button>
              ))}
              <span className="muted small">{form.rating ? `${form.rating} / 5` : 'Select'}</span>
            </div>
            {errors.rating && <small className="error-text">{errors.rating}</small>}
          </div>

          <label className="check">
            <input type="checkbox" checked={form.purchase} onChange={set('purchase')} />
            I purchased a car from this dealer
          </label>

          <div className="row">
            <label className="field">
              <span>Purchase date</span>
              <input className="input" type="date" max={today()} value={form.purchase_date} onChange={set('purchase_date')} disabled={!form.purchase} />
              {errors.purchase_date && <small className="error-text">{errors.purchase_date}</small>}
            </label>
            <label className="field">
              <span>Car make, model and year</span>
              <select className="input" value={form.car_id} onChange={set('car_id')}>
                <option value="">Choose car…</option>
                {cars.map((c) => <option key={c.id} value={c.id}>{c.CarMake} {c.CarModel} ({c.year})</option>)}
              </select>
              {errors.car && <small className="error-text">{errors.car}</small>}
            </label>
          </div>

          <button className="btn btn-accent btn-block" disabled={submitting}>
            {submitting ? 'Posting…' : 'Post Review'}
          </button>
        </form>
      </div>
    </div>
  );
}
