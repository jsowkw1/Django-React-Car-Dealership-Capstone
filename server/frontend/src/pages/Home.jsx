import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import DealerList from '../components/DealerList';
import { Alert } from '../components/common';
import { useAuth } from '../services/auth';

export default function Home() {
  const { user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [flash, setFlash] = useState(location.state?.flash || '');

  useEffect(() => {
    if (location.state?.flash) {
      setFlash(location.state.flash);
      navigate(location.pathname, { replace: true, state: null });
    }
  }, [location.state, location.pathname, navigate]);

  return (
    <>
      <section className="hero">
        <div className="container hero-inner">
          <div className="hero-text">
            <span className="eyebrow">Nationwide dealership network</span>
            <h1>Find a dealer you can trust.</h1>
            <p>
              Browse certified dealerships across the United States, read honest reviews analysed for
              sentiment, and share your own buying experience.
            </p>
            <div className="hero-actions">
              <a href="#dealers" className="btn btn-accent">Browse dealers</a>
              {user ? (
                <span className="hero-welcome">Welcome back, <strong>{user.firstName || user.userName}</strong></span>
              ) : (
                <Link to="/register" className="btn btn-ghost">Create an account</Link>
              )}
            </div>
          </div>
          <div className="hero-stats">
            <div><strong>15</strong><span>Dealerships</span></div>
            <div><strong>11</strong><span>States</span></div>
            <div><strong>AI</strong><span>Sentiment analysis</span></div>
          </div>
        </div>
      </section>
      <div className="container" id="dealers">
        <Alert type="success" onClose={() => setFlash('')}>{flash}</Alert>
        <DealerList state="All" basePath="/" />
      </div>
    </>
  );
}
