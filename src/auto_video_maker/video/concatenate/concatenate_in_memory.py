#!/usr/bin/python3


from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_in_memory(video_paths, output_path):
    """
    Concatenates multiple video files into a single video file while managing memory efficiently.

    Parameters:
    video_paths (list of str): A list of file paths to the video files that need to be concatenated.
    output_path (str): The file path where the final concatenated video will be saved.

    Note:
    - When the input videos have different resolutions (width and height), 
      the `concatenate_videoclips` function will raise an exception. 
      To avoid this issue, it is advisable to resize all videos to a 
      common resolution before concatenation. This can be accomplished 
      by using the `resize` method from the `VideoFileClip` class to ensure 
      that all clips are of the same size.
    - This method spend a lot of memory but is speed.

    Example:
    video_paths = ['video1.mp4', 'video2.mp4', 'video3.mp4']
    output_path = 'final_video.mp4'
    concat_videos_memory(video_paths, output_path)
    """
    # Agora, carregamos os vídeos temporários e concatenamos
    final_clips = [VideoFileClip(video) for video in video_paths]
    final_video = concatenate_videoclips(final_clips)

    # Exporta o vídeo final
    final_video.write_videofile(output_path)
