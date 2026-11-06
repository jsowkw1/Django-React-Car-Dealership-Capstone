import { useState } from 'react';
import { Alert } from '../components/common';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' });
  const [sent, setSent] = useState('');
  const [error, setError] = useState('');

  function submit(e) {
    e.preventDefault();
    if (!form.name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) || !form.message) {
      setError('Please enter your name, a valid email and a message.');
      return;
    }
    setError('');
    setSent(`Thanks ${form.name}! This demo form does not send email, but your message would reach our support team within one business day.`);
    setForm({ name: '', email: '', subject: '', message: '' });
  }

  return (
    <>
      <section className="page-hero" style={{ backgroundImage: 'linear-gradient(rgba(11,31,58,.8), rgba(11,31,58,.8)), url(https://images.unsplash.com/photo-1497366216548-37526070297c?w=1600&q=70&auto=format&fit=crop)' }}>
        <div className="container">
          <span className="eyebrow">Contact Us</span>
          <h1>We are here to help</h1>
          <p>Questions about a dealer, a review or your account? Reach our customer team by phone, email or the form below.</p>
        </div>
      </section>
      <div className="container page contact-grid">
        <div className="contact-info">
          <div className="card contact-card">
            <img src="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=900&q=70&auto=format&fit=crop" alt="Best Cars head office showroom" />
            <div className="card-body">
              <h3>Best Cars Head Office</h3>
              <ul className="info-list">
                <li><span>Address</span>1200 Main Street, Suite 400, Kansas City, MO 64105</li>
                <li><span>Phone</span><a href="tel:+18165550100">+1 (816) 555-0100</a></li>
                <li><span>Email</span><a href="mailto:support@bestcars-demo.com">support@bestcars-demo.com</a></li>
                <li><span>Dealer partnerships</span><a href="mailto:partners@bestcars-demo.com">partners@bestcars-demo.com</a></li>
                <li><span>Hours</span>Mon–Fri 8:00–18:00 CT · Sat 9:00–14:00 CT</li>
              </ul>
            </div>
          </div>
        </div>
        <div className="card form-card">
          <h2>Send us a message</h2>
          <Alert type="success">{sent}</Alert>
          <Alert type="error">{error}</Alert>
          <form onSubmit={submit} noValidate>
            <div className="row">
              <label className="field"><span>Name</span>
                <input className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Your name" /></label>
              <label className="field"><span>Email</span>
                <input className="input" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="you@example.com" /></label>
            </div>
            <label className="field"><span>Subject</span>
              <input className="input" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} placeholder="How can we help?" /></label>
            <label className="field"><span>Message</span>
              <textarea className="input" rows="5" value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} placeholder="Write your message…" /></label>
            <button className="btn btn-accent btn-block">Send message</button>
          </form>
          <p className="muted small">Demonstration contact details — phone numbers and emails are fictional.</p>
        </div>
      </div>
    </>
  );
}
