import itertools
import pymongo
import streamlit as st
from googleapiclient.discovery import build
from google.auth.exceptions import DefaultCredentialsError


# Set your YouTube API key here
API_KEY = 'AIzaSyDhIbzBcKkGD75Lux4bHJStXhZtn_Sm04o'

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# MongoDB connection URI (replace with your actual MongoDB Atlas connection string)
MONGODB_URI = 'mongodb+srv://Dhiya:nithya@cluster0.eetbpgj.mongodb.net/?retryWrites=true&w=majority'

# Initialize MongoDB client and database
client = pymongo.MongoClient(MONGODB_URI)
db = client['youtube_data']

def fetch_channel_details(channel_id):
    try:
        # Fetch channel details
        channel_response = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()
        return channel_response['items'][0]
    except Exception as e:
        st.error(f"An error occurred while fetching channel details: {str(e)}")

def fetch_playlist_details(channel_id):
    try:
        # Fetch playlists for the channel
        playlists_response = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=10  # Adjust as needed
        ).execute()
        return playlists_response['items']
    except Exception as e:
        st.error(f"An error occurred while fetching playlists: {str(e)}")

def fetch_video_comments(video_id):
    try:
        # Fetch video comments
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=10  # Adjust as needed
        ).execute()
        return comments_response['items']
    except Exception as e:
        st.error(f"An error occurred while fetching comments: {str(e)}")

# Streamlit web app title
st.title("YouTube Channel Data to MongoDB Atlas")

# Add a dropdown for users to select a YouTube Channel ID
channel_id = st.selectbox("Select a YouTube Channel ID:", ['CHANNEL_ID_1', 'CHANNEL_ID_2', 'CHANNEL_ID_3'])

# Check if the "Fetch Data" button is clicked
if st.button("Fetch Data"):
    if not channel_id:
        st.warning("Please select a YouTube Channel ID.")
    else:
        try:
            # Retrieve channel data
            channel_details = fetch_channel_details(channel_id)

            # Store channel data in MongoDB
            store_data_in_mongodb(channel_details, 'channel_details')

            st.write(f"Channel Name: {channel_details['snippet']['title']}")
            st.write(f"Subscriber Count: {channel_details['statistics']['subscriberCount']}")

            # Fetch and display playlists
            playlists = fetch_playlist_details(channel_id)
            if playlists:
                st.header("Playlists")
                for playlist in playlists:
                    st.write(f"Playlist Title: {playlist['snippet']['title']}")
                    st.write(f"Playlist ID: {playlist['id']}")

                    # Fetch and display video comments for each playlist
                    st.header(f"Comments for Playlist: {playlist['snippet']['title']}")
                    for video in playlist:
                        st.write(f"Video Title: {video['snippet']['title']}")
                        video_comments = fetch_video_comments(video['snippet']['resourceId']['videoId'])
                        for comment in video_comments:
                            st.write(f"Comment: {comment['snippet']['topLevelComment']['snippet']['textDisplay']}")
                            st.write(f"Author: {comment['snippet']['topLevelComment']['snippet']['authorDisplayName']}")
                            st.write(f"Published At: {comment['snippet']['topLevelComment']['snippet']['publishedAt']}")

            st.success("Data fetched and stored in MongoDB Atlas.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")






