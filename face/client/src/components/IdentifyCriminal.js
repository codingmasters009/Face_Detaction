import React, { useEffect, useState } from 'react';  

const IdentifyCriminal = () => {  
    const [error, setError] = useState("");  

    useEffect(() => {  
        const img = document.getElementById("webcam-feed");  
        img.onerror = () => {  
            setError("Unable to load video stream. Please check the server.");  
        };  
    }, []);  

    return (  
        <div>  
            <h1>Live Video Feed</h1>  
            {error && <p style={{color: "red"}}>{error}</p>}  
            <img id="webcam-feed" src="http://localhost:5001/webcam" alt="Webcam feed" />  
        </div>  
    );  
};  

export default IdentifyCriminal;