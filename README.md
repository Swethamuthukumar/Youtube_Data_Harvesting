Hi 👋, I'm Deepika

# Youtube_Data_Harvesting_and_Warehousing
## Domain : Social Media 💻
### Problem Statement :
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. Extracting data using Youtube API and storing it on MongoDB then Transforming it to a relational database like MySQL. For getting various info about youtube channels.

#### Technologies used :
👨‍💻 Python 
👨‍💻 MongoDB
👨‍💻 MySQL
👨‍💻 YouTube Data API
👨‍💻 Streamlit
👨‍💻 Pandas

##### OVERVIEW :
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a MongoDB database, migrates it to a SQL data warehouse, and enables users to search for channel details and join tables to view data in the Streamlit app.
Overall, this script provides a way to fetch YouTube channel data, store it in MongoDB, and migrate it to a SQL database using a Streamlit application for user interaction.

##### STEPS FOLLOWED:
📝 Create the streamlit dashboard : Using Streamlit library create the dashboard as per the requirement, go through documentation to learn more on streamlit. https://docs.streamlit.io/library/api-reference/performance/st.cache_data

📝 Set up YouTube API access : Enable the YouTube Data API in Google Developers console and obtain API credentials, go through documentation to learn more on how to extract data using API https://developers.google.com/youtube/v3/docs

📝 Scrape the YouTube data : Using google-api-python-client library, extract the youtube channel, playlist, videos and comments details.

📝 Store the data in MongoDB : Create the database and collections to Store the extracted data in MongoDB

📝 Migrate the data from MongoDb to SQL : Based on specific data create the tables, use mysql.connector to establish connection with MySQL 
            ✔ After collected data for multiple channels,it is then migrated/transformed it to a structured MySQL as data warehouse.

📝 Finally, the migrated data is displayed in the Streamlit app.
