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
                setError("Unable to load video stream. Please check the server.")
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
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>  
            <div style={{ width: '45%' }}>
                <h1>Live Video Feed</h1>  
                {error && <p style={{color: "red"}}>{error}</p>}  
                {isRunning ? (
                    <img ref={imgRef} id="webcam-feed" src="http://localhost:5001/webcam" alt="Webcam feed" style={{ width: '100%' }} />
                ) : (
                    <p>Camera is off. Press "Start" to begin.</p>
                )}
                <button onClick={handleStart} disabled={isRunning}>Start</button>
                <button onClick={handleStop} disabled={!isRunning}>Stop</button>
            </div>  

            <div style={{ width: '45%' }}>
                {userData ? (
                    <div>
                        <h2>Criminal Info</h2>
                        <p>Name: {userData.name}</p>
                        <p>Address: {userData.address}</p>
                        <p>CNIC: {userData.cnic}</p>
                        <p>Filename: {userData.img}</p>
                    </div>
                ) : (
                    <p>No user data available.</p>
                )}
            </div>
        </div>  
    );  
};  

export default IdentifyCriminal;
