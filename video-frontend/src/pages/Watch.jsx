import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getVideo } from "../api/videoApi";
import VideoPlayer from "../components/VideoPlayer";
import "../watch.css";

export default function Watch() {
    const { id } = useParams();
    const [video, setVideo] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadVideo();
    }, [id]);

    async function loadVideo() {
        try {
            const data = await getVideo(id);
            setVideo(data);
        } catch (err) {
            setError(err.message);
        }
    }

    if (!video) return <div>Loading...</div>;

    return (
        <div className="watch-page">
            <h2>{video.title}</h2>

            {error && <p className="error">{error}</p>}

            <div className="video-player-container">
                <VideoPlayer url={video.hls_playlist_url} />
            </div>
        </div>
    );
}