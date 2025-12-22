import React, { useState, useRef } from 'react';
import { Upload, FileAudio, FileImage, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const DragDrop = ({ onFileSelect, acceptedType = 'audio' }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [file, setFile] = useState(null);
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        validateAndSetFile(droppedFile);
    };

    const handleFileInput = (e) => {
        const selectedFile = e.target.files[0];
        validateAndSetFile(selectedFile);
    };

    const validateAndSetFile = (file) => {
        if (!file) return;

        // Dynamic validation based on props or default (handled by input accept but good to double check)
        const validImageTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const validAudioTypes = ['audio/mpeg', 'audio/wav', 'audio/mp3', 'audio/x-wav'];

        const fileType = file.type;

        let isValid = false;

        if (acceptedType === 'image') {
            if (validImageTypes.includes(fileType)) isValid = true;
        } else if (acceptedType === 'audio') {
            if (validAudioTypes.includes(fileType)) isValid = true;
        } else if (acceptedType === 'video') {
            const validVideoTypes = ['video/mp4', 'video/webm', 'video/ogg'];
            if (validVideoTypes.includes(fileType)) isValid = true;
        }

        if (isValid) {
            setFile(file);
            onFileSelect(file);
        } else {
            alert(`Please upload a valid ${acceptedType} file.`);
        }
    };

    const removeFile = () => {
        setFile(null);
        onFileSelect(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
    };

    return (
        <div style={{ width: '100%', maxWidth: '600px', margin: '0 auto' }}>
            <AnimatePresence>
                {!file ? (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
                        onDragOver={handleDragOver}
                        onDragLeave={handleDragLeave}
                        onDrop={handleDrop}
                        onClick={() => fileInputRef.current?.click()}
                        style={{
                            border: `2px dashed ${isDragging ? 'var(--primary)' : 'rgba(255,255,255,0.2)'}`,
                            borderRadius: '1rem',
                            padding: '3rem',
                            textAlign: 'center',
                            cursor: 'pointer',
                            background: isDragging ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255,255,255,0.03)',
                            transition: 'all 0.3s ease'
                        }}
                    >
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleFileInput}
                            style={{ display: 'none' }}
                            accept={acceptedType === 'image' ? "image/*" : acceptedType === 'video' ? "video/*" : "audio/*"}
                        />
                        <Upload size={48} color={isDragging ? 'var(--primary)' : 'var(--text-muted)'} style={{ marginBottom: '1rem' }} />
                        <h3 style={{ marginBottom: '0.5rem' }}>Drag & Drop or Click to Upload</h3>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                            Supported formats: JPEG, PNG, MP3, WAV
                        </p>
                    </motion.div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="file-preview"
                        style={{
                            background: 'rgba(255,255,255,0.05)',
                            borderRadius: '1rem',
                            padding: '1.5rem',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            border: '1px solid rgba(255,255,255,0.1)'
                        }}
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            {file.type.startsWith('image/') ? (
                                <div style={{ width: '50px', height: '50px', borderRadius: '8px', overflow: 'hidden' }}>
                                    <img src={URL.createObjectURL(file)} alt="Preview" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                                </div>
                            ) : file.type.startsWith('video/') ? (
                                <div style={{ width: '50px', height: '50px', borderRadius: '8px', overflow: 'hidden', background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                    <span style={{ fontSize: '24px' }}>🎥</span>
                                </div>
                            ) : (
                                <FileAudio size={40} color="var(--primary)" />
                            )}
                            <div style={{ textAlign: 'left' }}>
                                <p style={{ fontWeight: 500 }}>{file.name}</p>
                                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                        </div>
                        <button
                            onClick={(e) => { e.stopPropagation(); removeFile(); }}
                            style={{ background: 'transparent', padding: '0.5rem', borderRadius: '50%', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
                        >
                            <X size={20} />
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default DragDrop;
