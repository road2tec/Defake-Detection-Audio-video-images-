import React, { useState } from 'react';
import BackgroundAnimation from '../components/common/BackgroundAnimation';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        // Simulate login logic
        console.log("Logging in with:", email, password);
        // In a real app, you'd validate and maybe store a token
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
                <h1 style={{ marginBottom: '2rem' }}>Login</h1>
                <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Sign in to detect deepfakes.</p>

                <form onSubmit={handleLogin}>
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

                    <button type="submit" style={{ width: '100%', marginBottom: '1rem', padding: '0.8rem', borderRadius: '0.5rem', border: 'none', background: 'var(--primary)', color: 'white', fontWeight: 'bold', cursor: 'pointer' }}>Sign In</button>
                </form>

                <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Don't have an account? <Link to="/signup" style={{ color: 'var(--primary)' }}>Sign up</Link>
                </p>
            </div>
        </div>
    );
};

export default Login;
