import './App.css';
import { useState, useEffect } from 'react';
import axios from 'axios'; // Для отправки запросов

function App() {
    const [mode, setMode] = useState("directInput");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        // Добавьте эффекты, если необходимо
    }, []);

    const onUploadFile = async (event) => {
        const file = event.target.files[0];

        if (!file) return;

        try {
            setLoading(true);
            setProgress(0);

            // Добавьте логику для отправки файла на сервер для обработки
            // Вам также понадобится серверный код для обработки аудио/видео и создания .docx файла

            // Пример использования axios для отправки файла на сервер
            const formData = new FormData();
            formData.append('file', file);

            const response = await axios.post('/api/process', formData, {
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                },
            });

            // Получите результаты с сервера (например, ссылку на .docx файл) и установите их в state
            setResult(response.data.result);

            setLoading(false);
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    const onPasteLink = async (event) => {
        const link = event.target.value;

        if (!link) return;

        // Добавьте логику для извлечения аудиодорожки из видео по ссылке
        // И создания .docx файла с терминами

        try {
            setLoading(true);
            setProgress(0);

            // Пример использования axios для отправки запроса на сервер для обработки видео по ссылке
            const response = await axios.post('/api/process-youtube', { link }, {
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                },
            });

            // Получите результаты с сервера (например, ссылку на .docx файл) и установите их в state
            setResult(response.data.result);

            setLoading(false);
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    const downloadResult = () => {
        if (result) {
            // Добавьте логику для скачивания .docx файла
            window.location.href = result; // Перенаправление на скачивание файла
        }
    }

    return (
        <div className="container">
            <div>
                <button onClick={() => setMode("directInput")}>Upload audio</button>
                <button onClick={() => setMode("youTube")}>Download from YouTube</button>
            </div>
            <div>
                {mode === "directInput" ? (
                    <input onChange={onUploadFile} type="file" />
                ) : (
                    <input onChange={onPasteLink} type="text" placeholder="Enter YouTube link" />
                )}
            </div>
            {loading ? <progress value={progress} /> : null}
            <button hidden={!result} onClick={downloadResult}>Download result</button>
        </div>
    );
}

export default App;
