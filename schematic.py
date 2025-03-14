# import streamlit as st

# import requests

# from datetime import datetime, timedelta


# # YouTube API Key

# API_KEY = "AIzaSyDmAp27l_1iZ2YVYZPxmvpnc5p_AcBN8rc"

# YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

# YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"


# # Streamlit App Title

# st.title("YouTube Viral Topics Tool")


# # Input Fields

# days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)


# # List of broader keywords

# keywords = [

#   "SaaS Billing", "SaaS Pricing", 
#   "SaaS Subscription Management", 
#   "Pricing Strategy for SaaS", 
#   "SaaS Monetization", "B2B SaaS Pricing", 
#   "Automated Billing System", 
#   "Automated SaaS Billing System", 
#   "Best Billing Software for SaaS", 
#   "B2B SaaS Billing", "SaaS Billing System", 
#   "SaaS Invoicing", "B2B SaaS Payments", 
#   "SaaS Billing Software", "SaaS Billing Models", 
#   "SaaS Billing Platforms", "SaaS Subscription Billing", 
#   "Best SaaS Billing Software", "SaaS Pricing Strategy", 
#   "Software as a Service Pricing Models", "SaaS"
# ]


# # Fetch Data Button

# if st.button("Fetch Data"):

#     try:

#         # Calculate date range

#         start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"

#         all_results = []


#         # Iterate over the list of keywords

#         for keyword in keywords:

#             st.write(f"Searching for keyword: {keyword}")


#             # Define search parameters

#             search_params = {

#                 "part": "snippet",

#                 "q": keyword,

#                 "type": "video",

#                 "order": "viewCount",

#                 "publishedAfter": start_date,

#                 "maxResults": 5,

#                 "key": API_KEY,

#             }


#             # Fetch video data

#             response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)

#             data = response.json()


#             # Check if "items" key exists

#             if "items" not in data or not data["items"]:

#                 st.warning(f"No videos found for keyword: {keyword}")

#                 continue


#             videos = data["items"]

#             video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]

#             channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]


#             if not video_ids or not channel_ids:

#                 st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")

#                 continue


#             # Fetch video statistics

#             stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}

#             stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)

#             stats_data = stats_response.json()


#             if "items" not in stats_data or not stats_data["items"]:

#                 st.warning(f"Failed to fetch video statistics for keyword: {keyword}")

#                 continue


#             # Fetch channel statistics

#             channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}

#             channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)

#             channel_data = channel_response.json()


#             if "items" not in channel_data or not channel_data["items"]:

#                 st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")

#                 continue


#             stats = stats_data["items"]

#             channels = channel_data["items"]


#             # Collect results

#             for video, stat, channel in zip(videos, stats, channels):

#                 title = video["snippet"].get("title", "N/A")

#                 description = video["snippet"].get("description", "")[:200]

#                 video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"

#                 views = int(stat["statistics"].get("viewCount", 0))

#                 subs = int(channel["statistics"].get("subscriberCount", 0))


#                 if subs < 5000:  # Only include channels with fewer than 3,000 subscribers

#                     all_results.append({

#                         "Title": title,

#                         "Description": description,

#                         "URL": video_url,

#                         "Views": views,

#                         "Subscribers": subs

#                     })


#         # Display results

#         if all_results:

#             st.success(f"Found {len(all_results)} results across all keywords!")

#             for result in all_results:

#                 st.markdown(

#                     f"**Title:** {result['Title']}  \n"

#                     f"**Description:** {result['Description']}  \n"

#                     f"**URL:** [Watch Video]({result['URL']})  \n"

#                     f"**Views:** {result['Views']}  \n"

#                     f"**Subscribers:** {result['Subscribers']}"

#                 )

#                 st.write("---")

#         else:

#             st.warning("No results found for channels with fewer than 3,000 subscribers.")


#     except Exception as e:

#         st.error(f"An error occurred: {e}")




import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyDmAp27l_1iZ2YVYZPxmvpnc5p_AcBN8rc"

# YouTube API URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Function to format numbers in K/M/B
def format_count(number):
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

# Streamlit UI
st.title("🔍 YouTube Video Search")

# Search Bar
query = st.text_input("Enter Search Keyword:", "")

# Date Range Dropdown (Last 1 Day to Last 2 Years)
date_options = {
    "Last 1 Day": 1,
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last 3 Months": 90,
    "Last 6 Months": 180,
    "Last 1 Year": 365,
    "Last 2 Years": 730,
}
selected_range = st.selectbox("Filter by Date:", list(date_options.keys()))

# Max Subscribers Input
max_subscribers = st.number_input("Max Subscribers (Optional):", min_value=0, step=1000, value=0)

# Calculate Date Range
published_after = (datetime.utcnow() - timedelta(days=date_options[selected_range])).isoformat() + "Z"

# Session state for pagination
if "nextPageToken" not in st.session_state:
    st.session_state.nextPageToken = None
if "videos" not in st.session_state:
    st.session_state.videos = []
if "video_count" not in st.session_state:
    st.session_state.video_count = 0

# Function to fetch videos
def fetch_videos(page_token=None):
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 50,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": published_after,
        "key": API_KEY,
    }
    if page_token:
        params["pageToken"] = page_token
    
    response = requests.get(YOUTUBE_SEARCH_URL, params=params).json()
    return response

# Search YouTube API
if st.button("Search"):
    st.session_state.videos = []  # Reset results
    st.session_state.nextPageToken = None  # Reset pagination
    st.session_state.video_count = 0  # Reset video count
    response = fetch_videos()
    st.session_state.videos.extend(response.get("items", []))
    st.session_state.nextPageToken = response.get("nextPageToken", None)
    st.session_state.video_count += len(response.get("items", []))
    
    if not st.session_state.videos:
        st.write("❌ No results found.")

# Display results
if st.session_state.videos:
    cols = st.columns(4)
    
    for idx, item in enumerate(st.session_state.videos):
        vid = item["id"]["videoId"]
        snippet = item["snippet"]
        title = snippet["title"]
        thumbnail = snippet["thumbnails"]["medium"]["url"]
        
        # Get video details
        video_details_url = f"{YOUTUBE_VIDEO_URL}?part=statistics,snippet&id={vid}&key={API_KEY}"
        video_response = requests.get(video_details_url).json()
        stats = video_response.get("items", [{}])[0].get("statistics", {})
        views = format_count(int(stats.get("viewCount", 0)))
        
        # Get channel details
        channel_id = snippet["channelId"]
        channel_url = f"{YOUTUBE_CHANNEL_URL}?part=statistics&id={channel_id}&key={API_KEY}"
        channel_response = requests.get(channel_url).json()
        subscribers = format_count(int(channel_response.get("items", [{}])[0].get("statistics", {}).get("subscriberCount", 0)))
        
        # Filter by Max Subscribers
        if max_subscribers > 0 and int(channel_response.get("items", [{}])[0].get("statistics", {}).get("subscriberCount", 0)) > max_subscribers:
            continue
        
        with cols[idx % 4]:
            with st.container():
                st.image(thumbnail, use_container_width=True)
                st.write(f"**[{title}](https://www.youtube.com/watch?v={vid})**")
                st.write(f"👁️ {views} views | 📢 {subscribers} subscribers")
                st.markdown("---")
    
    # Load More Button (First after 200 videos, then in batches of 200)
    if st.session_state.nextPageToken and st.session_state.video_count >= 200:
        if st.button("Load More"):
            response = fetch_videos(st.session_state.nextPageToken)
            st.session_state.videos.extend(response.get("items", []))
            st.session_state.nextPageToken = response.get("nextPageToken", None)
            st.session_state.video_count += len(response.get("items", []))
            
            if not response.get("items", []):
                st.write("❌ No more results found.")
