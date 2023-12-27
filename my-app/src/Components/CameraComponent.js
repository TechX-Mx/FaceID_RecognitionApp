import React, { useRef, useEffect } from 'react';
import { Button } from 'react-bootstrap';

const CameraComponent = ({ onCapture }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    useEffect(() => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true})
                .then(stream => {
                    videoRef.current.srcObject = stream;
                })
                .catch(err => console.error("Error accessing the camera: ", err));
        }
    }, []);

    const captureImage = () => {
        const canvas = canvasRef.current;
        const video = videoRef.current;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        onCapture(canvas.toDataURL('image/png', 1.0));
    };

    return (
        <div className="d-flex flex-column align-items-center my-3">
            <video ref={videoRef} autoPlay style={{ maxWidth: '600px', width: '100%' }} />
            <div style={{ height: '20px' }}></div> {}
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            <Button variant="primary" onClick={captureImage}>Validate Identity</Button>
        </div>
    );
};

export default CameraComponent;
