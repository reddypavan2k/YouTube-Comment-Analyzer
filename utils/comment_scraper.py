import re
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    # Handle different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/watch\?.*&v=)([^#\&\?\n]+)',
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_service():
    """Build and return an authorized YouTube Data API v3 service"""
    # You need to enable YouTube Data API v3 and get an API key
    # from Google Cloud Console: https://console.cloud.google.com/
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key not found in environment variables")
    
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_video_comments(video_url, max_results=1000):
    """
    Fetch comments from a YouTube video
    
    Args:
        video_url (str): URL of the YouTube video
        max_results (int): Maximum number of comments to fetch
        
    Returns:
        pandas.DataFrame: DataFrame containing comments and metadata
    """
    try:
        # Extract video ID from URL
        video_id = extract_video_id(video_url)
        if not video_id:
            raise ValueError("Could not extract video ID from URL")
        
        # Initialize YouTube API client
        youtube = get_youtube_service()
        
        # Get video details to verify video exists
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        
        if not video_response.get('items'):
            raise ValueError("Video not found or comments disabled")
        
        # Check if comments are disabled
        video_details = video_response['items'][0]
        if 'commentCount' not in video_details['statistics']:
            raise ValueError("Comments are disabled for this video")
        
        comments = []
        next_page_token = None
        
        # Fetch comments in pages
        while True:
            try:
                response = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),  # YouTube API max is 100
                    pageToken=next_page_token,
                    textFormat='plainText',
                    order='relevance'  # 'time' for newest first, 'relevance' for most relevant
                ).execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment['likeCount'],
                        'published_at': comment['publishedAt'],
                        'updated_at': comment['updatedAt'],
                        'comment_id': item['id']
                    })
                    
                    # Check if we've reached the maximum number of comments
                    if len(comments) >= max_results:
                        break
                
                # Check if we've reached the maximum number of comments or no more pages
                if 'nextPageToken' in response and len(comments) < max_results:
                    next_page_token = response['nextPageToken']
                else:
                    break
                    
            except HttpError as e:
                error_json = e.content.decode('utf-8')
                if 'commentsDisabled' in error_json:
                    raise ValueError("Comments are disabled for this video")
                elif 'videoNotFound' in error_json:
                    raise ValueError("Video not found")
                else:
                    raise
        
        # Convert to DataFrame
        if not comments:
            return pd.DataFrame()
            
        df = pd.DataFrame(comments)
        df['published_at'] = pd.to_datetime(df['published_at'])
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        
        return df
    
    except Exception as e:
        print(f"Error fetching comments: {str(e)}")
        return None
