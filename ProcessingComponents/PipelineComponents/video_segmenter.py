import os
import json
from scenedetect import detect, ContentDetector
from Utility import utility
from ProcessingComponents.PipelineComponents.audio_segmenter import AudioSegmenter
from ProcessingComponents.component_base_class import Component


class VideoSegmenter:
    def __init__(self, file_path, file_name, file_format, first_component=True):
        Component.__init__(self,file_path, file_name)
        #file_format including the leading dot
        self.file_format = file_format
        self.audio_segmenter = AudioSegmenter(file_path, file_name, '.mp3')
        self.component_name = "VideoSegmenter"
        self.version = "0.1"

    def _try_run(self):
        self._detect_video_cuts()
        for scene in self.scene_list:
            if self.first_component:
                #TODO beahviour for video segmenting as first component
                continue
            else:
                split_point = int(scene[1].get_seconds()*1000)
                print(f"Cutting on second {split_point}")
                for segment_info in self.info_files:
                    if segment_info["segment_start"] < split_point < segment_info["segment_end"]:
                        print(f"Splitting segment {segment_info['segment_name']} on second {split_point/1000}")
                        self._split_segment(segment_info, split_point)
                        self._load_info_files()
                        break

    def _split_segment(self, segment_info, split_point ):
        print(segment_info)
        folder = (f'{self.dirs_path}/{segment_info["segment_name"]}')

        utility.delete_dir_and_content(folder)

        info_seg_a = {
            "segment_start": segment_info["segment_start"],
            "segment_end": split_point,
            "segment_name": f'{segment_info["segment_name"]}-1'
        }

        info_seg_b = {
            "segment_start": split_point,
            "segment_end": segment_info["segment_end"],
            "segment_name": f'{segment_info["segment_name"]}-2'
        }
        self._create_segment_files(info_seg_a)
        self._create_segment_files(info_seg_b)

    def _create_segment_files(self, segment_info):
        seg_path = f'{self.dirs_path}/{segment_info["segment_name"]}'
        os.mkdir(seg_path)
        self.audio_segmenter.create_segment(segment_info["segment_start"],segment_info["segment_end"],f'{self.dirs_path}/{segment_info["segment_name"]}/{segment_info["segment_name"]}')
        json.dump(
            segment_info,
            open(f"{seg_path}/{segment_info['segment_name']}-info.json", 'w'),
            indent=3
        )

    def _detect_video_cuts(self):
        self.scene_list = detect(f'{self.file_path}/{self.file_name}/{self.file_name}{self.file_format}', ContentDetector())


if __name__ == "__main__":
    filepath = "../../MediaFiles"
    file_name = 'test_video'
    file_format = '.mov'

    segmenter = VideoSegmenter(filepath,file_name,file_format)

    segmenter.run()








# for i, scene in enumerate(scene_list):
#     print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
#         i+1,
#         scene[0].get_timecode(), scene[0].get_frames(),
#         scene[1].get_timecode(), scene[1].get_frames(),))
