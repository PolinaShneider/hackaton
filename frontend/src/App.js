import './App.css';
import { useState } from 'react';
import ProgressBar from './ProgressBar';
import axios from 'axios';

function App() {
    const [mode, setMode] = useState("directInput");
    const [loading, setLoading] = useState(false);
    const [processing, setProcessing] = useState(false);
    const [result, setResult] = useState(null);
    const [progress, setProgress] = useState(0);

    const handleProcessing = async () => {
        try {
            setProcessing(true);
            const result = await axios.post('http://localhost:8000/ml_processor/process/', {
                test: '123'
            })
            setResult(result);
            setProcessing(false);
        } catch (e) {
            setProcessing(false);
        }
    }

    const onUploadFile = async (event) => {
        const file = event.target.files[0];
        setResult(null);

        if (!file) return;

        try {
            setLoading(true);
            setProgress(0);

            const formData = new FormData();
            formData.append('audio_file', file);

            const response = await axios.post('http://localhost:8000/api/upload_audio/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                },
            });

            setResult(response.data.result);

            setLoading(false);
            void handleProcessing();
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    const onPasteLink = async (event) => {
        const link = event.target.value;
        setResult(null);
        const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        if (!youtubeRegex.test(link)) {
            alert('Please enter a valid YouTube URL.');
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            setProgress(0);

            const response = await axios.post('http://localhost:8000/api/upload_video/', { youtube_url: link }, {
                responseType: 'blob',
                onDownloadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                },
            });

            setResult(response.data.result);
            void handleProcessing();
            setLoading(false);
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    const downloadResult = () => {
        if (result) {
            window.location.href = result; // Перенаправление на скачивание файла
        }
    }

    return (
        <div className="container">
            <div>
                <button disabled={loading} onClick={() => setMode("directInput")}>Upload audio</button>
                <button disabled={loading} onClick={() => setMode("youTube")}>Download from YouTube</button>
            </div>
            <div>
                {mode === "directInput" ? (
                    <input disabled={loading} onChange={onUploadFile} type="file" accept="audio/*"  />
                ) : (
                    <input disabled={loading} onChange={onPasteLink} type="text" placeholder="Enter YouTube link" />
                )}
            </div>
            <ProgressBar progress={progress} isLoading={loading} />
            <div hidden={!processing}>
                <h2>Processing started</h2>
                <p>Please, wait — we are processing your data. It can take some time</p>
            </div>
            <button hidden={loading || processing || !result} onClick={downloadResult}>Download result</button>
        </div>
    );
}

export default App;
