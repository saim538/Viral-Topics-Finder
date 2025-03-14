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

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# User Inputs
days = st.number_input("Enter Days to Search (1-180):", min_value=1, max_value=180, value=30)
keywords_input = st.text_area("Enter Keywords (comma-separated):", "")
subscriber_limit = st.number_input("Enter Max Subscriber Count to Filter:", min_value=1, value=5000)

# Convert keywords into a list
keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

# Fetch Data Button
if st.button("Fetch Data"):
    if not keywords:
        st.warning("Please enter at least one keyword.")
    else:
        try:
            # Calculate date range
            start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
            all_results = []

            # Iterate over the list of keywords
            for keyword in keywords:
                st.write(f"🔍 Searching for keyword: **{keyword}**")

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

                if "items" not in data or not data["items"]:
                    st.warning(f"⚠️ No videos found for keyword: {keyword}")
                    continue

                videos = data["items"]
                video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
                channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

                if not video_ids or not channel_ids:
                    st.warning(f"⚠️ Skipping keyword: {keyword} due to missing video/channel data.")
                    continue

                # Fetch video statistics
                stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
                stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
                stats_data = stats_response.json()

                if "items" not in stats_data or not stats_data["items"]:
                    st.warning(f"⚠️ Failed to fetch video statistics for keyword: {keyword}")
                    continue

                # Fetch channel statistics
                channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
                channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
                channel_data = channel_response.json()

                if "items" not in channel_data or not channel_data["items"]:
                    st.warning(f"⚠️ Failed to fetch channel statistics for keyword: {keyword}")
                    continue

                stats = stats_data["items"]
                channels = channel_data["items"]

                # Collect results
                for video, stat, channel in zip(videos, stats, channels):
                    title = video["snippet"].get("title", "N/A")
                    description = video["snippet"].get("description", "")[:200]
                    video_id = video["id"]["videoId"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    views = int(stat["statistics"].get("viewCount", 0))
                    subs = int(channel["statistics"].get("subscriberCount", 0))

                    if subs < subscriber_limit:  # Filter by user-defined subscriber count
                        all_results.append({
                            "Title": title,
                            "Description": description,
                            "Video ID": video_id,
                            "URL": video_url,
                            "Views": views,
                            "Subscribers": subs
                        })

            # Display results
            if all_results:
                st.success(f"✅ Found {len(all_results)} results across all keywords!")

                for result in all_results:
                    st.subheader(f"🎬 {result['Title']}")
                    st.video(f"https://www.youtube.com/watch?v={result['Video ID']}")
                    st.markdown(
                        f"**📌 Description:** {result['Description']}  \n"
                        f"**👁 Views:** {result['Views']}  \n"
                        f"**📢 Subscribers:** {result['Subscribers']}  \n"
                        f"🔗 [Watch on YouTube]({result['URL']})"
                    )
                    st.write("---")

            else:
                st.warning(f"⚠️ No results found for channels with fewer than {subscriber_limit} subscribers.")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")


