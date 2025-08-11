// src/components/EmotionRecommender.js
import React, { useRef, useState, useEffect } from 'react';

export default function EmotionRecommender() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [emotion, setEmotion] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function setupWebcam() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (err) {
        setError('Could not access webcam: ' + err.message);
      }
    }
    setupWebcam();
  }, []);

  const captureAndSend = async () => {
    if (!videoRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const base64Image = canvas.toDataURL('image/jpeg');

    setEmotion('Detecting emotion...');
    setMovies([]);
    setError('');

    try {
      const res = await fetch('http://127.0.0.1:5000/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || res.statusText);
      }

      const data = await res.json();
      setEmotion(`${data.emotion} (${data.confidence.toFixed(2)}%)`);
      setMovies(data.recommendations || []);
    } catch (err) {
      setError(err.message);
      setEmotion('');
    }
  };

  return (
    <div>
      <h1>🎭 Emotion-Based Movie Recommender</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <video ref={videoRef} autoPlay playsInline style={{ width: 320, height: 240, border: '1px solid black' }} />
      <br />
      <button onClick={captureAndSend}>Capture & Recommend</button>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <h2>{emotion}</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {movies.map((movie) => (
          <img
            key={movie.title}
            src={movie.poster_url}
            alt={movie.title}
            title={movie.title}
            style={{ width: 120, margin: 10 }}
          />
        ))}
      </div>
    </div>
  );
}
