import os
from yt_dlp import YoutubeDL

def download_single_video(video_url):
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'progress': True,
        'ignoreerrors': True,
        'nooverwrites': False,
        'continuedl': True,
        'retries': 3,
        'keepvideo': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"\nDownloading single video: {video_url}")
            video_info = ydl.extract_info(video_url, download=False)
            video_title = video_info.get('title', 'Untitled')
            video_path = f"{video_title}.mp4"
            expected_size = video_info.get('filesize_approx') or video_info.get('filesize')

            if os.path.exists(video_path):
                current_size = os.path.getsize(video_path)
                if expected_size and current_size >= expected_size:
                    print(f"Skipping: {video_title} (complete, size: {current_size} bytes)")
                    return
                else:
                    print(f"Resuming: {video_title} (incomplete, current: {current_size}, expected: {expected_size} bytes)")
            else:
                print(f"Starting: {video_title}")

            ydl.download([video_url])
            
            if os.path.exists(video_path):
                final_size = os.path.getsize(video_path)
                if expected_size and final_size >= expected_size:
                    print(f"Finished: {video_title}")
                else:
                    print(f"Warning: {video_title} incomplete (final: {final_size}, expected: {expected_size} bytes)")
            else:
                print(f"Error: {video_title} download failed")
        
        except Exception as e:
            print(f"Error downloading {video_url}: {str(e)}")

def download_playlist(playlist_url):
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': os.path.join('%(folder_name)s', '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'progress': True,
        'ignoreerrors': True,
        'nooverwrites': False,
        'continuedl': True,
        'retries': 3,
        'keepvideo': True,
    }

    try:
        if "watch?v=" in playlist_url and "&list=" in playlist_url:
            playlist_id = playlist_url.split('&list=')[1].split('&')[0]
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            print(f"Converted URL to: {playlist_url}")

        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            playlist_title = info.get('title', 'Unknown Playlist')
            print(f"\nDownloading playlist: {playlist_title}")

            if 'entries' not in info or not info['entries']:
                print("Error: No entries found in playlist!")
                return
            
            print(f"Total videos: {len(info['entries'])}")
            folder_name = ''.join(c for c in playlist_title if c.isalnum() or c in ' -_').strip() or "Playlist"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

        ydl_opts['outtmpl'] = os.path.join(folder_name, '%(title)s.%(ext)s')

        with YoutubeDL(ydl_opts) as ydl:
            for index, entry in enumerate(info['entries'], 1):
                if not entry:
                    print(f"Skipping item {index}: Invalid entry")
                    continue
                
                video_title = entry.get('title', 'Untitled')
                video_id = entry.get('id')
                if not video_id:
                    print(f"Skipping {video_title}: No video ID")
                    continue
                
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_path = os.path.join(folder_name, f"{video_title}.mp4")
                expected_size = entry.get('filesize_approx') or entry.get('filesize')

                if os.path.exists(video_path):
                    current_size = os.path.getsize(video_path)
                    if expected_size and current_size >= expected_size:
                        print(f"Skipping: {video_title} (complete, size: {current_size} bytes)")
                        continue
                    else:
                        print(f"Resuming: {video_title} (incomplete, current: {current_size}, expected: {expected_size} bytes)")
                else:
                    print(f"Starting: {video_title}")

                ydl.download([video_url])
                
                if os.path.exists(video_path):
                    final_size = os.path.getsize(video_path)
                    if expected_size and final_size >= expected_size:
                        print(f"Finished: {video_title} (item {index} of {len(info['entries'])})")
                    else:
                        print(f"Warning: {video_title} incomplete (final: {final_size}, expected: {expected_size} bytes)")
                else:
                    print(f"Error: {video_title} download failed")
        
        print(f"Finished downloading playlist: {playlist_title}\n")
        
    except Exception as e:
        print(f"Error processing playlist {playlist_url}: {str(e)}")

def main():
    print("Choose an option:")
    print("1 - Download a single video")
    print("2 - Download a playlist")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice! Please enter 1 or 2.")

    if choice == '1':
        video_url = input("Enter the video URL: ").strip()
        if video_url:
            download_single_video(video_url)
        else:
            print("Error: No URL provided!")
    
    elif choice == '2':
        playlist_url = input("Enter the playlist URL: ").strip()
        if playlist_url:
            download_playlist(playlist_url)
        else:
            print("Error: No URL provided!")

if __name__ == "__main__":
    main()