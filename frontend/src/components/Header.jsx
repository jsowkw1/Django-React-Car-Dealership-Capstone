import { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../services/auth';

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  async function handleLogout() {
    const name = user?.userName;
    window.alert(`Logging out ${name}...`);
    await logout();
    setOpen(false);
    navigate('/', { state: { flash: `You have been logged out successfully. Goodbye, ${name}!` } });
  }

  const navClass = ({ isActive }) => `nav-link${isActive ? ' active' : ''}`;

  return (
    <header className="header">
      <div className="container header-inner">
        <Link to="/" className="brand" onClick={() => setOpen(false)}>
          <img src={`${import.meta.env.BASE_URL}favicon.svg`} alt="" width="34" height="34" />
          <span>Best<strong>Cars</strong></span>
        </Link>
        <button className="nav-toggle" aria-label="Toggle navigation" onClick={() => setOpen(!open)}>
          <span /><span /><span />
        </button>
        <nav className={`nav${open ? ' open' : ''}`} onClick={(e) => e.target.tagName === 'A' && setOpen(false)}>
          <NavLink to="/" end className={navClass}>Home</NavLink>
          <NavLink to="/dealers" className={navClass}>Dealers</NavLink>
          <NavLink to="/about" className={navClass}>About Us</NavLink>
          <NavLink to="/contact" className={navClass}>Contact Us</NavLink>
          <div className="nav-auth">
            {user ? (
              <>
                <span className="nav-user" title={user.email}>
                  <span className="avatar">{user.userName.slice(0, 1).toUpperCase()}</span>
                  {user.userName}
                </span>
                <button className="btn btn-outline btn-sm" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <>
                <NavLink to="/login" className={navClass}>Login</NavLink>
                <Link to="/register" className="btn btn-accent btn-sm">Register</Link>
              </>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}
