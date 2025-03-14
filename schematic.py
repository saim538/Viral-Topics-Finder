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

# Function to convert numbers to K/M/B format
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

# Search YouTube API
if st.button("Search"):
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 12,
        "type": "video",
        "order": "viewCount",
        "publishedAfter": published_after,
        "key": API_KEY,
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = response.json()

    if "items" in data:
        video_ids = [item["id"]["videoId"] for item in data["items"]]
        video_details_url = f"{YOUTUBE_VIDEO_URL}?part=statistics,snippet&id={','.join(video_ids)}&key={API_KEY}"
        video_response = requests.get(video_details_url).json()

        # Display Results in Grid (4 Videos Per Row)
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]

        for idx, video in enumerate(video_response.get("items", [])):
            vid = video["id"]
            snippet = video["snippet"]
            stats = video["statistics"]
            title = snippet["title"]
            thumbnail = snippet["thumbnails"]["medium"]["url"]
            views = format_count(int(stats.get("viewCount", 0)))

            # Get Channel Details
            channel_id = snippet["channelId"]
            channel_url = f"{YOUTUBE_CHANNEL_URL}?part=statistics&id={channel_id}&key={API_KEY}"
            channel_response = requests.get(channel_url).json()
            subscribers = format_count(int(channel_response["items"][0]["statistics"]["subscriberCount"]))

            # Filter by Max Subscribers
            if max_subscribers > 0 and int(channel_response["items"][0]["statistics"]["subscriberCount"]) > max_subscribers:
                continue  # Skip if channel has more subscribers than the filter

            # Display Video
            with cols[idx % 4]:
                st.image(thumbnail, use_column_width=True)
                st.write(f"**[{title}](https://www.youtube.com/watch?v={vid})**")
                st.write(f"👁️ {views} views | 📢 {subscribers} subscribers")

    else:
        st.write("❌ No results found.")


