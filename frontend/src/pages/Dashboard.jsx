import React, { useState } from 'react';
import Navbar from '../components/Layout/Navbar';
import DragDrop from '../components/common/DragDrop';
import BackgroundAnimation from '../components/common/BackgroundAnimation';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const user = JSON.parse(localStorage.getItem('user'));
    const [file, setFile] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState([]);
    const [loadingHistory, setLoadingHistory] = useState(false);

    // Fetch history on mount if user is logged in
    React.useEffect(() => {
        if (user && user.email) {
            fetchHistory();
        }
    }, []);

    const fetchHistory = async () => {
        setLoadingHistory(true);
        try {
            const response = await fetch(`http://127.0.0.1:8080/history/${user.email}`);
            const data = await response.json();
            setHistory(data.history || []);
        } catch (error) {
            console.error("Error fetching history:", error);
        } finally {
            setLoadingHistory(false);
        }
    };

    const handleFileSelect = (selectedFile) => {
        setFile(selectedFile);
        setResult(null);
    };

    const handleAnalyze = async () => {
        if (!file) return;

        setAnalyzing(true);
        setResult(null);

        const formData = new FormData();
        formData.append('file', file);
        if (user && user.email) {
            formData.append('user_email', user.email);
        }

        try {
            const url = new URL('http://127.0.0.1:8080/predict');
            if (user && user.email) {
                url.searchParams.append('user_email', user.email);
            }

            const response = await fetch(url, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const data = await response.json();

            if (data.error) {
                console.error("Backend Error:", data.error, data.detail);
                setResult({
                    label: "ERROR",
                    confidence: 0,
                    errorDetail: data.detail || data.error
                });
                return;
            }

            setResult({
                label: data.label,
                confidence: data.confidence
            });

            // Refresh history if logged in
            if (user && user.email) {
                fetchHistory();
            }
        } catch (error) {
            console.error("Error analyzing file:", error);
            setResult({
                label: "OFFLINE",
                confidence: 0,
                errorDetail: "Ensure backend is running on port 8000."
            });
        } finally {
            setAnalyzing(false);
        }
    };

    const [predictionType, setPredictionType] = useState('audio'); // Default to audio as model is integrated

    return (
        <div style={{ minHeight: '100vh', paddingTop: '100px', position: 'relative' }}>
            <BackgroundAnimation />
            <Navbar />

            <div style={{ position: 'relative', zIndex: 1, maxWidth: '800px', margin: '0 auto', padding: '2rem', textAlign: 'center' }}>
                <h1 style={{ marginBottom: '1rem', fontSize: '2.5rem' }}>Upload Media for Analysis</h1>
                <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Login is optional. Select media type below.</p>

                {/* Type Selector */}
                <div style={{
                    display: 'inline-flex',
                    background: 'rgba(255,255,255,0.05)',
                    padding: '0.5rem',
                    borderRadius: '2rem',
                    marginBottom: '2rem',
                    border: '1px solid rgba(255,255,255,0.1)'
                }}>
                    <button
                        onClick={() => { setPredictionType('audio'); setFile(null); setResult(null); }}
                        style={{
                            padding: '0.8rem 2rem',
                            borderRadius: '1.5rem',
                            border: 'none',
                            background: predictionType === 'audio' ? 'var(--primary)' : 'transparent',
                            color: predictionType === 'audio' ? 'white' : 'var(--text-muted)',
                            cursor: 'pointer',
                            fontWeight: 600,
                            transition: 'all 0.3s'
                        }}
                    >
                        Audio
                    </button>
                    <button
                        onClick={() => { setPredictionType('image'); setFile(null); setResult(null); }}
                        style={{
                            padding: '0.8rem 2rem',
                            borderRadius: '1.5rem',
                            border: 'none',
                            background: predictionType === 'image' ? 'var(--primary)' : 'transparent',
                            color: predictionType === 'image' ? 'white' : 'var(--text-muted)',
                            cursor: 'pointer',
                            fontWeight: 600,
                            transition: 'all 0.3s'
                        }}
                    >
                        Image
                    </button>
                    <button
                        onClick={() => { setPredictionType('video'); setFile(null); setResult(null); }}
                        style={{
                            padding: '0.8rem 2rem',
                            borderRadius: '1.5rem',
                            border: 'none',
                            background: predictionType === 'video' ? 'var(--primary)' : 'transparent',
                            color: predictionType === 'video' ? 'white' : 'var(--text-muted)',
                            cursor: 'pointer',
                            fontWeight: 600,
                            transition: 'all 0.3s'
                        }}
                    >
                        Video
                    </button>
                </div>

                <DragDrop onFileSelect={handleFileSelect} acceptedType={predictionType} />

                {file && !result && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{ marginTop: '2rem' }}
                    >
                        <button
                            onClick={handleAnalyze}
                            disabled={analyzing}
                            style={{
                                padding: '1rem 3rem',
                                borderRadius: '30px',
                                background: analyzing ? 'var(--text-muted)' : 'var(--primary)',
                                color: 'white',
                                border: 'none',
                                fontSize: '1.1rem',
                                cursor: analyzing ? 'not-allowed' : 'pointer',
                                fontWeight: 600,
                                boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
                            }}
                        >
                            {analyzing ? 'Analyzing...' : 'Analyze Media'}
                        </button>
                    </motion.div>
                )}

                {result && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        style={{
                            marginTop: '3rem',
                            padding: '2rem',
                            background: 'rgba(255,255,255,0.05)',
                            borderRadius: '1rem',
                            border: '1px solid rgba(255,255,255,0.1)',
                            display: 'inline-block'
                        }}
                    >
                        <h2 style={{ marginBottom: '1rem' }}>Analysis Result</h2>
                        <div style={{
                            fontSize: '3rem',
                            fontWeight: 700,
                            color: result.label === 'REAL' ? '#10b981' : result.label === 'ERROR' || result.label === 'OFFLINE' ? '#f59e0b' : '#ef4444',
                            marginBottom: '0.5rem'
                        }}>
                            {result.label}
                        </div>
                        {result.errorDetail ? (
                            <p style={{ color: '#fca5a5', maxWidth: '300px' }}>{result.errorDetail}</p>
                        ) : (
                            <p style={{ color: 'var(--text-muted)' }}>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                        )}
                    </motion.div>
                )}

                {/* History Section - Only for logged in users */}
                {user ? (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{ marginTop: '4rem', textAlign: 'left', width: '100%' }}
                    >
                        <h2 style={{ marginBottom: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>Your Analysis History</h2>
                        {loadingHistory ? (
                            <p>Loading your history...</p>
                        ) : history.length > 0 ? (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '1.5rem' }}>
                                {history.map((item) => (
                                    <div key={item._id} style={{
                                        background: 'rgba(255,255,255,0.03)',
                                        padding: '1.5rem',
                                        borderRadius: '1rem',
                                        border: '1px solid rgba(255,255,255,0.05)',
                                        position: 'relative'
                                    }}>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                                            {new Date(item.timestamp).toLocaleString()}
                                        </div>
                                        <div style={{ fontWeight: 600, marginBottom: '0.5rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                            {item.filename}
                                        </div>
                                        <div style={{
                                            color: item.label === 'REAL' ? '#10b981' : '#ef4444',
                                            fontWeight: 700,
                                            fontSize: '1.2rem'
                                        }}>
                                            {item.label}
                                        </div>
                                        <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                                            {(item.confidence * 100).toFixed(1)}% Confidence
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p style={{ color: 'var(--text-muted)' }}>No history found. Start analyzing media to see them here!</p>
                        )}
                    </motion.div>
                ) : (
                    <p style={{ marginTop: '4rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                        💡 <Link to="/login" style={{ color: 'var(--primary)', fontWeight: 'bold' }}>Login</Link> to save your analysis results and see history.
                    </p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
