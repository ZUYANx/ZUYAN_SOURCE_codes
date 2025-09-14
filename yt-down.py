import yt_dlp
import os

def download_video(url, output_path="downloads"):
    """Download YouTube video/audio"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Download options
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',  # Best quality
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Get URL from user
    url = input("Enter YouTube URL: ").strip()
    
    # Download the video
    download_video(url)
