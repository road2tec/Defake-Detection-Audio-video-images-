import React from 'react';
import BackgroundAnimation from '../components/common/BackgroundAnimation';
import Navbar from '../components/Layout/Navbar';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div style={{ position: 'relative', minHeight: '100vh', overflow: 'hidden' }}>
            <BackgroundAnimation />
            <Navbar />

            <div style={{
                position: 'relative',
                zIndex: 1,
                height: '100vh',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
                padding: '0 1rem'
            }}>
                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    style={{ fontSize: '4rem', marginBottom: '1rem', background: 'linear-gradient(to right, #fff, #a1a1aa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}
                >
                    Detect Real or Fake.
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    style={{ maxWidth: '600px', fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '3rem', lineHeight: 1.6 }}
                >
                    Advanced AI-powered system to analyze images and audio for authenticity. Protect yourself from deepfakes.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                >
                    <Link to="/dashboard">
                        <button style={{
                            padding: '1rem 3rem',
                            fontSize: '1.1rem',
                            borderRadius: '30px',
                            background: 'var(--primary)',
                            color: 'white',
                            border: 'none',
                            cursor: 'pointer',
                            fontWeight: 600,
                            boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)'
                        }}>
                            Start Detection
                        </button>
                    </Link>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.6 }}
                    style={{ marginTop: '1rem' }}
                >
                    <Link to="/login" style={{ color: 'var(--text-muted)', fontSize: '0.9rem', textDecoration: 'underline' }}>
                        Login to save history (Optional)
                    </Link>
                </motion.div>
            </div>
        </div>
    );
};

export default Home;
