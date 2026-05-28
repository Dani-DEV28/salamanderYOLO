"use client";
import { useEffect, useState } from "react";

export default function FetchComp() {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("http://localhost:8000/")
            .then((res) => res.json())
            .then((data) => setData(data))
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            {/* <h1>Data from API:</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre> */}
        </div>);
}