'use client';

import { useState, useEffect } from "react";
import { uploadVideo } from "../../api/binarize/routes";

export default function Upload(props) {
    const [videoUrl, setVideoUrl] = useState([]);

    async function handleFileChanges(e) {
        const file = e.target.files[0];
        if (!file) return;

        try {
            const data = await uploadVideo(file);
            console.log("Upload result:", data);
            setVideoUrl(data.video_url);
        }
        catch (err) {
            console.error("Error uploading video:", err);
        }
    }

    return (
        <>
            <input type="file" accept="video/*" onChange={handleFileChanges} />
            {videoUrl && <video src={videoUrl} controls />}
        </>
    );
}
