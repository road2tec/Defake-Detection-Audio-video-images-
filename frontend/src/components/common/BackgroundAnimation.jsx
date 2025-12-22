import React from 'react';
import { motion } from 'framer-motion';
import './BackgroundAnimation.css';

const balls = [
    { size: 400, color: '#4f46e5', initialX: '10%', initialY: '10%' },
    { size: 350, color: '#ec4899', initialX: '70%', initialY: '20%' },
    { size: 300, color: '#06b6d4', initialX: '40%', initialY: '60%' },
];

const BackgroundAnimation = () => {
    return (
        <div className="animation-container">
            {balls.map((ball, index) => (
                <motion.div
                    key={index}
                    className="soft-ball"
                    style={{
                        width: ball.size,
                        height: ball.size,
                        backgroundColor: ball.color,
                        left: ball.initialX,
                        top: ball.initialY,
                    }}
                    animate={{
                        x: [0, 50, -30, 0],
                        y: [0, -40, 60, 0],
                        scale: [1, 1.1, 0.9, 1],
                    }}
                    transition={{
                        duration: 15 + index * 5,
                        repeat: Infinity,
                        repeatType: 'reverse',
                        ease: "easeInOut",
                    }}
                />
            ))}
        </div>
    );
};

export default BackgroundAnimation;
