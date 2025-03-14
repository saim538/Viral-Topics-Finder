import streamlit as st

import requests

from datetime import datetime, timedelta


# YouTube API Key

API_KEY = "AIzaSyDmAp27l_1iZ2YVYZPxmvpnc5p_AcBN8rc"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"


# Streamlit App Title

st.title("YouTube Viral Topics Tool")


# Input Fields

days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)


# List of broader keywords

keywords = [

  "car"
]


# Fetch Data Button

if st.button("Fetch Data"):

    try:

        # Calculate date range

        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"

        all_results = []


        # Iterate over the list of keywords

        for keyword in keywords:

            st.write(f"Searching for keyword: {keyword}")


            # Define search parameters

            search_params = {

                "part": "snippet",

                "q": keyword,

                "type": "video",

                "order": "viewCount",

                "publishedAfter": start_date,

                "maxResults": 5,

                "key": API_KEY,

            }


            # Fetch video data

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)

            data = response.json()


            # Check if "items" key exists

            if "items" not in data or not data["items"]:

                st.warning(f"No videos found for keyword: {keyword}")

                continue


            videos = data["items"]

            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]

            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]


            if not video_ids or not channel_ids:

                st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")

                continue


            # Fetch video statistics

            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}

            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)

            stats_data = stats_response.json()


            if "items" not in stats_data or not stats_data["items"]:

                st.warning(f"Failed to fetch video statistics for keyword: {keyword}")

                continue


            # Fetch channel statistics

            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}

            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)

            channel_data = channel_response.json()


            if "items" not in channel_data or not channel_data["items"]:

                st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")

                continue


            stats = stats_data["items"]

            channels = channel_data["items"]


            # Collect results

            for video, stat, channel in zip(videos, stats, channels):

                title = video["snippet"].get("title", "N/A")

                description = video["snippet"].get("description", "")[:200]

                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"

                views = int(stat["statistics"].get("viewCount", 0))

                subs = int(channel["statistics"].get("subscriberCount", 0))


                if subs < 500000:  # Only include channels with fewer than 3,000 subscribers

                    all_results.append({

                        "Title": title,

                        "Description": description,

                        "URL": video_url,

                        "Views": views,

                        "Subscribers": subs

                    })


        # Display results

        if all_results:

            st.success(f"Found {len(all_results)} results across all keywords!")

            for result in all_results:

                st.markdown(

                    f"**Title:** {result['Title']}  \n"

                    f"**Description:** {result['Description']}  \n"

                    f"**URL:** [Watch Video]({result['URL']})  \n"

                    f"**Views:** {result['Views']}  \n"

                    f"**Subscribers:** {result['Subscribers']}"

                )

                st.write("---")

        else:

            st.warning("No results found for channels with fewer than 3,000 subscribers.")


    except Exception as e:

        st.error(f"An error occurred: {e}")



# import streamlit as st
# import requests
# from datetime import datetime, timedelta

# # YouTube API Key
# API_KEY = "AIzaSyDmAp27l_1iZ2YVYZPxmvpnc5p_AcBN8rc"

# # YouTube API URLs
# YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
# YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
# YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# # Function to format numbers in K/M/B
# def format_count(number):
#     if number >= 1_000_000_000:
#         return f"{number / 1_000_000_000:.1f}B"
#     elif number >= 1_000_000:
#         return f"{number / 1_000_000:.1f}M"
#     elif number >= 1_000:
#         return f"{number / 1_000:.1f}K"
#     else:
#         return str(number)

# # Streamlit UI
# st.set_page_config(layout="wide")
# st.title("🔍 YouTube Video Search")

# # Search Bar
# query = st.text_input("Enter Search Keyword:", "")

# # Date Range Dropdown (Last 1 Day to Last 2 Years)
# date_options = {
#     "Last 1 Day": 1,
#     "Last 7 Days": 7,
#     "Last 30 Days": 30,
#     "Last 3 Months": 90,
#     "Last 6 Months": 180,
#     "Last 1 Year": 365,
#     "Last 2 Years": 730,
# }
# selected_range = st.selectbox("Filter by Date:", list(date_options.keys()))

# # Max Subscribers Input
# max_subscribers = st.number_input("Max Subscribers (Optional):", min_value=0, step=1000, value=0)

# # Video Length Filter
# video_length_filter = st.radio("Filter by Video Length:", ("All", "Shorts (<60s)", "Long (>=60s)"))

# # Calculate Date Range
# published_after = (datetime.utcnow() - timedelta(days=date_options[selected_range])).isoformat() + "Z"

# # Session state for pagination
# if "nextPageToken" not in st.session_state:
#     st.session_state.nextPageToken = None
# if "videos" not in st.session_state:
#     st.session_state.videos = []
# if "video_count" not in st.session_state:
#     st.session_state.video_count = 0

# # Function to fetch videos
# def fetch_videos(page_token=None):
#     if not query.strip():
#         return {"items": []}  # Prevent empty query error
    
#     params = {
#         "part": "snippet",
#         "q": query,
#         "maxResults": 50,
#         "type": "video",
#         "order": "viewCount",
#         "publishedAfter": published_after,
#         "key": API_KEY,
#         "videoDuration": "any",
#     }
#     if page_token:
#         params["pageToken"] = page_token
    
#     if video_length_filter == "Shorts (<60s)":
#         params["videoDuration"] = "short"
#     elif video_length_filter == "Long (>=60s)":
#         params["videoDuration"] = "long"
    
#     response = requests.get(YOUTUBE_SEARCH_URL, params=params).json()
#     return response

# # Search YouTube API
# if st.button("Search"):
#     st.session_state.videos = []  # Reset results
#     st.session_state.nextPageToken = None  # Reset pagination
#     st.session_state.video_count = 0  # Reset video count
#     response = fetch_videos()
#     st.session_state.videos.extend(response.get("items", []))
#     st.session_state.nextPageToken = response.get("nextPageToken", None)
#     st.session_state.video_count += len(response.get("items", []))
    
#     if not st.session_state.videos:
#         st.write("❌ No results found. Try adjusting filters or searching with a different keyword.")

# # Display results
# if st.session_state.videos:
#     st.markdown("""
#     <style>
#     .video-container {
#         display: flex;
#         flex-wrap: wrap;
#         gap: 20px;
#         justify-content: flex-start;
#         width: 100%;
#     }
#     .video-card {
#         width: 23%;
#         min-height: 300px;
#         border: 1px solid #ddd;
#         border-radius: 10px;
#         padding: 10px;
#         text-align: center;
#         background: #f9f9f9;
#     }
#     .video-card img {
#         width: 100%;
#         border-radius: 10px;
#     }
#     .video-title {
#         color: black;
#         margin: 10px 0;
#         font-weight: bold;
#         text-decoration: none;
#     }
#     </style>
#     <div class='video-container'>
#     """, unsafe_allow_html=True)
    
#     for item in st.session_state.videos:
#         vid = item["id"]["videoId"]
#         snippet = item["snippet"]
#         title = snippet["title"]
#         thumbnail = snippet["thumbnails"]["medium"]["url"]
        
#         st.markdown(f"""
#         <div class='video-card'>
#             <a href='https://www.youtube.com/watch?v={vid}' target='_blank'><img src='{thumbnail}'></a>
#             <p class='video-title'>{title}</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("</div>", unsafe_allow_html=True)
    
#     # Load More Button
#     if st.session_state.nextPageToken and st.session_state.video_count >= 200:
#         if st.button("Load More"):
#             response = fetch_videos(st.session_state.nextPageToken)
#             st.session_state.videos.extend(response.get("items", []))
#             st.session_state.nextPageToken = response.get("nextPageToken", None)
#             st.session_state.video_count += len(response.get("items", []))
            
#             if not response.get("items", []):
#                 st.write("❌ No more results found.")
