import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div>
          <div className="brand brand-light"><span>Best<strong>Cars</strong></span></div>
          <p className="muted-light">Honest reviews from real buyers across a nationwide dealership network.</p>
        </div>
        <div className="footer-links">
          <Link to="/dealers">Dealers</Link>
          <a href="/about">About Us</a>
          <a href="/contact">Contact Us</a>
          <a href="/admin/">Admin</a>
        </div>
        <p className="muted-light small">
          © {new Date().getFullYear()} Best Cars — IBM Full Stack Capstone demonstration project. All dealer, review and team data is fictional.
        </p>
      </div>
    </footer>
  );
}
