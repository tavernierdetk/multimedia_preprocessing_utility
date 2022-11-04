import ffmpeg
import json
import os
from Utility import utility
from ProcessingComponents.component_base_class import Component

class ScreenShotsGrabber(Component):
    def __init__(self, file_path, file_name, video_file_format, first_component=False, required=False):
        Component.__init__(self,file_path, file_name)
        self.video_file_format = video_file_format
        self.full_video_file_path = f'{self.file_path}/{self.file_name}/{self.file_name}{video_file_format}'
        self.first_component = first_component
        self.required = required
        self.component_name = "ScreenshotGrabber"
        self.version = "0.1"

    def _try_run(self):
        self.probe = ffmpeg.probe(self.full_video_file_path)
        for segment in self.segments_dir_list:
            self._create_screenshots(segment)
        del self.probe

    def _create_screenshots(self, segment):

        # width = self.probe['streams'][1]['width']

        intervals = self._create_intervals(segment)
        os.mkdir(f'{self.file_path}/{self.file_name}/Segments/{segment}/Screenshots')
        for index, item in enumerate(intervals[1:-1]):
            print(f"Screenshot {index}")
            (
                ffmpeg
                .input(self.full_video_file_path, ss=item[1])
                # .filter('scale', width, -1)
                .output(f'{self.file_path}/{self.file_name}/Segments/{segment}/Screenshots/screenshot_{str(index)}.png', vframes=1)
                .run()
            )


    def _create_intervals(self, segment):
        interval = json.load(open(f'{self.file_path}/{self.file_name}/Segments/{segment}/{segment}-info.json','rb'))
        time = interval['segment_end'] - interval['segment_start']
        parts = 5

        intervals = time // parts
        intervals = int(intervals)
        start_time = interval['segment_start']

        interval_list = []
        for i in range(parts):
            interval_list.append(
                (
                    ((i * intervals) + start_time)/1000,
                    ((((i + 1) * intervals) + start_time))/1000
                )
            )
            start_time += intervals
        return interval_list


if __name__ == "__main__":
    file_path = '/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles'
    file_name = 'test_video'
    file_format = '.mov'

    grabber = ScreenShotsGrabber(file_path, file_name, file_format)
    grabber.run()