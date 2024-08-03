import csv
import re
import os
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    else:
        raise ValueError("Invalid YouTube URL. Unable to extract video ID.")

def get_video_title(video_id):
    youtube_url = f'https://www.youtube.com/watch?v={video_id}'
    response = requests.get(youtube_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract video title
    title_tag = soup.find('meta', property='og:title')
    if title_tag:
        return title_tag['content']
    else:
        raise ValueError("Unable to extract video title from the YouTube page.")

def sanitize_filename(title):
    # Remove invalid characters for file names
    return re.sub(r'[<>:"/\\|?*]', '', title)

def save_transcript_to_csv(video_url):
    try:
        # Extract video ID from URL
        video_id = extract_video_id(video_url)
        
        # Fetch the video title
        video_title = get_video_title(video_id)
        sanitized_title = sanitize_filename(video_title)
        
        # Define the directory and file name
        directory = 'Transcripts'
        os.makedirs(directory, exist_ok=True)  # Create the directory if it does not exist
        csv_filename = os.path.join(directory, f'{sanitized_title}.csv')
        
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Write transcript to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Start Time', 'End Time', 'Text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in transcript:
                writer.writerow({
                    'Start Time': entry['start'],
                    'End Time': entry['start'] + entry['duration'],
                    'Text': entry['text']
                })
        
        print(f"Transcript has been saved to {csv_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your YouTube video URL
youtube_url = 'https://www.youtube.com/watch?v=H91aqUHn8sE&ab_channel=BeyondFireship'
save_transcript_to_csv(youtube_url)
