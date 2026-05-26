// import { read } from "jimp";

export async function POST(req) {
  try {
    const { imageUrl, hexColor, threshold } = await req.json();

    const { read } = await import('jimp');

    const rTarget = parseInt(hexColor.slice(1, 3), 16);
    const gTarget = parseInt(hexColor.slice(3, 5), 16);
    const bTarget = parseInt(hexColor.slice(5, 7), 16);

    const image = await read(imageUrl);
    const { width, height, data } = image.bitmap;

    function colorDistance(r1, g1, b1, r2, g2, b2) {
      return Math.sqrt(
        Math.pow(r1 - r2, 2) +
        Math.pow(g1 - g2, 2) +
        Math.pow(b1 - b2, 2)
      );
    }

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const idx = (y * width + x) * 4;
        const r = data[idx];
        const g = data[idx + 1];
        const b = data[idx + 2];

        const distance = colorDistance(r, g, b, rTarget, gTarget, bTarget);
        const color = distance >= threshold ? 0xFFFFFFFF : 0x000000FF;

        image.setPixelColor(color, x, y);
      }
    }

    const base64 = await image.getBase64Async("image/png");
    return new Response(JSON.stringify({ base64 }), { headers: { "Content-Type": "application/json" } });
  } catch (error) {
    console.error('Binarize API Error:', error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}

export async function fetchVideos() {
  try {
    // Send a GET request to the backend to fetch the video list
    const response = await fetch('http://localhost:3000/videos');

    // Check if the response is successful (status 200)
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // Parse the JSON response directly into an array
    const videoArray = await response.json();

    // Since the backend sends a plain array, no mapping is needed
    console.log(videoArray); // This is the array of filenames

    return videoArray; // Return the array of filenames
  } catch (error) {
    console.error('Error fetching videos:', error);
    return []; // Return an empty array in case of an error
  }
}

export async function fetchResults() {
  try {
    // Send a GET request to the backend to fetch the video list
    const response = await fetch('http://localhost:3000/process');

    // Check if the response is successful (status 200)
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // Parse the JSON response directly into an array
    const resultArray = await response.json();

    // Since the backend sends a plain array, no mapping is needed
    console.log(resultArray); // This is the array of filenames

    return resultArray; // Return the array of filenames
  } catch (error) {
    console.error('Error fetching videos:', error);
    return []; // Return an empty array in case of an error
  }
}

export async function fetchImg(filename) {
  try {
    let response;

    // Check if the filename ends with .mp4 (fetch thumbnail), otherwise fetch the image
    if (filename.endsWith('.mp4')) {
      response = await fetch(`http://localhost:3000/thumbnail/${filename}`);
    } else {
      response = await fetch(`http://localhost:3000/videos/${filename}`);
    }

    // Check if the response is successful (status 200)
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // Convert the response to a blob (binary large object)
    const blob = await response.blob();

    // Create a local URL for the blob
    const imageUrl = URL.createObjectURL(blob);

    // Return the image URL so that it can be used in an <img> tag
    return imageUrl;
  } catch (error) {
    console.error('Error fetching image:', error);
    return ''; // Return an empty string in case of an error
  }
}

export async function startProcessing(filename, targetColor, threshold) {

  const target = targetColor.replace("#", "");
  const res = await fetch(`http://localhost:3000/process/${filename}?targetColor=${target}&threshold=${threshold}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    }
  );

  const data = await res.json();
  console.log(data);
  return data;
}

export async function getJobStatus(jobId) {
  const res = await fetch(`http://localhost:8000/track`);

  const data = await res.json();
  console.log(data);
  return data;
}

