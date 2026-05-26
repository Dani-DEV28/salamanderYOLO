'use client';
import { useState, useEffect } from "react";
import { getJobStatus } from '../api/binarize/route';
import { uploadVideo } from "../api/binarize/routes";

export default function ProcessorStartCard() {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [percent, setPercent] = useState(0);

    async function handleSubmit(e) {
        e.preventDefault();
        if (!file) return;

        try {
            setLoading(true);
            setPercent(0);
            const data = await uploadVideo(file);
            setStatus(data.status || "processing");
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        if (status !== "processing") return;

        let intervalId = null;

        async function poll() {
            try {
                const job = await getJobStatus();
                console.log("STATUS:", job);

                setPercent(job.percent ?? 0);
                setStatus(job.status || "processing");

                if (job.status === "done") {
                    console.log("Job finished!", job.result);
                    setResult(job.result);
                    setPercent(100);
                    clearInterval(intervalId);

                }
            } catch (err) {
                console.error("Error polling job:", err);
            }
        }
        intervalId = setInterval(poll, 2000);
        poll();

        return () => {
            clearInterval(intervalId);
        };
    }, [status])


    return (
        <>
            <form className="container-card-starter" onSubmit={handleSubmit}>
                <div className="card-row">
                    <div className="card-left">
                        <ul>
                            <li>Import Video </li>
                            <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files[0])} />
                            <button type="submit" disabled={loading}>Submit</button>
                        </ul>
                    </div>
                </div>
            </form>
            {(loading || status === "processing") && (
                <>
                    <p>Processing...</p>
                    <progress value={percent} max={100} />
                </>
            )}
            {result && (
                <>
                    <video src={result.video_url} controls />
                    {result.tracks && result.tracks.length > 0 && (
                        <table>
                            <thead>
                                <tr>
                                    <th>Track ID</th>
                                    <th>Label</th>
                                    <th>Time on Screen (s)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {result.tracks.map((track) => (
                                    <tr key={track.track_id}>
                                        <td>{track.track_id}</td>
                                        <td>{track.label}</td>
                                        <td>{track.time_on_screen_s}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </>
            )}
        </>
    )
}