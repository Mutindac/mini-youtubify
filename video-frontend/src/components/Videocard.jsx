import { useNavigate } from 'react-router-dom';

export default function VideoCard({ video }) {
    const navigate = useNavigate();

    const thumbnailUrl = video.thumbnail_url?.startsWith("http")
    ? video.thumbnail_url
    : `http://127.0.0.1:7000${video.thumbnail_url}`;

    return (
        <div className="video-card" onClick={() => navigate(`/videos/${video.id}`)} style={{ cursor: 'pointer' }}>
            <img src={thumbnailUrl} alt={video.title} width="250" height="140" />
            <h3>{video.title}</h3>
            <p>Status: {video.status}</p>
        </div>
    );
}