'use client';
import { useState, useEffect } from "react";
import { getJobStatus } from '../api/binarize/route';

import TrackingOverlay from '@/app/components/imgCondition/TrackingOverlay';
import Upload from '@/app/components/imgCondition/Upload';
import { BinarizeCanvas, RenderImg } from '@/app/components/imgCondition/BinarizeCanvas';
import { uploadVideo } from "../api/binarize/routes";

import SoundButton from '@/app/components/ConfirmButton';
import StatusCard from '@/app/components/StatusCard';

export default function ProcessorStartCard() {
    //const [rangeNum, setNum] = useState(60);
    //const [hexNum, setHex] = useState("#2a3e25");
    //const [filename, setFile] = useState("");
    //const [centroid, setCentroid] = useState(null);
    const [jobId, setJobId] = useState("");
    const [statusFE, setStatusFe] = useState("");
    const [URL, setURL] = useState("");
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState(null);
    const [polling, setPolling] = useState(false);
    const [loading, setLoading] = useState(false);
    const [percent, setPercent] = useState(0);
    const [result, setResult] = useState(null);

    async function handleSubmit(e) {
        e.preventDefault();
        if (!file) return;

        setResult(null);
        setPercent(0);
        await uploadVideo(file);
        setPolling(true);
    }

    // async function handleSubmit(e) {
    //     e.preventDefault();
    //     if (!file) return;

    //     try {
    //         setLoading(true);
    //         const data = await uploadVideo(file);
    //         setResponse(data);
    //     } catch (err) {
    //         console.error(err);
    //     } finally {
    //         setLoading(false);
    //     }
    // }

    function setNumState(event) {
        setNum(event.target.value);
    }

    function setColor(event) {
        setHex(event.target.value);
    }

    function setFileName(event) {
        setFile(event.target.value);
        console.log(filename);
    }

    function setJob(data) {
        setJobId(data);
    }

    useEffect(() => {
        if (!polling) return;

        const intervalId = setInterval(async () => {
            try {
                const job = await getJobStatus();
                setPercent(job.percent ?? 0);

                if (job.status === "done") {
                    setResult(job.result);
                    setPolling(false);
                    setPercent(100);
                    clearInterval(intervalId);
                } else if (job.status === "error") {
                    console.error("Job error:", job.message);
                    setPolling(false);
                    clearInterval(intervalId);
                }
            } catch (err) {
                console.error("Polling error:", err);
            }
        }, 2000);

        return () => clearInterval(intervalId);
    }, [polling]);



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
            {polling && (
                <>
                    <p>Processing...</p>
                    <progress value={percent} max={100} />
                </>
            )}
            {result && (
                <>
                    <progress value={100} max={100} />
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