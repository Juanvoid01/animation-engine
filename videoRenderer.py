import subprocess
import threading
import queue

class VideoRenderer(threading.Thread):
    def __init__(self, framerate, width, height, output_file):
        super().__init__()
        self.output_file = output_file
        self.frame_queue = queue.Queue()  # Thread-safe queue for frames
        self.running = True  # Controls the thread loop

        # FFmpeg command
        ffmpeg_cmd = [
            'ffmpeg',
            '-y',  # Overwrite existing file
            '-f', 'rawvideo',  # Raw input format
            '-pix_fmt', 'rgb24',  # 24-bit RGB
            '-s', f'{width}x{height}',  # Frame size
            '-r', str(framerate),  # Frame rate
            '-i', 'pipe:0',  # Read input from stdin
            '-c:v', 'libx264',  # Encode using H.264
            '-preset', 'ultrafast',  # Faster encoding
            '-crf', '23',  # Quality (lower is better, 17-28 range)
            '-pix_fmt', 'yuv420p',  # Required for compatibility
            self.output_file  # Output file
        ]

        self.ffmpeg = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, bufsize=10**8)  
        self.start()  # Start the thread

    def run(self):
        """Thread loop: Sends frames to FFmpeg asynchronously."""
        while self.running or not self.frame_queue.empty():
            try:
                frame = self.frame_queue.get(timeout=1)  # Wait for a frame
                self.ffmpeg.stdin.write(frame)  # Send frame to FFmpeg
                self.frame_queue.task_done()
            except queue.Empty:
                continue  # No frame, keep waiting

    def send_frame(self, frame):
        """Queue a frame to be written to the video file asynchronously."""
        if self.running:
            self.frame_queue.put(frame)  

    def close(self):
        """Stops the thread and ensures FFmpeg finishes encoding."""
        self.running = False  # Stop accepting new frames
        self.frame_queue.join()  # Wait for all frames to be processed
        self.ffmpeg.stdin.close()
        self.ffmpeg.wait()  # Ensure FFmpeg completes encoding

    def __del__(self):
        self.close()  # Ensure cleanup on object deletion
