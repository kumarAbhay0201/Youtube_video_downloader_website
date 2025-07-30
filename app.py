import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("🎬 YouTube Video & Audio Downloader")

url = st.text_input("Paste your YouTube video URL here")

def get_download_options(video_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        return info_dict

if st.button("Search"):
    if url:
        try:
            st.info("Fetching video data...")
            info = get_download_options(url)

            st.success(f"Title: {info['title']}")
            st.image(info.get("thumbnail", ""))
            st.markdown(f"**Duration:** {round(info['duration']/60, 2)} minutes")

            video_formats = [f for f in info['formats'] if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            audio_formats = [f for f in info['formats'] if f.get('vcodec') == 'none' and f.get('acodec') != 'none']

            st.subheader("📽️ Video Formats")
            for fmt in video_formats:
                label = f"{fmt.get('format_note', 'Unknown')} - {round(fmt['filesize']/1024/1024, 2) if fmt.get('filesize') else '?'} MB"
                url = fmt.get('url')
                st.markdown(f"[Download {label}]({url})", unsafe_allow_html=True)

            st.subheader("🎧 Audio Formats")
            for fmt in audio_formats:
                label = f"{fmt.get('abr', 'Unknown')} kbps - {round(fmt['filesize']/1024/1024, 2) if fmt.get('filesize') else '?'} MB"
                url = fmt.get('url')
                st.markdown(f"[Download MP3 ({label})]({url})", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please paste a valid URL.")

st.markdown("""
<meta name="description" content="Free YouTube Downloader: Download videos and MP3 from YouTube instantly. Fast, easy, no login required."/>
<meta name="keywords" content="YouTube downloader, download mp3, youtube to mp4, online downloader"/>
""", unsafe_allow_html=True)
