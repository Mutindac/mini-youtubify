import subprocess
import os
import shutil
FFMPEG_PATH = shutil.which("ffmpeg") or "ffmpeg"

def process_video(input_path, output_path):
    try:
        # Use ffmpeg to convert the video to a standard format
        command = [
            FFMPEG_PATH,
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '22',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True)
        print(f"Video processed successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video: {e}")
        print(e.stderr.decode())
    
def generate_thumbnail(input_path, thumbnail_path):
    try:
        # Using ffmpeg to generate a thumbnail from the video
        command = [
            FFMPEG_PATH,
            '-i', input_path,
            '-ss', '00:00:01.000',
            '-vframes', '1',
            thumbnail_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,check=True)
        print(f"Thumbnail generated successfully: {thumbnail_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating thumbnail: {e}")
        print(e.stderr.decode())
        
#hls conversion
def convert_to_hls(input_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        # folders for resolutions
        p1080 = os.path.join(output_dir, "1080p")
        p720 = os.path.join(output_dir, "720p")
        p480 = os.path.join(output_dir, "480p")

        os.makedirs(p1080, exist_ok=True)
        os.makedirs(p720, exist_ok=True)
        os.makedirs(p480, exist_ok=True)

        # 1080p
        subprocess.run([
            FFMPEG_PATH,
            "-i", input_path,
            "-vf", "scale=1920:1080",
            "-c:v", "libx264",
            "-b:v", "5000k",
            "-c:a", "aac",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls",
            os.path.join(p1080, "index.m3u8")
        ], check=True)

        # 720p
        subprocess.run([
            FFMPEG_PATH,
            "-i", input_path,
            "-vf", "scale=1280:720",
            "-c:v", "libx264",
            "-b:v", "2800k",
            "-c:a", "aac",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls",
            os.path.join(p720, "index.m3u8")
        ], check=True)

        # 480p
        subprocess.run([
            FFMPEG_PATH,
            "-i", input_path,
            "-vf", "scale=854:480",
            "-c:v", "libx264",
            "-b:v", "1400k",
            "-c:a", "aac",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls",
            os.path.join(p480, "index.m3u8")
        ], check=True)

        # MASTER playlist 
        master_path = os.path.join(output_dir, "master.m3u8")

        with open(master_path, "w") as f:
            f.write("#EXTM3U\n")
            f.write("#EXT-X-VERSION:3\n\n")

            f.write("#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\n")
            f.write("1080p/index.m3u8\n\n")

            f.write("#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720\n")
            f.write("720p/index.m3u8\n\n")

            f.write("#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=854x480\n")
            f.write("480p/index.m3u8\n\n")

        return master_path

    except subprocess.CalledProcessError as e:
        print("HLS error:", e)
        print(e.stderr.decode())
        return None