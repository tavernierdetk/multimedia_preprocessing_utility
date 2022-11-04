from ProcessingComponents.component_base_class import Component
from moviepy.editor import *
import os
import json
import datetime

class Initializer(Component):
    def __init__(self, file_path, file_name, file_info, required=True, first_component=False):
        Component.__init__(self,file_path, file_name)
        self.file_info = file_info
        self.version = "0.1"
        self.valid_video_formats = [".mkv", ".mp4", ".mpeg", ".mov"]
        self.required = required
        self.component_name = "Initializer"

    def _try_run(self):
        if self.file_info['file_specs']['extension'] in self.valid_video_formats:
            self._parse_video_to_mp3()
            del self.video
        else:
            assert False, "File type not supported"

    def _parse_video_to_mp3(self):
        self.video = VideoFileClip(os.path.join(self.file_path, f"{self.file_name}/{self.file_name}{self.file_info['file_specs']['extension']}"))
        self.video.audio.write_audiofile(os.path.join(self.file_path, f"{self.file_name}/{self.file_name}.mp3"))

if __name__ == "__main__":
    file_path = "/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles"
    file_name = "test_video"
    file_info = json.load(open(f"{file_path}/{file_name}/{file_name}-main-info.json","r"))

    initializer = Initializer(file_path, file_name, file_info)
    initializer.run()