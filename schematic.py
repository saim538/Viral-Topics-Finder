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

# YouTube API Key (Your API key)
API_KEY = "AIzaSyDmAp27l_1iZ2YVYZPxmvpnc5p_AcBN8rc"

# API URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit UI
st.set_page_config(layout="wide")  # Set layout to wide for responsiveness
st.title("YouTube Trending Video Finder")

# Date Range Selection
date_ranges = {
    "Last 7 days": 7,
    "Last 15 days": 15,
    "Last 30 days": 30,
    "Last 2 months": 60,
    "Last 3 months": 90,
    "Last 6 months": 180,
    "Last 1 year": 365,
    "Last 2 years": 730
}
selected_range = st.selectbox("Select Time Range:", list(date_ranges.keys()))

# User Inputs
keywords_input = st.text_area("Enter Keywords (comma-separated):", "")  # No default keywords
max_subscribers = st.text_input("Enter Max Subscribers:", "1000000")  # Default 1M, user can enter custom value

# Convert keywords into a list
keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

# Function to format numbers (YouTube-style)
def format_number(num):
    num = int(num)
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

# Fetch Data Button
if st.button("Fetch Data"):
    if not keywords:
        st.warning("⚠️ Please enter at least one keyword.")
    else:
        try:
            max_subs = int(max_subscribers)  # Convert input to integer

            # Calculate date range
            start_date = (datetime.utcnow() - timedelta(days=date_ranges[selected_range])).isoformat("T") + "Z"
            all_results = []

            for keyword in keywords:
                st.write(f"🔍 Searching for keyword: **{keyword}**")

                # Search videos
                search_params = {
                    "part": "snippet",
                    "q": keyword,
                    "type": "video",
                    "order": "viewCount",
                    "publishedAfter": start_date,
                    "maxResults": 16,  # Fetch more results for grid
                    "key": API_KEY,
                }
                response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
                data = response.json()

                if "items" not in data or not data["items"]:
                    st.warning(f"⚠️ No videos found for: {keyword}")
                    continue

                video_ids = [video["id"]["videoId"] for video in data["items"]]
                channel_ids = [video["snippet"]["channelId"] for video in data["items"]]

                # Get video statistics
                stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
                stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params).json()

                # Get channel statistics
                channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
                channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params).json()

                if "items" not in stats_response or "items" not in channel_response:
                    st.warning(f"⚠️ Failed to fetch stats for: {keyword}")
                    continue

                stats = stats_response["items"]
                channels = {ch["id"]: ch["statistics"] for ch in channel_response["items"]}

                # Collect results
                for video, stat in zip(data["items"], stats):
                    channel_id = video["snippet"]["channelId"]
                    subs = int(channels.get(channel_id, {}).get("subscriberCount", 0))

                    if subs < max_subs:
                        views = int(stat["statistics"].get("viewCount", 0))

                        all_results.append({
                            "Title": video["snippet"]["title"],
                            "Description": video["snippet"]["description"][:100],  # Short description
                            "Video ID": video["id"]["videoId"],
                            "URL": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                            "Views": format_number(views),
                            "Subscribers": format_number(subs),
                            "Thumbnail": video["snippet"]["thumbnails"]["medium"]["url"]
                        })

            # Display results in a grid (4 per row)
            if all_results:
                st.success(f"✅ Found {len(all_results)} trending videos!")
                cols = st.columns(4)  # Create 4 columns per row
                
                for index, result in enumerate(all_results):
                    with cols[index % 4]:  # Arrange videos in 4-column grid
                        st.image(result["Thumbnail"], width=300)
                        st.markdown(f"**[{result['Title']}]({result['URL']})**", unsafe_allow_html=True)
                        st.markdown(f"👁 **Views:** {result['Views']} &nbsp; 📢 **Subscribers:** {result['Subscribers']}")
                        st.write("---")

            else:
                st.warning(f"⚠️ No results found for channels with fewer than {max_subs} subscribers.")

        except ValueError:
            st.error("❌ Invalid input for max subscribers. Please enter a number.")
        except Exception as e:
            st.error(f"❌ Error: {e}")



