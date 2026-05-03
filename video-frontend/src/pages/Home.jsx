import { useEffect, useState } from "react";
import { getVideos } from "../api/videoApi";
import VideoCard from "../components/Videocard";
import { useClerk, SignedIn, SignedOut } from "@clerk/clerk-react";

export default function Home() {
    const [error, setError] = useState(null);
    const [videos, setVideos] = useState([]);

    const { signOut } = useClerk();

    useEffect(() => {
        loadVideos();
    }, []);

    async function loadVideos() {
        try {
            const data = await getVideos();
            setVideos(data);
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <div className="home">

            {/* NAVBAR */}
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "12px 20px",
                borderBottom: "1px solid #333",
                marginBottom: "20px"
            }}>
                <h1 style={{ margin: 0 }}> ⌂ Home</h1>

                {/* RIGHT BUTTONS */}
                <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>

                    {/* UPLOAD BUTTON (ONLY LOGGED IN  COMRADES) */}
                    <SignedIn>
                        <a href="/upload">
                            <button style={{
                                background: "green",
                                color: "white",
                                padding: "6px 12px",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer"
                            }}>
                                Upload
                            </button>
                        </a>
                    </SignedIn>

                    {/*LOGOUT */}
                    <SignedIn>
                        <button
                            onClick={() => signOut()}
                            style={{
                                background: "red",
                                color: "white",
                                padding: "6px 12px",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer"
                            }}
                        >
                            Sign-out
                        </button>
                    </SignedIn>

                    {/* LOGIN */}
                    <SignedOut>
                        <a href="/sign-in">
                            <button style={{
                                background: "blue",
                                color: "white",
                                padding: "6px 12px",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer"
                            }}>
                                Sign-in
                            </button>
                        </a>
                    </SignedOut>

                </div>
            </div>

            
            {error && <div className="error">{error}</div>}

            
            
            <div className="videos">
                {Array.isArray(videos) && videos.map((video) => (
                    <VideoCard key={video.id} video={video} />
                ))}
            </div>

        </div>
    );
}