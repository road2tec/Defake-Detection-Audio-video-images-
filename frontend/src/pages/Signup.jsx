import React, { useState } from 'react';
import BackgroundAnimation from '../components/common/BackgroundAnimation';
import { Link, useNavigate } from 'react-router-dom';

const Signup = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSignup = (e) => {
        e.preventDefault();
        // Simulate signup logic
        console.log("Signing up with:", name, email, password);
        navigate('/dashboard');
    };

    return (
        <div style={{ position: 'relative', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <BackgroundAnimation />
            <div style={{
                zIndex: 1,
                background: 'rgba(26, 26, 32, 0.6)',
                padding: '3rem',
                borderRadius: '1.5rem',
                backdropFilter: 'blur(12px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                width: '400px',
                textAlign: 'center'
            }}>
                <h1 style={{ marginBottom: '2rem' }}>Sign Up</h1>
                <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Create an account to get started.</p>

                <form onSubmit={handleSignup}>
                    <input
                        type="text"
                        placeholder="Full Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        style={{ width: '100%', padding: '0.8rem', marginBottom: '1rem', borderRadius: '0.5rem', border: 'none', background: 'rgba(255,255,255,0.05)', color: 'white' }}
                        required
                    />
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{ width: '100%', padding: '0.8rem', marginBottom: '1rem', borderRadius: '0.5rem', border: 'none', background: 'rgba(255,255,255,0.05)', color: 'white' }}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ width: '100%', padding: '0.8rem', marginBottom: '2rem', borderRadius: '0.5rem', border: 'none', background: 'rgba(255,255,255,0.05)', color: 'white' }}
                        required
                    />

                    <button type="submit" style={{ width: '100%', marginBottom: '1rem', padding: '0.8rem', borderRadius: '0.5rem', border: 'none', background: 'var(--primary)', color: 'white', fontWeight: 'bold', cursor: 'pointer' }}>Create Account</button>
                </form>

                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Already have an account? <Link to="/login" style={{ color: 'var(--primary)' }}>Login</Link>
                </p>
            </div>
        </div>
    );
};

export default Signup;
