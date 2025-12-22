import React from 'react';
import Navbar from '../components/Layout/Navbar';
import BackgroundAnimation from '../components/common/BackgroundAnimation';
import { motion } from 'framer-motion';

const Features = () => {
    const features = [
        {
            title: "Advanced Audio Detection",
            description: "Analyze voice recordings to detect AI-generated speech patterns and synthetic artifacts invisible to the human ear.",
            icon: "🎙️"
        },
        {
            title: "Deepfake Image Analysis",
            description: "Scans images for pixel-level inconsistencies and generative noise footprints typical of GANs and Diffusion models.",
            icon: "🖼️"
        },
        {
            title: "Real-time Processing",
            description: "Get instant results with our optimized inference engine. No long wait times, just drag, drop, and detect.",
            icon: "⚡"
        },
        {
            title: "Secure & Private",
            description: "Your media is processed securely. We prioritize user privacy and data protection above all else.",
            icon: "🔒"
        },
        {
            title: "Video Deepfake Detection",
            description: "Advanced frame-by-frame analysis to detect manipulated videos, face swaps, and lip-sync inconsistencies.",
            icon: "🎥"
        }
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.2
            }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: {
            y: 0,
            opacity: 1
        }
    };

    return (
        <div style={{ minHeight: '100vh', paddingTop: '100px', position: 'relative', overflow: 'hidden' }}>
            <BackgroundAnimation />
            <Navbar />

            <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem', position: 'relative', zIndex: 1 }}>
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    style={{ textAlign: 'center', marginBottom: '4rem' }}
                >
                    <h1 style={{
                        fontSize: '3.5rem',
                        marginBottom: '1.5rem',
                        background: 'linear-gradient(to right, #fff, #a5b4fc)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent'
                    }}>
                        Powerful Detection Features
                    </h1>
                    <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto' }}>
                        Our multi-modal system uses state-of-the-art deep learning to separate reality from fabrication.
                    </p>
                </motion.div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                    style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                        gap: '2rem'
                    }}
                >
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            variants={itemVariants}
                            whileHover={{ scale: 1.05, backgroundColor: 'rgba(255,255,255,0.08)' }}
                            style={{
                                background: 'rgba(255,255,255,0.03)',
                                backdropFilter: 'blur(10px)',
                                padding: '2.5rem',
                                borderRadius: '1.5rem',
                                border: '1px solid rgba(255,255,255,0.1)',
                                transition: 'all 0.3s ease'
                            }}
                        >
                            <div style={{ fontSize: '3rem', marginBottom: '1.5rem' }}>{feature.icon}</div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'white' }}>{feature.title}</h3>
                            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>{feature.description}</p>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </div>
    );
};

export default Features;
