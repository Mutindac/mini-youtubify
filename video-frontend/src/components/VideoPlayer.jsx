import { useEffect, useRef, useState } from "react";
import Hls from "hls.js";
import { Link } from "react-router-dom";

export default function VideoPlayer({ url }) {
    const videoRef = useRef(null);
    const hlsRef = useRef(null);

    const [levels, setLevels] = useState([]);
    const [currentLevel, setCurrentLevel] = useState(-1);

    const qualityLabels = {
        0: "1080p",
        1: "720p",
        2: "480p",
    };

    useEffect(() => {
    if (!url) return;

    if (hlsRef.current) {
        hlsRef.current.destroy();
    }

    if (url.endsWith('.m3u8') && Hls.isSupported()) {
        const hls = new Hls();
        hlsRef.current = hls;
        hls.loadSource(url);
        hls.attachMedia(videoRef.current);
        hls.on(Hls.Events.MANIFEST_PARSED, (_, data) => {
            setLevels(data.levels);
        });
    } else {
        videoRef.current.src = url;
    }

    return () => {
        if (hlsRef.current) {
            hlsRef.current.destroy();
        }
    };
    }, [url]);

    function changeQuality(e) {
        const level = Number(e.target.value);
        setCurrentLevel(level);

        if (hlsRef.current) {
            hlsRef.current.currentLevel = level;
        }
    }

    return (
        <div className="video-page">

            <div className="video-player-container">
                <video ref={videoRef} controls />

                {levels.length > 0 && (
                    <div className="quality-selector">
                        <label>Quality:</label>

                        <select value={currentLevel} onChange={changeQuality}>
                            <option value={-1}>Auto</option>

                            {levels.map((_, i) => (
                                <option key={i} value={i}>
                                    {qualityLabels[i] || `Level ${i}`}
                                </option>
                            ))}
                        </select>
                    </div>
                )}
            </div>
            <div className="video-actions">
                <Link to="/">
                    <button className="home-btn">
                        Home
                    </button>
                </Link>
            </div>

        </div>
    );
}