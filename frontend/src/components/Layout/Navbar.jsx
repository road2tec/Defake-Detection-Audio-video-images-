import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <Link to="/" className="logo">DeepDetect</Link>
            <div className="nav-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/features" className="nav-link">Features</Link>
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
            </div>
        </nav>
    );
};

export default Navbar;
