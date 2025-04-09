import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';

const IdentifyCriminal = () => {
    const [error, setError] = useState("");
    const [userData, setUserData] = useState(null);
    const [isRunning, setIsRunning] = useState(false);
    const [intervalId, setIntervalId] = useState(null);
    const imgRef = useRef(null); // Create a ref for the img element

    useEffect(() => {
        if (imgRef.current) {
            imgRef.current.onerror = () => {
                setError("Unable to load video stream. Please check the server.");
            };
        }

        if (isRunning) {
            // Start polling when the camera is running
            const id = setInterval(async () => {
                try {
                    const response = await axios.get("http://localhost:5001/api/recognized-user");
                    const filename = response.data.filename;

                    const userDetailsResponse = await axios.get(`http://localhost:3001/api/user/${filename}`);
                    setUserData(userDetailsResponse.data);
                } catch (error) {
                    console.error("Error fetching user data", error);
                }
            }, 5000);  // poll every 5 seconds

            setIntervalId(id);
        }

        // Cleanup interval on unmount or when stopping the feed
        return () => clearInterval(intervalId);
    }, [isRunning]);

    const handleStart = () => {
        setIsRunning(true);
    };

    const handleStop = () => {
        setIsRunning(false);
        setUserData(null);  // Clear user data when stopping
        clearInterval(intervalId);  // Stop polling
    };

    return (
        <div style={styles.container}>
            <div style={styles.videoSection}>
                <h1 style={styles.title}>Live Video Feed</h1>
                {error && <p style={styles.error}>{error}</p>}
                {isRunning ? (
                    <img ref={imgRef} id="webcam-feed" src="http://localhost:5001/webcam" alt="Webcam feed" style={styles.videoFeed} />
                ) : (
                    <p style={styles.infoText}>Camera is off. Press "Start" to begin.</p>
                )}
                <div style={styles.buttonGroup}>
                    <button onClick={handleStart} disabled={isRunning} style={styles.button}>Start</button>
                    <button onClick={handleStop} disabled={!isRunning} style={styles.button}>Stop</button>
                </div>
            </div>

            <div style={styles.userInfoSection}>
                {userData ? (
                    <div style={styles.card}>
                        <h2 style={styles.subtitle}>Criminal Info</h2>
                        <p><strong>Name:</strong> {userData.name}</p>
                        <p><strong>Address:</strong> {userData.address}</p>
                        <p><strong>CNIC:</strong> {userData.cnic}</p>
                        <p><strong>Filename:</strong> {userData.img}</p>
                    </div>
                ) : (
                    <p style={styles.infoText}>No user data available.</p>
                )}
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'space-between',
        padding: '20px',
        backgroundColor: '#f4f6f9',
        minHeight: '80vh',
    },
    videoSection: {
        width: '45%',
        backgroundColor: '#fff',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        padding: '20px',
        textAlign: 'center',
    },
    title: {
        fontSize: '24px',
        fontWeight: '600',
        color: '#333',
    },
    error: {
        color: 'red',
        fontWeight: '500',
    },
    videoFeed: {
        width: '100%',
        borderRadius: '10px',
        marginTop: '20px',
    },
    infoText: {
        fontSize: '16px',
        color: '#666',
    },
    buttonGroup: {
        marginTop: '20px',
    },
    button: {
        padding: '10px 20px',
        margin: '0 10px',
        fontSize: '16px',
        color: '#fff',
        backgroundColor: '#007bff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease',
    },
    buttonDisabled: {
        backgroundColor: '#ccc',
    },
    userInfoSection: {
        width: '45%',
        backgroundColor: '#fff',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        padding: '20px',
        textAlign: 'left',
    },
    card: {
        padding: '15px',
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
        boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
    },
    subtitle: {
        fontSize: '20px',
        fontWeight: '600',
        color: '#333',
        marginBottom: '10px',
    },
};

export default IdentifyCriminal;
