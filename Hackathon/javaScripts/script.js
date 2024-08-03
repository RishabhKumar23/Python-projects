const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');
const { getTranscript } = require('youtube-transcript-api');

// Function to extract video ID from YouTube URL
function extractVideoId(url) {
    const urlParams = new URLSearchParams(new URL(url).search);
    const videoId = urlParams.get('v');
    if (videoId) {
        return videoId;
    } else {
        throw new Error('Invalid YouTube URL. Unable to extract video ID.');
    }
}

// Function to fetch video title from YouTube page
async function getVideoTitle(videoId) {
    const youtubeUrl = `https://www.youtube.com/watch?v=${videoId}`;
    const response = await axios.get(youtubeUrl);
    const $ = cheerio.load(response.data);
    
    // Extract video title
    const titleTag = $('meta[property="og:title"]').attr('content');
    if (titleTag) {
        return titleTag;
    } else {
        throw new Error('Unable to extract video title from the YouTube page.');
    }
}

// Function to sanitize filename
function sanitizeFilename(title) {
    return title.replace(/[<>:"/\\|?*]/g, '');
}

// Function to save transcript to CSV
async function saveTranscriptToCsv(videoUrl) {
    try {
        // Extract video ID from URL
        const videoId = extractVideoId(videoUrl);
        
        // Fetch the video title
        const videoTitle = await getVideoTitle(videoId);
        const sanitizedTitle = sanitizeFilename(videoTitle);
        
        // Define the directory and file name
        const directory = 'Transcripts';
        if (!fs.existsSync(directory)) {
            fs.mkdirSync(directory);
        }
        const csvFilename = path.join(directory, `${sanitizedTitle}.csv`);
        
        // Fetch the transcript
        const transcript = await getTranscript(videoId);
        
        // Write transcript to CSV
        const csvLines = [
            'Start Time,End Time,Text',
            ...transcript.map(entry => `${entry.start},${entry.start + entry.duration},"${entry.text.replace(/"/g, '""')}"`)
        ].join('\n');
        
        fs.writeFileSync(csvFilename, csvLines, 'utf-8');
        
        console.log(`Transcript has been saved to ${csvFilename}`);
    } catch (error) {
        console.error(`An error occurred: ${error.message}`);
    }
}

// Replace with your YouTube video URL
const youtubeUrl = 'https://www.youtube.com/watch?v=H91aqUHn8sE&ab_channel=BeyondFireship';
saveTranscriptToCsv(youtubeUrl);
