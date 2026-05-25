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
    const [rangeNum, setNum] = useState(60);
    const [hexNum, setHex] = useState("#2a3e25");
    //const [filename, setFile] = useState("");
    const [centroid, setCentroid] = useState(null);
    const [jobId, setJobId] = useState("");
    const [statusFE, setStatusFe] = useState("");
    const [URL, setURL] = useState("");
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);


    async function handleSubmit(e) {
        e.preventDefault();
        if (!file) return;

        try {
            setLoading(true);
            const data = await uploadVideo(file);
            setResponse(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

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
        if (!jobId) return;

        let intervalId = null;
        let stopped = false;

        async function poll() {
            try {
                const status = await getJobStatus(jobId.jobId);
                setURL(jobId.jobId);
                console.log("URL:", URL);
                setStatusFe(status.status);
                console.log("STATUS:", status);

                if (status.status === "done") {
                    console.log("Job finished!", status.result);
                    stopped = true;
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
            stopped = true;
        };
    }, [jobId])


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
            {loading && <p>Processing...</p>}
            {response && (
                <>
                    <video src={response.video_url} controls />
                    {response.tracks && response.tracks.length > 0 && (
                        <table>
                            <thead>
                                <tr>
                                    <th>Track ID</th>
                                    <th>Label</th>
                                    <th>Time on Screen (s)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {response.tracks.map((track) => (
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