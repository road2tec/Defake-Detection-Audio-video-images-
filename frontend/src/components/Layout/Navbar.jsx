import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    const user = JSON.parse(localStorage.getItem('user'));

    const handleLogout = () => {
        localStorage.removeItem('user');
        window.location.href = '/';
    };

    return (
        <nav className="navbar">
            <Link to="/" className="logo">DeepDetect</Link>
            <div className="nav-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/features" className="nav-link">Features</Link>
                {user ? (
                    <>
                        <span className="nav-link" style={{ opacity: 0.7 }}>Hi, {user.name}</span>
                        <button onClick={handleLogout} className="nav-link" style={{
                            background: 'transparent',
                            border: 'none',
                            cursor: 'pointer',
                            color: 'var(--primary)',
                            fontWeight: 'bold'
                        }}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Login</Link>
                        <Link to="/signup" className="nav-link" style={{
                            background: 'white',
                            color: 'black',
                            padding: '0.4rem 1.2rem',
                            borderRadius: '20px',
                            fontWeight: 500
                        }}>
                            Get Started
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
