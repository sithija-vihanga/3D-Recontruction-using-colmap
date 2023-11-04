import cv2
import os

# List of video file paths
video_paths = ['vid04.mp4']  # Add more video paths as needed

# Create a directory to save the frames
output_folder = 'output_frames'
os.makedirs(output_folder, exist_ok=True)

# Frame capturing interval in seconds
frame_interval = 1

for video_path in video_paths:
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Frame count for unique frame filenames
    frame_count = 0

    while True:
        ret, frame = cap.read()

        # Break the loop if the video is over
        if not ret:
            break

        # Get the current frame count
        current_frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # Check if it's time to capture a frame (every 5 seconds)
        if current_frame_count % (frame_interval * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
            # Save the frame as an image
            frame_count += 1
            frame_filename = os.path.join(output_folder, f'video_{video_paths.index(video_path) + 1}_frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_filename, frame)
            print(f'Saved frame {frame_count} from {video_path} at {current_frame_count / cap.get(cv2.CAP_PROP_FPS):.2f} seconds')

    # Release the video capture object for the current video
    cap.release()

print('Frames sampling completed.')
