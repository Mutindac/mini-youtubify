const BASE_URL = 'https://mini-youtubify.onrender.com';
import axios from 'axios'; 

export async function getVideos() {
    const res = await fetch(`${BASE_URL}/videos/list/`);
    if (!res.ok) {
        throw new Error('Failed to fetch videos');
    }
    return res.json();
}

export async function uploadVideo(formData, onProgress) {
    const res = await axios.post(
        `${BASE_URL}/videos/upload/`,
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            onUploadProgress: (event) => {
                const percent = Math.round(
                    (event.loaded * 100) / event.total
                );

                if (onProgress) onProgress(percent);
            },
        }
    );

    return res.data;
}

export async function getVideo(id) {
    const res = await fetch(`${BASE_URL}/videos/detail/${id}/`);
    if (!res.ok) {
        throw new Error('Failed to fetch video');
    }
    return res.json();
}