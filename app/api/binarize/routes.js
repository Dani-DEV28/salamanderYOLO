export async function uploadVideo(file) {
    try {

        const form = new FormData();
        form.append("video", file);
        const res = await fetch("http://localhost:8000/track", {
            method: "POST",
            body: form,
        });

        // Check if the response is successful (status 200)
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response directly into an array
        const videoArray = await res.json();

        // Since the backend sends a plain array, no mapping is needed
        console.log(videoArray); // This is the array of filenames

        return videoArray; // Return the array of filenames
    } catch (error) {
        console.error('Error fetching videos:', error);
        return []; // Return an empty array in case of an error
    }
}