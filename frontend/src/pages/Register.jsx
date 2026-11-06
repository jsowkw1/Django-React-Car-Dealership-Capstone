import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/auth';
import { Alert } from '../components/common';

const FIELDS = [
  { name: 'userName', label: 'Username', type: 'text', autoComplete: 'username', placeholder: 'Choose a username' },
  { name: 'firstName', label: 'First Name', type: 'text', autoComplete: 'given-name', placeholder: 'First name' },
  { name: 'lastName', label: 'Last Name', type: 'text', autoComplete: 'family-name', placeholder: 'Last name' },
  { name: 'email', label: 'Email', type: 'email', autoComplete: 'email', placeholder: 'you@example.com' },
  { name: 'password', label: 'Password', type: 'password', autoComplete: 'new-password', placeholder: 'At least 8 characters' },
];

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ userName: '', firstName: '', lastName: '', email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    const local = {};
    FIELDS.forEach((f) => { if (!form[f.name].trim()) local[f.name] = `${f.label} is required`; });
    if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) local.email = 'Enter a valid email address';
    if (form.password && form.password.length < 8) local.password = 'Password must be at least 8 characters';
    setErrors(local);
    if (Object.keys(local).length) return;
    setBusy(true);
    setMessage('');
    try {
      await register(form);
      navigate('/', { replace: true, state: { flash: `Welcome to Best Cars, ${form.firstName}! Your account has been created.` } });
    } catch (err) {
      setErrors(err.errors || {});
      setMessage(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="card form-card auth-card">
        <h1>Sign Up</h1>
        <p className="muted">Create your account to review dealerships.</p>
        <Alert type="error">{message}</Alert>
        <form onSubmit={submit} noValidate>
          {FIELDS.map((f) => (
            <label className="field" key={f.name}>
              <span>{f.label}</span>
              <input className="input" name={f.name} type={f.type} autoComplete={f.autoComplete} placeholder={f.placeholder}
                value={form[f.name]} onChange={(e) => setForm({ ...form, [f.name]: e.target.value })} />
              {errors[f.name] && <small className="error-text">{errors[f.name]}</small>}
            </label>
          ))}
          <button className="btn btn-accent btn-block" disabled={busy}>{busy ? 'Registering…' : 'Register'}</button>
        </form>
        <p className="muted center">Already have an account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  );
}
