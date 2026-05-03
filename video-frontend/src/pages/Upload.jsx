import { useState } from "react";
import { uploadVideo } from "../api/videoApi";
import { Link } from "react-router-dom";
import { useAuth, SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";

export default function Upload() {
    const [error, setError] = useState(null);
    const [title, setTitle] = useState("");
    const [file, setFile] = useState(null);
    const [progress, setProgress] = useState(0);
    const [uploading, setUploading] = useState(false);

    const { getToken } = useAuth();

    async function handleUpload() {
        try {
            const token = await getToken();

            const formData = new FormData();
            formData.append("title", title);
            formData.append("video_file", file);

            setUploading(true);
            setProgress(0);

            await uploadVideo(formData, token, setProgress);

            alert("Upload done.");

            setTitle("");
            setFile(null);
            setUploading(false);
        } catch (err) {
            setError(err.message);
            setUploading(false);
        }
    }

    return (
        <>
            <SignedIn>
                <div className="upload-container">

                    <h2>➕Upload Video</h2>

                    <input
                        type="text"
                        placeholder="Video Title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />

                    <input
                        type="file"
                        accept="video/*"
                        onChange={(e) => setFile(e.target.files[0])}
                    />

                    <button onClick={handleUpload} disabled={uploading}>
                        {uploading ? "Uploading..." : "Upload"}
                    </button>

                    {/* PROGRESS BAR */}
                    {uploading && (
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${progress}%` }}
                            />
                            <p>{progress}%</p>
                        </div>
                    )}

                    {error && <p className="error">{error}</p>}

                    {/* HOME BUTTON */}
                    <Link to="/">
                        <button className="home-btn">
                            ⌂ Home
                        </button>
                    </Link>

                </div>
            </SignedIn>

            <SignedOut>
                <RedirectToSignIn />
            </SignedOut>
        </>
    );
}