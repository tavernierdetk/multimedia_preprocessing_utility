import time

import ffmpeg
import datetime
import os

class Recorder:
    def __init__(self, file_path, segment_length=60, output_format=".mp4", output_codec=""):
        self.file_path = file_path
        self.segment_length = segment_length
        self.output_format = output_format

        return

    def start_recording(self, program):
        program_path = f"{file_path}/{program['channel']}/{program['program_name']}"
        now = datetime.datetime.now()
        end = now + datetime.timedelta(seconds=program['duration'])
        timespan = f"{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}-{str(now.hour).zfill(2)}{str(now.minute).zfill(2)}-{str(end.hour).zfill(2)}{str(end.minute).zfill(2)}"
        recording_name = f"{program['channel']}_{program['program_name']}_{timespan}"
        os.mkdir(f"{program_path}/{recording_name}")

        for i in range(0,int(program["duration"]/self.segment_length) ):

            input_ffmpeg = ffmpeg.input(program["stream_link"], to=self.segment_length)
            # Refer to the master audio, video and subtitles streams separately.
            input_video = input_ffmpeg['v']
            input_audio = input_ffmpeg['a']

            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, f"{program_path}/{recording_name}/{recording_name}-{i}{self.output_format}",
                vcodec='copy', acodec='copy'
            )

            # If the destination file already exists, overwrite it.
            output_ffmpeg = ffmpeg.overwrite_output(output_ffmpeg)


            ffmpeg.run(output_ffmpeg)


program = {
    "stream_link" : "https://rcavlive.akamaized.net/hls/live/704025/xcanrdi/master.m3u8",
    "channel": "RDI-TV-Q3456752",
    "program_name": "telejournal",
    "duration": 600
}

file_path = '/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles/Streams'

recorder = Recorder(file_path)
recorder.start_recording(program)




