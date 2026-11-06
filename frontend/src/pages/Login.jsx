import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/auth';
import { Alert } from '../components/common';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    if (!userName.trim() || !password) return setError('Please enter your username and password.');
    setBusy(true);
    setError('');
    try {
      await login(userName.trim(), password);
      navigate(location.state?.from || '/', { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="card form-card auth-card">
        <h1>Welcome back</h1>
        <p className="muted">Log in to post reviews for your dealership.</p>
        <Alert type="error">{error}</Alert>
        <form onSubmit={submit} noValidate>
          <label className="field">
            <span>Username</span>
            <input className="input" name="username" autoComplete="username" value={userName}
              onChange={(e) => setUserName(e.target.value)} placeholder="Enter your username" />
          </label>
          <label className="field">
            <span>Password</span>
            <input className="input" name="password" type="password" autoComplete="current-password" value={password}
              onChange={(e) => setPassword(e.target.value)} placeholder="Enter your password" />
          </label>
          <button className="btn btn-accent btn-block" disabled={busy}>{busy ? 'Logging in…' : 'Login'}</button>
        </form>
        <p className="muted center">New to Best Cars? <Link to="/register">Register now</Link></p>
      </div>
    </div>
  );
}
