import { useEffect, useState } from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../services/auth';
import { Alert, DealerImage, SentimentBadge, Spinner, Stars } from '../components/common';

export default function DealerDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const location = useLocation();
  const newReviewId = location.state?.newReviewId;
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    setError('');
    Promise.all([api.dealer(id), api.reviews(id)])
      .then(([d, r]) => { setDealer(d.dealer); setReviews(r); })
      .catch((e) => setError(e.message));
  }, [id]);

  if (error) return <div className="container page"><Alert type="error">{error}</Alert><Link to="/dealers">← Back to dealers</Link></div>;
  if (!dealer || !reviews) return <div className="container page"><Spinner label="Loading dealer…" /></div>;

  return (
    <div className="container page">
      <Link to="/dealers" className="back-link">← All dealers</Link>
      {newReviewId && <Alert type="success">Thank you! Your review has been posted successfully.</Alert>}
      <section className="dealer-hero card">
        <div className="dealer-hero-media"><DealerImage src={dealer.image} alt={dealer.full_name} /></div>
        <div className="dealer-hero-body">
          <span className="chip chip-static">{dealer.state}</span>
          <h1>{dealer.full_name}</h1>
          <p className="desc">{dealer.description}</p>
          <ul className="info-list">
            <li><span>Address</span>{dealer.address}, {dealer.city}, {dealer.st} {dealer.zip}</li>
            <li><span>Phone</span>{dealer.phone}</li>
            <li><span>Rating</span>
              {reviews.average_rating ? <><Stars value={reviews.average_rating} /> <strong>{reviews.average_rating}</strong>&nbsp;/ 5 · {reviews.count} reviews</> : 'No ratings yet'}
            </li>
          </ul>
          {user ? (
            <Link to={`/postreview/${dealer.id}`} className="btn btn-accent">✍ Post Review</Link>
          ) : (
            <p className="muted"><Link to="/login" state={{ from: `/dealer/${dealer.id}` }}>Log in</Link> to post a review.</p>
          )}
        </div>
      </section>

      <h2 className="section-title">Customer reviews ({reviews.count})</h2>
      {reviews.count === 0 ? (
        <p className="empty">No reviews yet — be the first to share your experience.</p>
      ) : (
        <div className="reviews">
          {reviews.reviews.map((r) => (
            <article key={r.id} className={`card review-card${r.id === newReviewId ? ' review-new' : ''}`}>
              <header>
                <div className="avatar avatar-lg">{r.name.slice(0, 1)}</div>
                <div>
                  <strong>{r.name}</strong>
                  <div className="muted small">{r.purchase ? `Purchased ${r.purchase_date || ''}` : 'Did not purchase'}</div>
                </div>
                <SentimentBadge sentiment={r.sentiment} />
              </header>
              <Stars value={r.rating} size="sm" />
              <p>{r.review}</p>
              {(r.car_make || r.car_model) && (
                <footer className="muted small">🚗 {r.car_make} {r.car_model} {r.car_year}</footer>
              )}
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
