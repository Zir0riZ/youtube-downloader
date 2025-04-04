import os
from yt_dlp import YoutubeDL

def download_playlists(txt_file):
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
        'keepvideo': False,
    }

    with open(txt_file, 'r', encoding='utf-8') as file:
        playlist_urls = [line.strip() for line in file if line.strip()]

    for url in playlist_urls:
        try:
            if "watch?v=" in url and "&list=" in url:
                playlist_id = url.split('&list=')[1].split('&')[0]
                url = f"https://www.youtube.com/playlist?list={playlist_id}"
                print(f"Converted URL to: {url}")

            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                playlist_title = info.get('title', 'Unknown Playlist')
                print(f"\nDownloading playlist: {playlist_title}")

                if 'entries' not in info or not info['entries']:
                    print("Error: No entries found in playlist data!")
                    continue

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
                        print(f"Skipping {video_title}: No video ID found")
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
            print(f"Error processing playlist {url}: {str(e)}")
            continue

if __name__ == "__main__":
    txt_file_name = "playlists.txt"
    if not os.path.exists(txt_file_name):
        print(f"Error: {txt_file_name} not found!")
    else:
        download_playlists(txt_file_name)