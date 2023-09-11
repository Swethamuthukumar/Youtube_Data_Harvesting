import streamlit as st
import pymongo
from googleapiclient.discovery import build
from capstone_guvi import fetch_playlist_details, fetch_video_comments, fetch_channel_details


# Set your YouTube API key here
API_KEY = 'AIzaSyDUpGRI6l78mDDcvjKsuDrrHlcYKaWHriw'

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# MongoDB connection URI (replace with your actual MongoDB Atlas connection string)
MONGODB_URI = 'mongodb+srv://swethashruthi05:shruthi05@cluster0.ms1ivux.mongodb.net/?retryWrites=true&w=majority'

# Initialize MongoDB client and database
client = pymongo.MongoClient(MONGODB_URI)
db = client['youtube_data']


def store_data_in_mongodb(data, collection_name):
    try:
        # Get or create the specified collection
        collection = db[collection_name]

        # Insert the data into the collection
        inserted_id = collection.insert_one(data).inserted_id

        return inserted_id
    except Exception as e:
        st.error(f"An error occurred while storing data in MongoDB: {str(e)}")


# Streamlit web app title
st.title("YouTube Channel Data to MongoDB Atlas")

# Create a dropdown for users to select a YouTube Channel ID
channel_ids = ['UCKWaEZ-_VweaEx1j62do_vQ', 'UCzAF54cHk1ZO82af-8E3qOQ', 'UC7cs8q-gJRlGwj4A8OmCmXg',
               'UCtC_WTVuo9k3Zol0ZB6u5mQ','UCBwmMxybNva6P_5VmxjzwqA', 'UCb-8cJKS3MnAvK7eoYSehZw',
               'UCiYjpuUaSfkvdZkmtDU7JRw', 'UCWv7vMbMWH4-V0ZXdmDpPBA', 'UCOMG0iHHi27owoyxGvURxiQ',
               'UCcfngi7_ASuo5jdWX0bNauQ']  # Replace with your actual channel IDs
selected_channel_index = st.selectbox("Select a YouTube Channel:", range(len(channel_ids)))


# Check if the "Fetch Data" button is clicked
def fetch_videos_in_playlist(playlist_id):
    try:
        # Fetch videos in the playlist using the YouTube API
        videos_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=10  # Adjust as needed
        ).execute()

        # Extract the list of videos from the API response
        videos = videos_response.get('items', [])
        if videos is None:
            st.error("No videos found in the playlist.")
            return[] # Return an empty list if no vidio are found

        return videos
    except Exception as e:
        st.error(f"An error occurred while fetching videos in the playlist: {str(e)}")
        return []  # Return an empty list on error





if st.button("Fetch Data", key="fetch_data_button"):

    try:
        # Retrieve the selected channel ID
        channel_id = channel_ids[selected_channel_index]

        if not channel_id:
            st.warning("Please select a YouTube Channel ID.")
        else:
            # Retrieve channel data
            channel_details = fetch_channel_details(channel_id)

            # Store channel data in MongoDB
            store_data_in_mongodb(channel_details,'channel_details')

            st.write(f"Channel Name: {channel_details['snippet']['title']}")
            st.write(f"Subscriber Count: {channel_details['statistics']['subscriberCount']}")

            # Fetch and display playlists
            playlists = fetch_playlist_details(channel_id)
            if playlists:
                st.header("Playlists")
                for playlist in playlists:
                    st.write(f"Playlist Title: {playlist['snippet']['title']}")
                    st.write(f"Playlist ID: {playlist['id']}")

                    # Fetch and display video comments for each video in the playlist
                    videos = fetch_videos_in_playlist(playlist['id'])
                    for video in videos:
                        st.write(f"Video Title: {video['snippet']['title']}")
                        video_comments = fetch_video_comments(video['snippet']['resourceId']['videoId'])
                        for comment in video_comments:
                            st.write(f"Comment: {comment['snippet']['topLevelComment']['snippet']['textDisplay']}")
                            st.write(f"Author: {comment['snippet']['topLevelComment']['snippet']['authorDisplayName']}")
                            st.write(f"Published At: {comment['snippet']['topLevelComment']['snippet']['publishedAt']}")

        st.success("Data fetched and stored in MongoDB Atlas.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


        # Data Migration to SQL Database
        def create_sql_tables_and_insert_data(sql_cursor, transformed_data):
            pass


        def fetch_data_from_data_lake(channel_id):
            pass


        def transform_data(data_from_data_lake):
            pass


        if st.button("Migrate Data to SQL"):
            try:
                # Retrieve the selected channel ID
                channel_id = channel_ids[selected_channel_index]

                if not channel_id:
                    st.warning("Please select a YouTube Channel ID.")
                else:
                    # Fetch data from the data lake based on the selected channel (You need to implement this)
                    data_from_data_lake = fetch_data_from_data_lake(channel_id)

                    # Transform data if needed (You need to implement this)
                    transformed_data = transform_data(data_from_data_lake)

                    # Create SQL tables and insert data (You need to implement this)
                    create_sql_tables_and_insert_data(sql_cursor, transformed_data)

                    st.success("Data migrated to SQL database successfully.")

            except Exception as e:
                st.error(f"An error occurred during data migration to SQL: {str(e)}")

        # Close SQL connection
        sql_conn.close()



        

