#videoRenderer.py

import subprocess
import threading
import queue
import numpy as np

class VideoRenderer(threading.Thread):
    def __init__(self, framerate, width, height, output_file):
        super().__init__()
        self.output_file = output_file
        self.frame_queue = queue.Queue(maxsize=120)  # ✅ Limit memory usage
        self.running = True

        # FFmpeg command
        ffmpeg_cmd = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-s', f'{width}x{height}',
            '-r', str(framerate),
            '-thread_queue_size', '512',  # ✅ Allow buffering
            '-i', 'pipe:0',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            self.output_file
        ]

        self.ffmpeg = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, bufsize=10**8)  
        self.start()  

    def run(self):
        """Thread loop: Sends frames to FFmpeg asynchronously."""
        while self.running or not self.frame_queue.empty():
            frame = self.frame_queue.get()  # ✅ Blocks until frame is available
            self.ffmpeg.stdin.write(frame)
            self.frame_queue.task_done()

    def send_frame(self, frame):
        """Queue a frame to be written to the video file asynchronously."""
        if self.running:
            try:
                self.frame_queue.put(frame, timeout=0.1)  # ✅ Drop frames if overloaded
            except queue.Full:
                print("⚠️ Frame dropped: FFmpeg is too slow!")

    def close(self):
        """Stops the thread and ensures FFmpeg finishes encoding."""
        self.running = False  
        self.frame_queue.join()  
        self.ffmpeg.stdin.close()
        self.ffmpeg.wait()  

    def __del__(self):
        print(f"Warning: VideoRenderer object deleted without explicit close(). Call .close() before exiting.")
